from asyncio import get_event_loop_policy
from pytest import fixture

from uuid import UUID

from store.db.mongo import db_client
from store.schemas.product import ProductIn
from tests.factories import product_data


@fixture(scope="session")
def event_loop():
    loop = get_event_loop_policy().new_event_loop()

    yield loop
    loop.close()


@fixture
def mongo_client():
    return db_client.get()


@fixture(autouse=True)
async def clear_collections(mongo_client):
    yield
    collections_names = await mongo_client.get_database().list_collection_names()
    for collection_name in collections_names:
        if collection_name.startswith("system"):
            continue

        await mongo_client.get_database()[collection_name].delete_many({})


@fixture
def produc_id() -> UUID:
    return UUID("65cc34b9-ecd6-4384-b464-9d8a5e9de0be")


@fixture
def produc_in(produc_id):
    return ProductIn(**product_data(), id=produc_id)
