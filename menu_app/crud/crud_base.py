from sqlmodel import SQLModel
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


class Crud_Base():

    async def get(db: AsyncSession, model: SQLModel, id: int):
        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        return result

    async def get_list(db: AsyncSession, model: SQLModel):
        result = await db.execute(select(model))
        return result.scalars().all()

    async def create(db: AsyncSession, model: SQLModel, data):
        result = model.from_orm(data)
        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    async def update(db: AsyncSession, model: SQLModel, data, id: int):
        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        data = data.dict(exclude_unset=True)

        for key, value in data.items():
            setattr(result, key, value)

        db.add(result)
        await db.commit()
        await db.refresh(result)
        return result

    async def delete(db: AsyncSession, model: SQLModel, id: int):
        result = await db.get(model, id)
        if not result:
            raise HTTPException(
                    status_code=404,
                    detail=f"{model.__name__.lower()} not found"
            )
        await db.delete(result)
        await db.commit()
        return {"ok": True}