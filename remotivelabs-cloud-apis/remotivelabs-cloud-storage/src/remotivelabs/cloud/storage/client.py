import aiohttp
import asyncio
import os
import logging
import json
from pathlib import Path
from typing import Optional, Dict, Any, Union

logger = logging.getLogger(__name__)

logging.basicConfig(
    format="%(levelname)s - %(message)s",
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
)


class FileExistsException(Exception):
    """
    Raised when upload fails but overwrite was
    """
    pass

class AuthenticationException(Exception):
    """
    Raised when we get 401 or 403 from backend
    """
    pass

class ForbiddenException(Exception):
    """
    Raised when we get 401 or 403 from backend
    """
    pass



class AsyncClient:
    def __init__(
        self,
        access_token: str,
        base_url: str = "https://cloud.remotivelabs.com",
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[aiohttp.ClientTimeout] = None,
        aiohttpSession: Optional[aiohttp.ClientSession] = None,
        **kwargs
    ):
        """
        Initialize the AsyncClient with optional base_url, headers, and other aiohttp.ClientSession parameters.

        :param base_url: Optional base URL for all requests.
        :param headers: Optional default headers for all requests.
        :param timeout: Optional aiohttp.ClientTimeout object.
        :param kwargs: Additional keyword arguments for aiohttp.ClientSession.
        """
        self.access_token = access_token
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout or aiohttp.ClientTimeout(total=60)  # Default timeout of 60 seconds
        self.session: Optional[aiohttp.ClientSession] = aiohttpSession
        self.session_kwargs = kwargs


    async def __aenter__(self):
        print("enter")
        """
        Enter the asynchronous context manager, initializing the aiohttp ClientSession.
        """
        self.session = aiohttp.ClientSession(
            headers=self.headers,
            timeout=self.timeout,
            **self.session_kwargs
        )
        return self

    async def __aexit__(self, exc_type, exc, tb):
        print("exit")
        """
        Exit the asynchronous context manager, closing the aiohttp ClientSession.
        """
        if self.session:
            logger.debug("Closing aio.http session")
            await self.session.close()


    def _to_url(self, project:str, storage_file_path:str):
        storage_file_path = storage_file_path if storage_file_path.startswith("/")  else f"/{storage_file_path}"
        url=f"/api/project/{project}/files/storage{storage_file_path}"
        return f"{self.base_url}{url}"
    


    #@SIGN_TIME.time()
    async def __create_signed_url(self, storage_file_path:str, project:str, overwrite: bool = False, params={}
    ) -> tuple[bool, dict[str, any]]:
        headers = {}
        headers["Authorization"] = f"Bearer {self.access_token}".strip()
        headers["User-Agent"] = "smartlogger-remotivelabs"
        headers["content-type"] = "application/json"

        upload_request = {"resumable": False, "overwrite": "always" if overwrite else "never"}
        url=f"/api/project/{project}/files/storage{storage_file_path}"
        async with self.session.post(
                f"{self.base_url}{url}", headers=headers, params=params,
                data=json.dumps(upload_request)
        ) as response:
            if response.status == 401:
                logger.error("Access token not valid")
                raise Exception(
                    f"Access denied to RemotiveCloud: {response.status}, {await response.text()}"
                )
            elif response.status == 409:
                raise FileExistsException(f"File with path {storage_file_path} already exists")
            elif response.status != 200:
                raise Exception(
                    f"Request to {url} got non 200 OK from backend {response.status}, {await response.text()}"
                )
            json_res = await response.json()
            return True, json_res, response.status


    async def upload_file(
        self,
            project: str,
            storage_file_path: str,
            file_to_upload: str,
            overwrite: bool,
    ) -> tuple[bool, str]:
        storage_file_path = storage_file_path if storage_file_path.startswith("/")  else f"/{storage_file_path}"
        (success, result, code) = await self.__create_signed_url(
             overwrite=overwrite,
             project=project,
            storage_file_path=storage_file_path
        )

        if not (success):
            return (False, storage_file_path, code)

        await self.upload_signed_url(
            signed_url=result["url"],
            source_file_name=file_to_upload,
            headers=result["headers"]
        )

        return (True, storage_file_path)


    #@UPLOAD_TIME.time()
    async def upload_signed_url(self,signed_url: str, source_file_name: str, headers: dict[str, str]
    ):
        """
        Upload file to file storage with signed url and resumable remotivelabs.
        :param headers:
        :param signed_url:
        :param source_file_name:
        :return:
        """

        with open(source_file_name, 'rb') as f:
            async with self.session.put(signed_url, headers=headers, data=f) as response:
                # Check the response status and content
                if response.status not in (200, 201, 308):
                    raise Exception(
                        f"Failed to upload file: {response.status} - {await response.text()}"
                    )

    #@UPLOAD_TIME.time()
    async def delete(self, project:str, storage_file_path:str):
        """
        Upload file to file storage with signed url and resumable remotivelabs.
        :param headers:
        :param signed_url:
        :param source_file_name:
        :return:
        """
        headers = {}
        headers["Authorization"] = f"Bearer {self.access_token}".strip()
        headers["User-Agent"] = "smartlogger-remotivelabs"
        async with self.session.delete(url=self._to_url(project, storage_file_path), headers=headers) as response:
            # Check the response status and content
            print(response.status)
            if response.status not in (200, 201,204, 308):
                raise Exception(
                    f"Failed to upload file: {response.status} - {await response.text()}"
                )


    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> aiohttp.ClientResponse:
        """
        Perform an HTTP GET request.

        :param url: The endpoint or full URL.
        :param params: Query parameters as a dictionary.
        :param kwargs: Additional keyword arguments for aiohttp.ClientSession.get.
        :return: aiohttp.ClientResponse object.
        """
        full_url = self._get_url(url)
        async with self.session.get(full_url, params=params, **kwargs) as response:
            response.raise_for_status()  # Raise exception for HTTP errors
            return await response.text()  # Or response.json() / response.read()

    async def post(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> aiohttp.ClientResponse:
        """
        Perform an HTTP POST request.

        :param url: The endpoint or full URL.
        :param data: Form data to send in the body.
        :param json: JSON data to send in the body.
        :param kwargs: Additional keyword arguments for aiohttp.ClientSession.post.
        :return: aiohttp.ClientResponse object.
        """
        full_url = self._get_url(url)
        async with self.session.post(full_url, data=data, json=json, **kwargs) as response:
            response.raise_for_status()
            return await response.text()

    # Similarly, you can add other HTTP methods like PUT, DELETE, etc.
    
    async def put(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str, bytes]] = None,
        json: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> aiohttp.ClientResponse:
        full_url = self._get_url(url)
        async with self.session.put(full_url, data=data, json=json, **kwargs) as response:
            response.raise_for_status()
            return await response.text()

    async def desdflete(
        self,
        url: str,
        **kwargs
    ) -> aiohttp.ClientResponse:
        full_url = self._get_url(url)
        async with self.session.delete(full_url, **kwargs) as response:
            response.raise_for_status()
            return await response.text()

    # You can also add methods to handle more specific use-cases as needed.
