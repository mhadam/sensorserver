from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.tables import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model
        self.db = db

    async def get(self, id_: Any) -> Optional[ModelType]:
        model_id = getattr(self.model, "id")
        return await self.db.query(self.model).filter(model_id == id_).first()

    async def get_multi(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return await self.db.query(self.model).offset(skip).limit(limit).all()

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        await self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def remove(self, id_: int) -> ModelType:
        obj = await self.db.query(self.model).get(id_)
        await self.db.delete(obj)
        await self.db.commit()
        return obj


class CRUDBase(CRDBase, Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    async def update(
        self, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj
