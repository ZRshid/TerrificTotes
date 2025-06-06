import pytest
import pandas as pd
from src.transform.fact_sales import sales_facts

@pytest.fixture()
def dummy_sales_order():
    data = {"from_time": "2022-01-02 23:30:00.00", 
            "to_time": "2025-06-02 23:59:59.00", 
            "sales_order": [
                {"sales_order_id": 2, 
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
                "agreed_delivery_location_id": 8}, 
                {"sales_order_id": 3, 
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
                "agreed_delivery_location_id": 19}, 
                {"sales_order_id": 4, 
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
                "agreed_delivery_location_id": 15}, 
                {"sales_order_id": 5, 
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
                "agreed_delivery_location_id": 25}
            ]}
    sales_data = data.get("sales_order", [])
    columns = ["sales_order_id", "created_at", "last_updated", "design_id", "staff_id", 
                "counterparty_id", "units_sold", "unit_price", "currency_id", 
                "agreed_delivery_date", "agreed_payment_date", "agreed_delivery_location_id"]
    df_sales_order = pd.DataFrame(sales_data, columns=columns)
    return df_sales_order

@pytest.fixture()
def dummy_dim_currency():
        data = [{"currency_name": "Afghani", 
                 "currency_code": "AFN", 
                 "currency_id": 0}, 
                {"currency_name": "Euro", 
                 "currency_code": "EUR", 
                 "currency_id": 1},
                {"currency_name": "US Dollar", 
                 "currency_code": "USD", 
                 "currency_id": 2}]
        df_dim_currency = pd.DataFrame(data)
        return df_dim_currency

@pytest.fixture()
def dummy_dim_design():
        data = [{"design_id": 8, 
                 "design_name": "Wooden", 
                 "file_location": "/usr",
                 "file_name": "wooden-20220717-npgz.json"}, 
                {"design_id": 51, 
                 "design_name": "Bronze", 
                 "file_location": "/private",
                 "file_name": "bronze-20221024-4dds.json"},
                {"design_id": 8, 
                 "design_name": "Bronze", 
                 "file_location": "/lost+found",
                 "file_name": "bronze-20230102-r904.json"}]
        df_dim_design = pd.DataFrame(data)
        return df_dim_design

@pytest.fixture()
def dummy_dim_date():
        data = [{"date_id": "2022-11-03", 
                 "year": 2022, 
                 "month": 11,
                 "day": 3,
                 "day_of_week": 3, 
                 "day_name": "Thursday",
                 "month_name": "November",
                 "quarter": 4}, 
                {"date_id": "2022-11-08", 
                 "year": 2022, 
                 "month": 11,
                 "day": 8,
                 "day_of_week": 1, 
                 "day_name": "Tuesday",
                 "month_name": "November",
                 "quarter": 4},
                {"date_id": "2022-11-07", 
                 "year": 2022, 
                 "month": 11,
                 "day": 7,
                 "day_of_week": 0, 
                 "day_name": "Monday",
                 "month_name": "November",
                 "quarter": 4},]
        df_dim_date = pd.DataFrame(data)
        return df_dim_date

class TestSales_facts:
    def test_function_returns_a_dataframe(self, 
            dummy_sales_order, dummy_dim_currency, dummy_dim_design, 
            dummy_dim_date):
        pass
