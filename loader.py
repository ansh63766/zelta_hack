import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Missing data heatmaps and trading plots will be saved in these folders
os.makedirs("missing_data_heatmaps", exist_ok=True)
os.makedirs("trading_plots", exist_ok=True)

def load_csv_data(folder_path):
    """
    Load all CSV files from a specified folder.
    
    Parameters:
        folder_path (str): Path to the folder containing CSV files.
    
    Returns:
        dict: Dictionary where keys are filenames and values are DataFrames.
    """
    data_files = {}
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".csv"):
            file_path = os.path.join(folder_path, file_name)
            df = pd.read_csv(file_path)
            # # Remove 'Unnamed: 0' column if it exists
            # if "Unnamed: 0" in df.columns:
            #     df = df.drop(columns=["Unnamed: 0"])
            data_files[file_name] = df
    return data_files

def convert_datetime_column(data_files):
    """
    Convert the 'datetime' column in each DataFrame to a datetime object and set it as the index.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames.
    
    Returns:
        None
    """
    # for file_name, df in data_files.items():
    #     if "datetime" in df.columns:
    #         df["datetime"] = pd.to_datetime(df["datetime"])
    #         df.set_index("datetime", inplace=True)
    #         data_files[file_name] = df

def print_first_five_rows(data_files):
    """
    Print the first five rows of each CSV file in a readable manner.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames loaded from CSV files.
    """
    for file_name, df in data_files.items():
        print(f"\n{'-'*60}\nFirst 5 rows of {file_name}:\n{'-'*60}")
        print(df.head())
        print("\n")

def print_missing_data_summary(data_files):
    """
    Print the number of missing data points in each column for each CSV file.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames loaded from CSV files.
    """
    for file_name, df in data_files.items():
        print(f"\n{'-'*60}\nMissing Data Summary for {file_name}:\n{'-'*60}")
        missing_counts = df.isnull().sum()
        for column, count in missing_counts.items():
            print(f"{column}: {count} missing values")
        print("\n")

def analyze_missing_values(data_files):
    """
    Calculate missing data values for each DataFrame and generate a heatmap.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames loaded from CSV files.
    """
    for file_name, df in data_files.items():
        missing_values = df.isnull()
        plt.figure(figsize=(10, 6))
        sns.heatmap(missing_values, cbar=False, cmap="viridis", yticklabels=False)
        plt.title(f"Missing Data Heatmap for {file_name}", fontsize=14)
        heatmap_path = os.path.join("missing_data_heatmaps", f"{file_name}_missing_heatmap.png")
        plt.savefig(heatmap_path, bbox_inches="tight")
        plt.close()
        print(f"Heatmap saved for {file_name} at {heatmap_path}")

def generate_trading_plots(data_files):
    """
    Generate and save trading-related plots for each CSV file.
    
    Parameters:
        data_files (dict): Dictionary of DataFrames loaded from CSV files.
    """
    for file_name, df in data_files.items():
        if {"open", "high", "low", "close", "volume"}.issubset(df.columns):
            plt.figure(figsize=(12, 8))
            
            fig, axs = plt.subplots(5, 1, figsize=(14, 18), sharex=True, gridspec_kw={'hspace': 0.3})
            trading_columns = ["open", "high", "low", "close", "volume"]
            colors = ["blue", "green", "red", "purple", "orange"]
            
            for ax, column, color in zip(axs, trading_columns, colors):
                sns.lineplot(data=df, x=df.index, y=column, ax=ax, color=color)
                ax.set_title(f"{column.capitalize()} Over Time", fontsize=12)
                ax.set_ylabel(column.capitalize())
                ax.grid(True)
            
            trading_plot_path = os.path.join("trading_plots", f"{file_name}_trading_plot.png")
            plt.savefig(trading_plot_path, bbox_inches="tight")
            plt.close(fig)
            print(f"Trading plots saved for {file_name} at {trading_plot_path}")

