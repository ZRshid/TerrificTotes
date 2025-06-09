import pytest
import pandas as pd
from src.transform.dim_date import dim_date, create_dim_date
from datetime import date


@pytest.fixture
def dummy_data():
    data = {
        "from_time": "2022-01-02 23:30:00.00",
        "to_time": "2025-06-02 23:59:59.00",
        "sales_order": [
            {
                "sales_order_id": 2,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 3,
                "staff_id": 19,
                "counterparty_id": 8,
                "units_sold": 42972,
                "unit_price": "3.94",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-07",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 8,
            },
            {
                "sales_order_id": 3,
                "created_at": "2022-11-03 14:20:52.188000",
                "last_updated": "2022-11-03 14:20:52.188000",
                "design_id": 4,
                "staff_id": 10,
                "counterparty_id": 4,
                "units_sold": 65839,
                "unit_price": "2.91",
                "currency_id": 3,
                "agreed_delivery_date": "2022-11-06",
                "agreed_payment_date": "2022-11-07",
                "agreed_delivery_location_id": 19,
            },
            {
                "sales_order_id": 4,
                "created_at": "2022-11-03 14:20:52.188000",
                "last_updated": "2022-11-03 14:20:52.188000",
                "design_id": 4,
                "staff_id": 10,
                "counterparty_id": 16,
                "units_sold": 32069,
                "unit_price": "3.89",
                "currency_id": 2,
                "agreed_delivery_date": "2022-11-05",
                "agreed_payment_date": "2022-11-07",
                "agreed_delivery_location_id": 15,
            },
            {
                "sales_order_id": 5,
                "created_at": "2022-11-03 14:20:52.186000",
                "last_updated": "2022-11-03 14:20:52.186000",
                "design_id": 7,
                "staff_id": 18,
                "counterparty_id": 4,
                "units_sold": 49659,
                "unit_price": "2.41",
                "currency_id": 3,
                "agreed_delivery_date": "2022-11-05",
                "agreed_payment_date": "2022-11-08",
                "agreed_delivery_location_id": 25,
            },
        ],
    }
    sales_data = data.get("sales_order", [])
    columns = [
        "sales_order_id",
        "created_at",
        "last_updated",
        "design_id",
        "staff_id",
        "counterparty_id",
        "units_sold",
        "unit_price",
        "currency_id",
        "agreed_delivery_date",
        "agreed_payment_date",
        "agreed_delivery_location_id",
    ]
    df_sales_order = pd.DataFrame(sales_data, columns=columns)
    return df_sales_order


class TestDimDate:
    def test_function_returns_a_dataframe(self, dummy_data):
        df_dim_date = dim_date(dummy_data)
        assert isinstance(df_dim_date, pd.DataFrame)

    def test_function_returns_a_dataframe_containing_8_columns(self, dummy_data):
        df_dim_date = dim_date(dummy_data)
        assert df_dim_date.shape[1] == 8

    def test_dataframe_is_not_empty(self, dummy_data):
        df_dim_date = dim_date(dummy_data)
        assert df_dim_date.shape[0] == 5

    def test_dataframe_has_the_correct_columns(self, dummy_data):
        df_dim_date = dim_date(dummy_data)
        expected_columns = [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
        assert list(df_dim_date.columns) == expected_columns

    def test_function_returns_an_error_when_table_is_not_generated(self):
        with pytest.raises(Exception):
            dim_date({})


class TestCreate_dim_date:
    def test_function_returns_a_dataframe(self):
        start_date = date(2025, 6, 5)
        end_date = date(2025, 6, 6)
        df_dim_date = create_dim_date(start_date, end_date)
        assert isinstance(df_dim_date, pd.DataFrame)

    def test_returns_a_dataframe_with_correct_number_of_rows(self):
        start_date = date(2025, 6, 1)
        end_date = date(2025, 6, 6)

        expected_days = 6
        df_dim_date = create_dim_date(start_date, end_date)

        assert df_dim_date.shape[0] == expected_days

    def test_function_returns_a_dataframe_containing_8_columns(self):
        start_date = date(2025, 6, 5)
        end_date = date(2025, 6, 6)
        df_dim_date = create_dim_date(start_date, end_date)
        assert df_dim_date.shape[1] == 8

    def test_dataframe_is_not_empty(self):
        start_date = date(2025, 6, 5)
        end_date = date(2025, 6, 6)
        df_dim_date = create_dim_date(start_date, end_date)
        assert df_dim_date.shape[0] == 2

    def test_dataframe_has_the_correct_columns(self):
        start_date = date(2025, 6, 5)
        end_date = date(2025, 6, 6)
        df_dim_date = create_dim_date(start_date, end_date)
        expected_columns = [
            "date_id",
            "year",
            "month",
            "day",
            "day_of_week",
            "day_name",
            "month_name",
            "quarter",
        ]
        assert list(df_dim_date.columns) == expected_columns

    def test_function_returns_an_error_when_table_is_not_generated(self):
        with pytest.raises(Exception):
            start_date = date(2025, 6, 5)
            end_date = date(2025, 6, 32)
            df_dim_date = create_dim_date(start_date, end_date)
