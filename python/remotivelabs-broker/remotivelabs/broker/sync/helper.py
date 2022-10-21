from ..generated.sync import common_pb2
from ..generated.sync import network_api_pb2
from ..generated.sync import system_api_pb2
from .. import log
import remotivelabs.broker.sync as br
import os

import base64
import grpc
import hashlib
import itertools
import ntpath
import posixpath

from glob import glob
from grpc_interceptor import ClientCallDetails, ClientInterceptor
from typing import Any, Callable, Sequence, Generator, Optional
from urllib.parse import urlparse


class HeaderInterceptor(ClientInterceptor):
    def __init__(self, header_dict):
        self.header_dict = header_dict

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        new_details = ClientCallDetails(
            call_details.method,
            call_details.timeout,
            self.header_dict.items(),
            call_details.credentials,
            call_details.wait_for_ready,
            call_details.compression,
        )

        return method(request_or_iterator, new_details)


def create_channel(
        url: str, x_api_key: Optional[str] = None
) -> grpc.intercept_channel:
    """
    Create communication channels for gRPC calls.

    :param url: URL to broker
    :param x_api_key: API key used with RemotiveBroker running in cloud.
    :return: gRPC channel
    """

    url = urlparse(url)

    if url.scheme == "https":
        creds = grpc.ssl_channel_credentials(
            root_certificates=None, private_key=None, certificate_chain=None
        )
        channel = grpc.secure_channel(
            url.hostname + ":" + str(url.port or "443"), creds
        )
    else:
        addr = url.hostname + ":" + str(url.port or "50051")
        channel = grpc.insecure_channel(addr)

    if x_api_key is None:
        x_api_key = 'none'

    intercept_channel = grpc.intercept_channel(
        channel, HeaderInterceptor({"x-api-key": x_api_key})
    )
    return intercept_channel


def publish_signals(
        client_id, stub, signals_with_payload, frequency: int = 0
) -> None:
    """
    Publish array of values for signals

    :param ClientId client_id: Named source for publisher
    :param NetworkServiceStub stub: Channel stub to send request
    :param Signal signals_with_payload: Array of signals with data
    """

    publisher_info = network_api_pb2.PublisherConfig(
        clientId=client_id,
        signals=network_api_pb2.Signals(signal=signals_with_payload),
        frequency=frequency,
    )

    try:
        stub.PublishSignals(publisher_info)
    except grpc._channel._Rendezvous as err:
        log.error(err)


def printer(signals: Sequence[common_pb2.SignalId]) -> None:
    """
    Debug printing of received array of signal with values.

    :param signals: Array of signals with values
    """

    for signal in signals:
        log.info(
            "{} {} {}".format(
                signal.id.name, signal.id.namespace.name, get_value(signal)
            )
        )


def get_sha256(path: str) -> str:
    """
    Calculate SHA256 for a file.

    :param path: Path to file
    :rtype int:
    """

    f = open(path, "rb")
    bytes = f.read()  # read entire file as bytes
    readable_hash = hashlib.sha256(bytes).hexdigest()
    f.close()
    return readable_hash


def generate_data(
        file, dest_path, chunk_size, sha256
) -> Generator[system_api_pb2.FileUploadRequest, None, None]:
    for x in itertools.count(start=0):
        if x == 0:
            fileDescription = system_api_pb2.FileDescription(
                sha256=sha256, path=dest_path
            )
            yield system_api_pb2.FileUploadRequest(
                    fileDescription=fileDescription)
        else:
            buf = file.read(chunk_size)
            if not buf:
                break
            yield system_api_pb2.FileUploadRequest(chunk=buf)