if __name__ == "__main__":
    # Path to the folder containing CSV files
    data_folder = "data"

    data_files = load_csv_data(data_folder)

    convert_datetime_column(data_files)

    print_first_five_rows(data_files)

    print_missing_data_summary(data_files)

    analyze_missing_values(data_files)

    generate_trading_plots(data_files)

    print("\nAll heatmaps and trading plots have been generated and saved.")

# -> there is no missing data in the data files, so the heatmaps will be empty.
# -> as the timeframe increases (e.g., 1 minute → 1 day), trading patterns consolidate, showing aggregated movements over broader intervals.

# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_6h.csv:
# ------------------------------------------------------------
#                          open      high       low     close    volume
# datetime                                                             
# 2019-09-08 12:00:00  10000.00  10000.00  10000.00  10000.00     0.002
# 2019-09-08 18:00:00  10344.77  10412.65  10324.77  10391.63  3096.289
# 2019-09-09 00:00:00  10316.62  10316.68  10251.51  10304.32  2131.251
# 2019-09-09 06:00:00  10304.32  10475.54  10077.22  10414.60  3779.472
# 2019-09-09 12:00:00  10411.70  10411.70  10183.31  10263.33  5426.249



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_15m.csv:
# ------------------------------------------------------------
#                         open     high      low    close  volume
# datetime                                                       
# 2019-09-08 17:45:00  10000.0  10000.0  10000.0  10000.0   0.002
# 2019-09-08 18:00:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:15:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:30:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:45:00  10000.0  10000.0  10000.0  10000.0   0.000



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_1m.csv:
# ------------------------------------------------------------
#                         open     high      low    close  volume
# datetime                                                       
# 2019-09-08 17:57:00  10000.0  10000.0  10000.0  10000.0   0.001
# 2019-09-08 17:58:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 17:59:00  10000.0  10000.0  10000.0  10000.0   0.001
# 2019-09-08 18:00:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:01:00  10000.0  10000.0  10000.0  10000.0   0.000



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_3d.csv:
# ------------------------------------------------------------
#                 open      high       low     close     volume
# datetime                                                     
# 2019-09-07  10000.00  10475.54  10000.00  10307.00  17920.664
# 2019-09-10  10307.00  10450.13   9884.31  10415.13  35576.511
# 2019-09-13  10414.96  10440.55  10024.81  10302.22  60445.600
# 2019-09-16  10302.00  10353.81  10080.70  10155.16  63538.139
# 2019-09-19  10154.70  10331.62   9530.02   9983.33  73137.051



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_12h.csv:
# ------------------------------------------------------------
#                          open      high       low     close    volume
# datetime                                                             
# 2019-09-08 12:00:00  10000.00  10412.65  10000.00  10391.63  3096.291
# 2019-09-09 00:00:00  10316.62  10475.54  10077.22  10414.60  5910.723
# 2019-09-09 12:00:00  10411.70  10420.65  10183.31  10307.00  8913.650
# 2019-09-10 00:00:00  10307.00  10382.97  10206.87  10254.56  4662.539
# 2019-09-10 12:00:00  10252.70  10270.58   9940.87  10102.02  4406.416



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_1h.csv:
# ------------------------------------------------------------
#                          open      high       low     close   volume
# datetime                                                            
# 2019-09-08 17:00:00  10000.00  10000.00  10000.00  10000.00    0.002
# 2019-09-08 18:00:00  10000.00  10000.00  10000.00  10000.00    0.000
# 2019-09-08 19:00:00  10344.77  10357.53  10337.43  10340.12  471.659
# 2019-09-08 20:00:00  10340.12  10368.64  10334.54  10351.42  583.271
# 2019-09-08 21:00:00  10351.42  10391.90  10324.77  10391.90  689.759



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_30m.csv:
# ------------------------------------------------------------
#                          open      high       low     close   volume
# datetime                                                            
# 2019-09-08 17:30:00  10000.00  10000.00  10000.00  10000.00    0.002
# 2019-09-08 18:00:00  10000.00  10000.00  10000.00  10000.00    0.000
# 2019-09-08 18:30:00  10000.00  10000.00  10000.00  10000.00    0.000
# 2019-09-08 19:00:00  10344.77  10357.53  10342.90  10354.62  136.177
# 2019-09-08 19:30:00  10354.62  10357.35  10337.43  10340.12  335.482



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_2h.csv:
# ------------------------------------------------------------
#                          open      high       low     close    volume
# datetime                                                             
# 2019-09-08 16:00:00  10000.00  10000.00  10000.00  10000.00     0.002
# 2019-09-08 18:00:00  10344.77  10357.53  10337.43  10340.12   471.659
# 2019-09-08 20:00:00  10340.12  10391.90  10324.77  10391.90  1273.030
# 2019-09-08 22:00:00  10392.59  10412.65  10366.57  10391.63  1351.600
# 2019-09-09 00:00:00  10391.63  10391.63  10391.63  10391.63     0.000



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_1d.csv:
# ------------------------------------------------------------
#                 open      high       low     close     volume
# datetime                                                     
# 2019-09-08  10000.00  10412.65  10000.00  10391.63   3096.291
# 2019-09-09  10316.62  10475.54  10077.22  10307.00  14824.373
# 2019-09-10  10307.00  10382.97   9940.87  10102.02   9068.955
# 2019-09-11  10094.27  10293.11   9884.31  10159.55  10897.922
# 2019-09-12  10163.06  10450.13  10042.12  10415.13  15609.634



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_3m.csv:
# ------------------------------------------------------------
#                         open     high      low    close  volume
# datetime                                                       
# 2019-09-08 17:57:00  10000.0  10000.0  10000.0  10000.0   0.002
# 2019-09-08 18:00:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:03:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:06:00  10000.0  10000.0  10000.0  10000.0   0.000
# 2019-09-08 18:09:00  10000.0  10000.0  10000.0  10000.0   0.000



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_1w.csv:
# ------------------------------------------------------------
#                 open      high       low     close      volume
# datetime                                                      
# 2019-09-02  10000.00  10412.65  10000.00  10391.63    3096.291
# 2019-09-09  10316.62  10475.54   9884.31  10302.22  110846.484
# 2019-09-16  10302.00  10353.81   9530.02  10023.04  160591.544
# 2019-09-23   8061.98  10046.91   7700.67   8041.96  279795.272
# 2019-09-30   8042.08   8499.00   7709.01   7852.79  257976.889



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_4h.csv:
# ------------------------------------------------------------
#                          open      high       low     close    volume
# datetime                                                             
# 2019-09-08 16:00:00  10000.00  10357.53  10000.00  10340.12   471.661
# 2019-09-08 20:00:00  10340.12  10412.65  10324.77  10391.63  2624.630
# 2019-09-09 00:00:00  10316.62  10316.68  10267.37  10297.89   779.449
# 2019-09-09 04:00:00  10297.89  10316.34  10092.71  10149.47  2664.789
# 2019-09-09 08:00:00  10149.47  10475.54  10077.22  10414.60  2466.485



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_8h.csv:
# ------------------------------------------------------------
#                          open      high       low     close    volume
# datetime                                                             
# 2019-09-08 16:00:00  10000.00  10412.65  10000.00  10391.63  3096.291
# 2019-09-09 00:00:00  10316.62  10316.68  10092.71  10149.47  3444.238
# 2019-09-09 08:00:00  10149.47  10475.54  10077.22  10314.26  5852.500
# 2019-09-09 16:00:00  10314.26  10420.65  10183.31  10307.00  5527.635
# 2019-09-10 00:00:00  10307.00  10382.97  10226.81  10272.46  3253.538



# ------------------------------------------------------------
# First 5 rows of BTC_2019_2023_1month.csv:
# ------------------------------------------------------------
#                open      high      low    close       volume
# datetime                                                    
# 2019-09-01  8042.08  10475.54  7700.67  8041.96   608742.111
# 2019-10-01  8285.31  10408.48  7172.76  9150.00  2439561.887
# 2019-11-01  9149.88   9550.00  6510.19  7542.93  4042674.725
# 2019-12-01  7541.08   7800.00  6427.00  7189.00  4063882.296
# 2020-01-01  7189.43   9599.00  6863.44  9364.51  5165281.358