from src.transform.transform_transaction import transform_transaction
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

@pytest.fixture(autouse=True)
def dummy_transaction():
    data = [{
      "transaction_id": 1,
      "transaction_type": "PURCHASE",
      "sales_order_id": None,
      "purchase_order_id": 2,
      "created_at": "2022-11-03 14:20:52.186000",
      "last_updated": "2022-11-03 14:20:52.186000"
    },
    {
      "transaction_id": 3,
      "transaction_type": "SALE",
      "sales_order_id": 1,
      "purchase_order_id": None,
      "created_at": "2022-11-03 14:20:52.186000",
      "last_updated": "2022-11-03 14:20:52.186000"
    }]
    test = pd.DataFrame(data)
    return test

class TestTransformTransaction:
    def  test_return_dataframe(self, dummy_transaction):
        result = transform_transaction(dummy_transaction)
        assert isinstance(result, pd.DataFrame)

    def test_correct_num_of_columns_after_drop(self, dummy_transaction):
        assert len(dummy_transaction.columns) == 6
        response = transform_transaction(dummy_transaction)
        assert len(response.columns) == 4

    def test_data_is_correct(self, dummy_transaction):
        result = transform_transaction(dummy_transaction)
        expected = pd.DataFrame([{
      "transaction_id": 1,
      "transaction_type": "PURCHASE",
      "sales_order_id": None,
      "purchase_order_id": 2
    },
    {
        "transaction_id": 3,
        "transaction_type": "SALE",
        "sales_order_id": 1,
        "purchase_order_id": None
    }])
        assert_frame_equal(result, expected)