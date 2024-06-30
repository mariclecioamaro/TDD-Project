from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncioMotorClient, AsyncioMotordatabase
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
import pymongo

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncioMotorClient = db_client.get()
        self.database: AsyncioMotordatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())
    
    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({'id': id})

        if not result:
            raise NotFoundException(message=f"Product not found whith filter: {id}")

        return ProductOut(**result)
    
    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]
    

    async def update(self, id: UUID, body=ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={'id': id},
            update={"$set": body.model_dump()},
            return_document=pymongo.ReturnDocument.AFTER
        )

        return ProductOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({'id': id})
        if not product:
            raise NotFoundException(message=f"Product not found whith filter: {id}")
        result = await self.collection.delete_one({"id": id})

        return True if result.delete_count > 0 else False

product_usecase = ProductUsecase()