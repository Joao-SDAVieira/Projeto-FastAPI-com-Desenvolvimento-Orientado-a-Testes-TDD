from store.usecases.product import product_usecase


async def test_usecases_should_return_success(produc_in):
    result = await product_usecase.create(body=produc_in)
    # assert isinstance(result, ProductOut)
    assert result is None
