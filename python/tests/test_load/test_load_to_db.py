import pytest
import pandas as pd
from unittest.mock import patch
from src.load.load_to_db import load_to_db

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


class TestLoadToDb:

    @patch("src.load.load_to_db.create_engine")
    def test_load_to_db_mocked(self, mock_create_engine, dummy_data):
        # Arrange
        test_df = dummy_data
        mock_table = "test"
        mock_user = "test"
        mock_password = "test"
        mock_host = "test"
        mock_database = "test"
        expected_db_url = f"postgresql+pg8000://{mock_user}:{mock_password}@{mock_host}/{mock_database}"
        mock_engine = mock_create_engine.return_value
        # Act
        result = load_to_db(
            test_df, mock_table, mock_user, mock_password, mock_host, mock_database
        )
        # Assert
        mock_create_engine.assert_called_once()
       
        assert mock_engine is not None
        mock_create_engine.assert_called_once_with(
            "postgresql+pg8000://test:test@test/test"
        )
        assert int(result) == 2
