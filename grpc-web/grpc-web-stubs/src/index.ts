import {
    Empty,
    ClientId,
    SignalId,
    SignalInfo,
    NameSpace,
    Frames,
    MetaData,
    FrameInfo,
    NetworkInfo
} from '../generated-ts/common_pb';

import {
    DiagnosticsServiceClient,
    DiagnosticsServicePromiseClient,
} from '../generated-ts/diagnostics_api_grpc_web_pb'


import {
    DiagnosticsRequest,
    DiagnosticsResponse,
} from '../generated-ts/diagnostics_api_pb'

import {
    NetworkServiceClient,
    NetworkServicePromiseClient,
} from '../generated-ts/network_api_grpc_web_pb'

import {
    SubscriberConfig,
    SignalIds,
    Signals,
    PublisherConfig,
    Signal,
} from '../generated-ts/network_api_pb'

import {
    SystemServiceClient,
    SystemServicePromiseClient,
} from '../generated-ts/system_api_grpc_web_pb'

import {
    Configuration,
    LicenseInfo,
    LicenseStatus,
    License,
    ReloadMessage,
    FileUploadChunkRequest,
    FileDescription,
    FileDownloadResponse,
    FileUploadResponse,
} from '../generated-ts/system_api_pb'

import {
    TrafficServiceClient,
    TrafficServicePromiseClient,
} from '../generated-ts/traffic_api_grpc_web_pb'

import {
    Mode,
    PlaybackConfig,
    PlaybackInfo,
    PlaybackInfos,
    PlaybackMode,
} from '../generated-ts/traffic_api_pb';

/*export default {
  Empty,
  ClientId,
  SignalId,
  SignalInfo,
  NameSpace,
  Frames,

  DiagnosticsServiceClient,
  DiagnosticsServicePromiseClient,

  DiagnosticsRequest,
  DiagnosticsResponse,

  NetworkServiceClient,
  NetworkServicePromiseClient,

  SubscriberConfig,
  SignalIds,
  Signals,
  PublisherConfig,
  Signal,

  SystemServiceClient,
  SystemServicePromiseClient,

  Configuration,
  LicenseInfo,
  LicenseStatus,
  License,
  ReloadMessage,
  FileUploadChunkRequest,
  FileDescription,
  FileDownloadResponse,
  FileUploadResponse,

  TrafficServiceClient,
  TrafficServicePromiseClient,

  Mode,
  PlaybackConfig,
  PlaybackInfo,
  PlaybackInfos,
  PlaybackMode,
};
*/



export {
    Empty,
    ClientId,
    SignalId,
    SignalInfo,
    NameSpace,
    Frames,
    MetaData,
    FrameInfo,
    NetworkInfo,

    DiagnosticsServiceClient,
    DiagnosticsServicePromiseClient,
    DiagnosticsRequest,
    DiagnosticsResponse,
    NetworkServiceClient,
    NetworkServicePromiseClient,
    SubscriberConfig,
    SignalIds,
    Signals,
    PublisherConfig,
    Signal,
    SystemServiceClient,
    SystemServicePromiseClient,
    Configuration,
    LicenseInfo,
    LicenseStatus,
    License,
    ReloadMessage,
    FileUploadChunkRequest,
    FileDescription,
    FileDownloadResponse,
    FileUploadResponse,

    TrafficServiceClient,
    TrafficServicePromiseClient,
    Mode,
    PlaybackConfig,
    PlaybackInfo,
    PlaybackInfos,
    PlaybackMode


}
