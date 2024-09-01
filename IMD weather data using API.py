#!/usr/bin/env python
# coding: utf-8

# In[4]:


import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import io  # Add this import

def download_weather_data(district, date, num_days=1, api_key=None):
    """
    Downloads daily weather data for a district from the IMD API.

    Args:
        district (str): Name of the district.
        date (str): Start date in YYYYMMDD format.
        num_days (int, optional): Number of days for which data is required (default: 1).
        api_key (str, optional): Your IMD API key (default: None).

    Returns:
        pandas.DataFrame: The downloaded weather data as a DataFrame or None if download fails.
    """

    if num_days > 30:
        raise ValueError("Maximum number of days allowed is 30")

    url = "https://mausam.imd.gov.in/api/districtwise_rainfall_api.php"
    params = {
        "district": district,
        "date": date,
        "cnt": num_days,
        "format": "csv",
        "api_key": api_key,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            data = response.text
            df = pd.read_csv(io.StringIO(data))
            return df
        else:
            print(f"Error downloading data: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error downloading data: {e}")
        return None

# Example usage
district_name = "Pune"  # Replace with your desired district
start_date = datetime(2024, 1, 1).strftime('%Y%m%d')  # Adjust start date
num_days = 5
api_key = "YOUR_API_KEY"  # Replace with your API key

if api_key is None:
    print("Please provide your IMD API key for download.")
else:
    weather_data = download_weather_data(district_name, start_date, num_days, api_key)

    if weather_data is not None:
        # Create directory if it doesn't exist
        os.makedirs("weather_data", exist_ok=True)

        filename = f"{district_name}_{start_date}_weather.csv"
        filepath = os.path.join("weather_data", filename)
        weather_data.to_csv(filepath, index=False)
        print(f"Downloaded weather data for {district_name} from {start_date} to {datetime.strptime(start_date, '%Y%m%d') + timedelta(days=num_days-1):%Y-%m-%d} and saved to {filepath}")


# In[ ]:




