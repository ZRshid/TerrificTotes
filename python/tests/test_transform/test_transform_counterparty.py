from src.transform.transform_counterparty import transform_counterparty
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal


@pytest.fixture(autouse=True)
def dummy_counterparty():
    data = [
        {
            "counterparty_id": 1,
            "counterparty_legal_name": "Fahey and Sons",
            "legal_address_id": 15,
            "commercial_contact": "Micheal Toy",
            "delivery_contact": "Mrs. Lucy Runolfsdottir",
            "created_at": "2022-11-03 14:20:51.563000",
            "last_updated": "2022-11-03 14:20:51.563000",
        },
        {
            "counterparty_id": 2,
            "counterparty_legal_name": "Leannon, Predovic and Morar",
            "legal_address_id": 28,
            "commercial_contact": "Melba Sanford",
            "delivery_contact": "Jean Hane III",
            "created_at": "2022-11-03 14:20:51.563000",
            "last_updated": "2022-11-03 14:20:51.563000",
        },
    ]
    test = pd.DataFrame(data)
    return test


@pytest.fixture(autouse=True)
def dummy_address():
    data = [
        {
            "address_id": 15,
            "address_line_1": "605 Haskell Trafficway",
            "address_line_2": "Axel Freeway",
            "district": None,
            "city": "East Bobbie",
            "postal_code": "88253-4257",
            "country": "Heard Island and McDonald Islands",
            "phone": "9687 937447",
            "created_at": "2022-11-03 14:20:49.962000",
            "last_updated": "2022-11-03 14:20:49.962000",
        },
        {
            "address_id": 28,
            "address_line_1": "079 Horacio Landing",
            "address_line_2": None,
            "district": None,
            "city": "Utica",
            "postal_code": "93045",
            "country": "Austria",
            "phone": "7772 084705",
            "created_at": "2022-11-03 14:20:49.962000",
            "last_updated": "2022-11-03 14:20:49.962000",
        },
    ]
    test = pd.DataFrame(data)
    return test

class TestTransformCounterparty:
    def test_return_dataframe(self, dummy_counterparty, dummy_address):
        result = transform_counterparty(dummy_counterparty, dummy_address)
        assert isinstance(result, pd.DataFrame)


    def test_correct_num_of_columns_after_drop(self, dummy_counterparty, dummy_address):
        assert len(dummy_counterparty.columns) == 7
        response = transform_counterparty(dummy_counterparty, dummy_address)
        assert len(response.columns) == 9


    def test_data_is_correct(self, dummy_counterparty, dummy_address):
        result = transform_counterparty(dummy_counterparty, dummy_address)
        expected = pd.DataFrame(
            [
                {
                    "counterparty_id": 1,
                    "counterparty_legal_name": "Fahey and Sons",
                    "counterparty_legal_address_line_1": "605 Haskell Trafficway",
                    "counterparty_legal_address_line_2": "Axel Freeway",
                    "counterparty_legal_district": None,
                    "counterparty_legal_city": "East Bobbie",
                    "counterparty_legal_postal_code": "88253-4257",
                    "counterparty_legal_country": "Heard Island and McDonald Islands",
                    "counterparty_legal_phone_number": "9687 937447",
                },
                {
                    "counterparty_id": 2,
                    "counterparty_legal_name": "Leannon, Predovic and Morar",
                    "counterparty_legal_address_line_1": "079 Horacio Landing",
                    "counterparty_legal_address_line_2": None,
                    "counterparty_legal_district": None,
                    "counterparty_legal_city": "Utica",
                    "counterparty_legal_postal_code": "93045",
                    "counterparty_legal_country": "Austria",
                    "counterparty_legal_phone_number": "7772 084705",
                },
            ]
        )
        assert_frame_equal(result, expected)

class TestErrorHandling:
    def test_error_input_datatype(self):
        with pytest.raises(TypeError, match="counterparty is a dataframe"):
            transform_counterparty("not a df", "hello")

        with pytest.raises(TypeError, match="address is a dataframe"):
            transform_counterparty(pd.DataFrame(), 123)

    def test_missing_columns_in_counterparty(self):
        counterparty = pd.DataFrame([{"counterparty_id": 1}])
        address = pd.DataFrame([{"address_id": 15, "address_line_1": "test", "city": "test", "postal_code": "test", "country": "test"}])
        with pytest.raises(ValueError, match="required columns missing in counterparty"):
            transform_counterparty(counterparty, address)

    def test_missing_columns_in_address(self):
        counterparty = pd.DataFrame([{"counterparty_id": 1, "counterparty_legal_name": "Test", "legal_address_id": 15}])
        address = pd.DataFrame([{"address_id": 15}])
        with pytest.raises(ValueError, match="required columns missing in address"):
            transform_counterparty(counterparty, address)

    def test_error_given_invalid_datatype(self, dummy_counterparty):
        address = pd.DataFrame([{
            "address_id": [15],
            "address_line_1": "605 Haskell Trafficway",
            "address_line_2": "Axel Freeway",
            "district": None,
            "city": "East Bobbie",
            "postal_code": "88253-4257",
            "country": "Heard Island and McDonald Islands",
            "phone": "9687 937447",
            "created_at": "2022-11-03 14:20:49.962000",
            "last_updated": "2022-11-03 14:20:49.962000",
        },
        {
            "address_id": 28,
            "address_line_1": "079 Horacio Landing",
            "address_line_2": None,
            "district": None,
            "city": "Utica",
            "postal_code": "93045",
            "country": "Austria",
            "phone": "7772 084705",
            "created_at": "2022-11-03 14:20:49.962000",
            "last_updated": "2022-11-03 14:20:49.962000",
        }])
        with pytest.raises(Exception):
            transform_counterparty(dummy_counterparty, address)