def upload_file(
        system_stub: br.system_api_pb2_grpc.SystemServiceStub,
        path: str, dest_path: str
) -> None:
    """
    Upload single file to internal storage on broker.

    :param system_stub: System gRPC channel stub
    :param path: Path to file in local file system
    :param dest_path: Path to file in broker remote storage
    """

    sha256 = get_sha256(path)
    log.debug("SHA256 for file {}: {}".format(path, sha256))
    file = open(path, "rb")

    # make sure path is unix style (necessary for windows, and does no harm om
    # linux)
    upload_iterator = generate_data(
        file, dest_path.replace(ntpath.sep, posixpath.sep), 1000000, sha256
    )
    response = system_stub.UploadFile(
        upload_iterator, compression=grpc.Compression.Gzip
    )
    log.debug("Uploaded {} with response {}".format(path, response))


def download_file(
        system_stub: br.system_api_pb2_grpc.SystemServiceStub,
        path: str, dest_path: str
) -> None:
    """
    Download file from Broker remote storage.

    :param system_stub: System gRPC channel stub
    :param path: Path to file in broker remote storage
    :param dest_path: Path to file in local file system
    """

    file = open(dest_path, "wb")
    for response in system_stub.DownloadFile(
        system_api_pb2.FileDescription(path=path.replace(ntpath.sep,
                                                         posixpath.sep))
    ):
        assert not response.HasField("errorMessage"), (
            "Error uploading file, message is: %s" % response.errorMessage
        )
        file.write(response.chunk)
    file.close()


def upload_folder(
        system_stub: br.system_api_pb2_grpc.SystemServiceStub,
        folder: str
) -> None:
    """
    Upload directory and its content to Broker remote storage.

    :param system_stub: System gRPC channel stub
    :param folder: Path to directory in local file storage
    """

    files = [
        y
        for x in os.walk(folder)
        for y in glob(os.path.join(x[0], "*"))
        if not os.path.isdir(y)
    ]
    assert len(files) != 0, (
        "Specified upload folder is empty or does not exist"
    )
    for file in files:
        upload_file(system_stub, file, file.replace(folder, ""))


def reload_configuration(
        system_stub: br.system_api_pb2_grpc.SystemServiceStub,
) -> None:
    """
    Trigger reload of configuration on Broker.

    :param system_stub: System gRPC channel stub
    """

    request = common_pb2.Empty()
    response = system_stub.ReloadConfiguration(request, timeout=60000)
    log.debug("Reload configuration with response {}".format(response))


def check_license(
        system_stub: br.system_api_pb2_grpc.SystemServiceStub,
) -> None:
    """
    Check license to Broker. Throws exception if failure.

    :param system_stub: System gRPC channel stub
    """
    status = system_stub.GetLicenseInfo(common_pb2.Empty()).status
    assert status == system_api_pb2.LicenseStatus.VALID, (
        "Check your license, status is: %d" % status
    )


def act_on_signal(
        client_id: br.common_pb2.ClientId,
        network_stub: br.network_api_pb2_grpc.NetworkServiceStub,
        sub_signals: Sequence[br.common_pb2.SignalId],
        on_change: bool,
        fun: Callable[[Sequence[br.network_api_pb2.Signal]], None],
        on_subcribed: Optional[Callable[..., None]] = None
) -> None:
    """
    Bind callback to be triggered when receiving any of the specified signals.

    :param ClientId client_id: Named source for listener
    :param network_stub: Network gRPC channel stub
    :param sub_signals: List of signals to listen for
    :param on_change: Callback to be triggered
    :param fun: Callback for receiving signals update
    :param on_subcribed: Callback for successful subscription
    """

    log.debug("Subscription started")

    sub_info = network_api_pb2.SubscriberConfig(
        clientId=client_id,
        signals=network_api_pb2.SignalIds(signalId=sub_signals),
        onChange=on_change,
    )
    try:
        subscripton = network_stub.SubscribeToSignals(sub_info, timeout=None)
        if on_subcribed:
            on_subcribed(subscripton)
        log.debug("Waiting for signal...")
        for subs_counter in subscripton:
            fun(subs_counter.signal)

    except grpc.RpcError as e:
        try:
            subscripton.cancel()
        except grpc.RpcError as e2:
            pass

    except grpc._channel._Rendezvous as err:
        log.error(err)
    # reload, alternatively non-existing signal
    log.debug("Subscription terminated")
