
import os
import pytest
import pytest_asyncio
from remotivelabs.cloud.storage import AsyncClient
from aiohttp import ClientSession


@pytest_asyncio.fixture(name="client")
async def client():

    print("\nSetting up resources...")
    access_token = os.getenv("REMOTIVE_ACCESSTOKEN")
    async with AsyncClient(access_token=access_token) as client:
        yield client
            
        res = await client.delete(
            project="beamyhack", 
            storage_file_path="test/out3.txt")

    print("\nTearing down resources...")


@pytest_asyncio.fixture(name="session")
async def session():

    print("\nSetting up resources...")
    access_token = os.getenv("REMOTIVE_ACCESSTOKEN")
    async with ClientSession() as session:
        client = AsyncClient(access_token = access_token, aiohttpSession=session)
        yield client
            
        res = await client.delete(
            project="beamyhack", 
            storage_file_path="test/out3.txt")

    print("\nTearing down resources...")    

@pytest.mark.itests
@pytest.mark.asyncio
async def test_upload_with_client(client: AsyncClient):

    res = await client.upload_file(
        project="beamyhack", 
        storage_file_path="test/out3.txt",
        file_to_upload="./poetry.lock", 
        overwrite=False )
    print(res)


@pytest.mark.itests
@pytest.mark.asyncio
async def test_upload_with_session(session: AsyncClient):


    res = await session.upload_file(
        project="beamyhack", 
        storage_file_path="test/out3.txt",
        file_to_upload="./poetry.lock", 
        overwrite=False )
    print(res)
