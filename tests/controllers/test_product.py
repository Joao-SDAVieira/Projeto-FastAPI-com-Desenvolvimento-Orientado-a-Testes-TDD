from typing import List
from httpx import AsyncClient
from fastapi import status

from tests.factories import product_data


async def test_controller_should_return_success(client: AsyncClient, products_url: str):
    response = await client.post(products_url, json=product_data())

    content = response.json()

    del content["updated_at"]
    del content["created_at"]
    del content["id"]

    assert response.status_code == status.HTTP_201_CREATED
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
    }


async def test_controller_read_single_product_should_return_success(
    client: AsyncClient, products_url: str, product_inserted
):
    response = await client.get(f"{products_url}{product_inserted.id}")

    content = response.json()

    del content["updated_at"]
    del content["created_at"]

    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "8.500",
        "status": True,
        "id": str(product_inserted.id),
    }
    assert response.status_code == status.HTTP_200_OK


async def test_controller_read_single_product_should_return_not_found(
    client: AsyncClient, products_url: str
):
    response = await client.get(f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }


async def test_controller_read_products_should_return_success(
    client: AsyncClient, products_url: str, products_inserted
):
    response = await client.get(products_url)

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), List)
    assert len(response.json()) > 1


async def test_controller_update_product_should_return_success(
    client: AsyncClient, products_url: str, product_inserted
):
    response = await client.patch(
        f"{products_url}{product_inserted.id}", json={"price": "7.500"}
    )
    content = response.json()
    content = response.json()

    del content["updated_at"]
    del content["created_at"]
    assert response.status_code == status.HTTP_200_OK
    assert content == {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": "7.500",
        "status": True,
        "id": str(product_inserted.id),
    }


async def test_controller_delete_product_should_return_no_content(
    client: AsyncClient, products_url: str, product_inserted
):
    response = await client.delete(f"{products_url}{product_inserted.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT


async def test_controller_delete_product_should_return_not_found(
    client: AsyncClient, products_url: str
):
    response = await client.delete(
        f"{products_url}4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {
        "detail": "Product not found with filter: 4fd7cd35-a3a0-4c1f-a78d-d24aa81e7dca"
    }
