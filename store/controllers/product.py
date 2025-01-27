from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status, Path
from pydantic import UUID4

from store.schemas.product import ProductIn, ProductOut, ProductUpdate
from store.usecases.product import ProductUseCase
from store.core.exceptions import NotFoundException

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def create_product(
    body: ProductIn = Body(...), usecase: ProductUseCase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def read_single_product(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)

    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def read_products(usecase: ProductUseCase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def update_product(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUseCase = Depends(),
) -> ProductOut:
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    id: UUID4 = Path(alias="id"), usecase: ProductUseCase = Depends()
):
    try:
        await usecase.delete(id=id)

    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
