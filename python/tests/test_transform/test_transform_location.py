from src.transform.transform_location import transform_location
import pandas as pd
import pytest

@pytest.fixture(autouse=True)
def dummy_dataframe():
    data = [
    {
        "from_time": "2022-01-02 23:30:00.00", 
        "to_time": "2025-06-02 23:59:59.00", 
        "address_id": 1, 
        "address_line_1": "6826 Herzog Via", 
        "address_line_2": None, 
        "district": "Avon", 
        "city": "New Patienceburgh", 
        "postal_code": "28441", 
        "country": "Turkey", 
        "phone": "1803 637401", 
        "created_at": "2022-11-03 14:20:49.962000", 
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
        "from_time": "2022-01-02 23:30:00.00", 
        "to_time": "2025-06-02 23:59:59.00", 
        "address_id": 2,
        "address_line_1": "179 Alexie Cliffs", 
        "address_line_2": None,
        "district": None,
        "city": "Aliso Viejo",
        "postal_code": "99305-7380",
        "country": "San Marino",
        "phone": "9621 880720",
        "created_at": "2022-11-03 14:20:49.962000",
        "last_updated": "2022-11-03 14:20:49.962000"
    },
    {"address_id": 30, "address_line_1": "0336 Ruthe Heights", "address_line_2": None, "district": "Buckinghamshire", "city": "Lake Myrlfurt", "postal_code": "94545-4284", "country": "Falkland Islands (Malvinas)", "phone": "1083 286132", "created_at": "2022-11-03 14:20:49.962000", "last_updated": "2022-11-03 14:20:49.962000"}
]
    test = pd.DataFrame(data)
    return test

def test_return_dataframe(dummy_dataframe):
    result = transform_location(dummy_dataframe)
    assert isinstance(result, pd.DataFrame)

def test_correct_len_of_columns_after_drop(dummy_dataframe):
    length = len(dummy_dataframe.columns)
    assert length == 12
    response = transform_location(dummy_dataframe)
    result = len(response.columns)
    assert result == 8

def test_changed_column_name(dummy_dataframe):
    assert "address_id" in dummy_dataframe.columns
    assert "location_id" not in dummy_dataframe.columns
    response = transform_location(dummy_dataframe)
    assert "address_id" not in response.columns
    assert "location_id" in response.columns