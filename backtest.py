import os
from untrade.client import Client
from tabulate import tabulate
import json

def perform_backtest(csv_file_path):
    client = Client()

    result = client.backtest(
        file_path=csv_file_path,
        leverage=1,
        jupyter_id="screening",
    )
    return result

def parse_and_print_statistics(result):
    try:
        for item in result:
            if isinstance(item, str):
                result_data = json.loads(item.split("data: ", 1)[1])
                stats = result_data.get("result", {})
                static_stats = stats.get("static_statistics", {})
                compound_stats = stats.get("compound_statistics", {})

                static_table = [[key, value] for key, value in static_stats.items()]
                print("\nStatic Statistics:")
                print(tabulate(static_table, headers=["Metric", "Value"], tablefmt="pretty"))

                compound_table = [[key, value] for key, value in compound_stats.items()]
                print("\nCompound Statistics:")
                print(tabulate(compound_table, headers=["Metric", "Value"], tablefmt="pretty"))
                break
    except Exception as e:
        print(f"Error parsing backtest result: {e}")
        print("Raw result:", result)

if __name__ == "__main__":
    csv_file_path = "/Users/shivanshgupta/Desktop/zelta hack/signals_BTC_2019_2023_15m.csv"

    if not os.path.exists(csv_file_path):
        print(f"Error: File not found at path {csv_file_path}")
    else:
        print("### Performing backtest ###")
        backtest_result = perform_backtest(csv_file_path)

        print("### Backtest Results ###")
        if not backtest_result:
            print("No results returned from the backtest.")
        else:
            parse_and_print_statistics(backtest_result)
