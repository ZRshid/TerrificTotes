import pytest
import pandas as pd
from unittest import mock
from src.transform.create_sql import create_sql


@pytest.fixture
def dummy_data():
    data = [
        {
            "sales_record_id": 0,
            "sales_order_id": 2,
            "created_date": "2022-11-03",
            "created_time": "14:20:52.186000",
            "last_updated_date": "2022-11-03",
            "last_updated_time": "14:20:52.186000",
            "sales_staff_id": 19,
            "counterparty_id": 8,
            "units_sold": 42972,
            "unit_price": "3.94",
            "currency_id": 2,
            "design_id": 3,
            "agreed_payment_date": "2022-11-08",
            "agreed_delivery_date": "2022-11-07",
            "agreed_delivery_location_id": 8,
        },
        {
            "sales_record_id": 1,
            "sales_order_id": 3,
            "created_date": "2022-11-03",
            "created_time": "14:20:52.188000",
            "last_updated_date": "2022-11-03",
            "last_updated_time": "14:20:52.188000",
            "sales_staff_id": 10,
            "counterparty_id": 4,
            "units_sold": 65839,
            "unit_price": "2.91",
            "currency_id": 3,
            "design_id": 4,
            "agreed_payment_date": "2022-11-07",
            "agreed_delivery_date": "2022-11-06",
            "agreed_delivery_location_id": 19,
        },
    ]
    df = pd.DataFrame(data)
    return df


class TestCreate_sql:
    def test_function_returns_a_non_empty_table(self, dummy_data):
        create_sql(dummy_data, "test_table")
