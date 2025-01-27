from pytest import raises
from pydantic import ValidationError

from store.schemas.product import ProductIn
from tests.factories import product_data


def test_schemas_return_sucess():
    data = product_data()

    product = ProductIn(**data)

    assert product.name == "Iphone 14 pro Max"


def test_schemas_return_raise():
    data = {
        "name": "Iphone 14 pro Max",
        "quantity": 10,
        "price": 8.500,
    }

    with raises(ValidationError) as err:
        ProductIn.model_validate(data)

    assert err
