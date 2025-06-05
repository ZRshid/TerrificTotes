import pandas as pd
import logging

def transform_staff_with_department(staff_data:pd.DataFrame,dept_data:pd.DataFrame) -> pd.DataFrame:
    """Creates the staff dimension by inserting columns for department name and location,
    with data from dept_data with the department_id.

    Args:
        staff_data (pd.DataFrame): The original staff data.
        dept_data (pd.DataFrame): All the departments which exist.

    Returns:
        pd.DataFrame: A DataFrame with columns: ["staff_id", "first_name", "last_name", "department_name", "location", "email_address"]
    """
    try:
        staff_dim_df = staff_data.drop(["created_at", "last_updated", "from_time" ,"to_time"], axis='columns', errors="ignore")
        
        dept_data = dept_data[['department_id','location','department_name']]
        dept_data = dept_data.set_index('department_id') 

        staff_dim_df = staff_dim_df.join(dept_data,on="department_id")
        staff_dim_df = staff_dim_df.drop('department_id', axis=1)
        return staff_dim_df
    except Exception as e:
        logging.error(msg=f"Failed to make staff_dim DataFrame because: {e}")
        raise e
