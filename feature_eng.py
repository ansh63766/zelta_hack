import os
import pandas as pd
from ta import add_all_ta_features
from ta.utils import dropna
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import MACD, SMAIndicator, EMAIndicator
from loader import load_csv_data, print_first_five_rows

# ensuring ki output folder exists
os.makedirs("engineered_data", exist_ok=True)

def add_technical_indicators(data_files):
    """
    Add technical indicators to each DataFrame using the TA library.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames loaded from CSV files.
    
    Returns:
        dict: Updated DataFrames with added technical indicators.
    """
    for file_name, df in data_files.items():
        df = dropna(df)  # Clean NaN values required for TA package
        if {"open", "high", "low", "close", "volume"}.issubset(df.columns):
            # adding technical indicators
            # Moving Averages (SMA and EMA)
            df['sma_10'] = SMAIndicator(df['close'], window=10).sma_indicator()
            df['ema_10'] = EMAIndicator(df['close'], window=10).ema_indicator()

            # Relative Strength Index (RSI)
            df['rsi_14'] = RSIIndicator(df['close'], window=14).rsi()

            # Bollinger Bands (Upper, Lower Bands, and Band Width)
            bb = BollingerBands(df['close'], window=20, window_dev=2)
            df['bb_upper'] = bb.bollinger_hband()
            df['bb_lower'] = bb.bollinger_lband()
            df['bb_width'] = bb.bollinger_wband()

            # MACD (Moving Average Convergence Divergence)
            macd = MACD(df['close'], window_slow=26, window_fast=12, window_sign=9)
            df['macd'] = macd.macd()
            df['macd_signal'] = macd.macd_signal()
            df['macd_diff'] = macd.macd_diff()

        data_files[file_name] = df
    return data_files

def add_lagged_features(data_files, lag=3):
    """
    Add lagged features to each DataFrame.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames.
        lag (int): Number of lagged features to generate.
    
    Returns:
        dict: Updated DataFrames with lagged features.
    """
    for file_name, df in data_files.items():
        lagged_features = []
        for i in range(1, lag + 1):
            for col in ["close", "volume"]:
                lagged_col = f"{col}_lag_{i}"
                lagged_features.append(lagged_col)
                df[lagged_col] = df[col].shift(i)
        data_files[file_name] = df
    return data_files

def calculate_price_changes(data_files):
    """
    Calculate percentage price changes and volatility for each DataFrame.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames.
    
    Returns:
        dict: Updated DataFrames with price changes and volatility.
    """
    for file_name, df in data_files.items():
        if "close" in df.columns:
            # Calculate price change percentage
            df['price_change_pct'] = df['close'].pct_change() * 100
            # Calculate volatility (rolling standard deviation)
            df['volatility'] = df['close'].rolling(window=5).std()

        data_files[file_name] = df
    return data_files

def save_engineered_data(data_files):
    """
    Save engineered DataFrames to CSV files.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames with engineered features.
    """
    for file_name, df in data_files.items():
        output_path = os.path.join("engineered_data", file_name)
        df.to_csv(output_path, index=False)
        print(f"Saved engineered data to {output_path}")

if __name__ == "__main__":
    # Path to the folder containing CSV files
    data_folder = "data"
    data_files = load_csv_data(data_folder)

    # Feature Engineering Steps
    data_files = add_technical_indicators(data_files)
    data_files = add_lagged_features(data_files, lag=3)
    data_files = calculate_price_changes(data_files)

    print_first_five_rows(data_files)

    # Save engineered data
    save_engineered_data(data_files)

    print("\nFeature engineering completed and all files saved in 'engineered_data' folder.")
