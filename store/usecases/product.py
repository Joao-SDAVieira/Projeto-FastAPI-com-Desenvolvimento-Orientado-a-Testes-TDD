from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from store.db.mongo import db_client
from store.schemas.product import ProductIn

from bson.binary import Binary
from bson import UuidRepresentation


class ProductUseCase:
    def __init__(self):
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.colletction = self.database.get_collection("products")

    async def create(self, body: ProductIn):
        body_dict = body.model_dump()
        body_dict["id"] = Binary.from_uuid(
            body_dict["id"], uuid_representation=UuidRepresentation.STANDARD
        )
        await self.colletction.insert_one(body_dict)


product_usecase = ProductUseCase()
