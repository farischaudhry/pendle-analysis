from abc import ABC, abstractmethod
import requests
import pandas as pd
import io
import os

class BaseAPI(ABC):
    def fetch_and_save_ohlcv_data(base_url: str, headers: dict[str, str], token_name: str, token_address: str, chain_id: int, time_frame: str):
        url = f'{base_url}/{chain_id}/prices/{token_address}/ohlcv?time_frame={time_frame}'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            csv_data = data.get('results', '')
            if csv_data:
                df = pd.read_csv(io.StringIO(csv_data))
            else:
                df = pd.DataFrame(data)

            if 'time' in df.columns:
                df['time'] = pd.to_datetime(df['time'], unit='s')
                df.set_index('time', inplace=True)

            if not df.empty:
                os.makedirs('data', exist_ok=True)
                df.to_csv(f'data\\{token_name}_ohlcv_data.csv')

            return df
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return None

    def fetch_and_save_ohlcv_data_daily(base_url: str, headers: dict[str, str], token_name: str, token_address: str, chain_id: int):
        return BaseAPI.fetch_and_save_ohlcv_data(base_url, headers, token_name, token_address, chain_id, 'day')

    def fetch_and_save_ohlcv_data_hourly(base_url: str, headers: dict[str, str], token_name: str, token_address: str, chain_id: int):
        return BaseAPI.fetch_and_save_ohlcv_data(base_url, headers, token_name, token_address, chain_id, 'hour')
