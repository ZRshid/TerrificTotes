from src.transform.transform_payment_type import transform_payment_type
import pytest
import pandas as pd
from pandas.testing import assert_frame_equal

@pytest.fixture(autouse=True)
def dummy_payment_types():
    data = [
{
      "payment_type_id": 1,
      "payment_type_name": "SALES_RECEIPT",
      "created_at": "2022-11-03 14:20:49.962000",
      "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
      "payment_type_id": 2,
      "payment_type_name": "SALES_REFUND",
      "created_at": "2022-11-03 14:20:49.962000",
      "last_updated": "2022-11-03 14:20:49.962000"
    }]
    test = pd.DataFrame(data)
    return test


class TestTransformPaymentsTypes:
    def test_return_dataframe(self, dummy_payment_types):
        result = transform_payment_type(dummy_payment_types)
        assert isinstance(result, pd.DataFrame)

    def test_correct_num_of_columns(self, dummy_payment_types):
        assert len(dummy_payment_types.columns) == 4
        result = transform_payment_type(dummy_payment_types)
        assert len(result.columns) == 2

    def test_correct_data(self, dummy_payment_types):
        expected = pd.DataFrame([{"payment_type_id": 1,
                                 "payment_type_name": "SALES_RECEIPT"},
                                 {"payment_type_id": 2,
                                 "payment_type_name": "SALES_REFUND"}])
        result = transform_payment_type(dummy_payment_types)
        assert_frame_equal(expected, result)

    def test_error(self):
        test_input = ["fake", "data"]
        with pytest.raises(Exception):
            transform_payment_type(test_input)