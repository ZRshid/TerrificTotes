from src.transform.transform_design import transform_design
import pandas as pd
import pytest

@pytest.fixture(autouse=True)
def dummy_data():
    data=[      
    {
      "design_id": 8,
      "created_at": "2022-11-03 14:20:49.962000",
      "design_name": "Wooden",
      "file_location": "/usr",
      "file_name": "wooden-20220717-npgz.json",
      "last_updated": "2022-11-03 14:20:49.962000"
    },
    {
      "design_id": 51,
      "created_at": "2023-01-12 18:50:09.935000",
      "design_name": "Bronze",
      "file_location": "/private",
      "file_name": "bronze-20221024-4dds.json",
      "last_updated": "2023-01-12 18:50:09.935000"
    },
    {
      "design_id": 69,
      "created_at": "2023-02-07 17:31:10.093000",
      "design_name": "Bronze",
      "file_location": "/lost+found",
      "file_name": "bronze-20230102-r904.json",
      "last_updated": "2023-02-07 17:31:10.093000"
    }]
    
    df_dummy_data = pd.DataFrame(data)
    return df_dummy_data
    
def test_returns_the_correct_data_type(dummy_data):
    result = transform_design(dummy_data)
    assert isinstance(result,pd.DataFrame)

def test_returns_the_correct_data_shape(dummy_data):
    result = transform_design(dummy_data)
    assert result.shape == (3,4)  

def test_checks_individual_columns_are_present_and_not_in_the_transformed_table(dummy_data):
    result = transform_design(dummy_data)
    assert "design_name" in result
    assert "file_location" in result
    assert "file_name" in result
    assert "design_id" in result
    
    assert "created_at" not in result
    assert "last_updated" not in result
    
def test_returns_the_data_in_ascending_order(dummy_data):
    result = transform_design(dummy_data)
    assert result["design_id"].is_monotonic_increasing
    
def test_handles_empty_inputs(dummy_data):
  empty_df = dummy_data.iloc[0:0]  
  result = transform_design(empty_df)
  assert result.empty
