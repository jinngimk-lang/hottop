import pytest

from hottop.models import ProductProfile


def test_product_profile_normalizes_category_when_present():
    product = ProductProfile(name="Ribbon Lunch", category="  food  ")

    assert product.category == "food"


def test_product_profile_rejects_blank_category_when_present():
    with pytest.raises(ValueError, match="product profile category must not be blank"):
        ProductProfile(name="Ribbon Lunch", category="   ")
