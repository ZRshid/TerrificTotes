from src.transform.transform_location import transform_location
import pandas as pd
import pytest

@pytest.fixture(autouse=True)
def dummy_dataframe():
    data = {
    "from_time": "2022-01-02 23:30:00.00", 
    "to_time": "2025-06-02 23:59:59.00", 
    "address": [
        {"address_id": 1, "address_line_1": "6826 Herzog Via", "address_line_2": None, "district": "Avon", "city": "New Patienceburgh", "postal_code": "28441", "country": "Turkey", "phone": "1803 637401", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"},
        {"address_id": 2, "address_line_1": "179 Alexie Cliffs", "address_line_2": None, "district": None, "city": "Aliso Viejo", "postal_code": "99305-7380", "country": "San Marino", "phone": "9621 880720", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}
    ]
}
    test = pd.DataFrame(data)
    return test

def test_return_dataframe_and_not_same_dataframe(dummy_dataframe):
    result = transform_location(dummy_dataframe)
    assert isinstance(result, pd.DataFrame) == False