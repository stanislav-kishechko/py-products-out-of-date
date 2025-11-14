import datetime
from unittest.mock import patch

import pytest

from app.main import outdated_products


@pytest.mark.parametrize(
    "today, products, expected",
    [
        (
            datetime.date(2022, 2, 2),
            [
                {
                    "name": "salmon",
                    "expiration_date": datetime.date(2022, 2, 10),
                    "price": 600
                },
                {
                    "name": "chicken",
                    "expiration_date": datetime.date(2022, 2, 5),
                    "price": 120
                },
                {
                    "name": "duck",
                    "expiration_date": datetime.date(2022, 2, 1),
                    "price": 160
                },
            ],
            ["duck"],
        ),
        (
            datetime.date(2022, 1, 1),
            [
                {
                    "name": "milk",
                    "expiration_date": datetime.date(2021, 12, 31),
                    "price": 35
                },
                {
                    "name": "meat",
                    "expiration_date": datetime.date(2022, 1, 1),
                    "price": 120
                },
            ],
            ["milk"],
        ),
        (
            datetime.date(2022, 5, 10),
            [
                {
                    "name": "bread",
                    "expiration_date": datetime.date(2022, 5, 11),
                    "price": 20
                },
                {
                    "name": "juice",
                    "expiration_date": datetime.date(2022, 5, 10),
                    "price": 50
                },
            ],
            [],
        ),
        (
            datetime.date(2023, 3, 15),
            [],
            [],
        ),
    ],
    ids=[
        "one_outdated_duck",
        "only_one_outdated_milk",
        "none_outdated_equal_and_future",
        "empty_product_list",
    ]
)
def test_outdated_products(
        today: datetime,
        products: list,
        expected: list,
        monkeypatch: patch
) -> None:
    with patch("datetime.date") as mock_date:
        mock_date.today.return_value = today
        mock_date.side_effect = lambda *args, **kwargs: datetime.date(
            *args, **kwargs
        )
        assert outdated_products(products) == expected
