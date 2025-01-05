import pandas as pd
import plotly.graph_objects as go

def generate_signals(input_csv_path, output_csv_path):
    data = pd.read_csv(input_csv_path)

    data['signals'] = 0
    data['trade_type'] = 'hold'

    # Strategy Logic:
    # Buy signal: RSI < 30 and MACD crosses above signal
    # Sell signal: RSI > 70 and MACD crosses below signal
    for i in range(1, len(data)):
        if data.loc[i, 'rsi_14'] < 30 and data.loc[i, 'macd_diff'] > 0 and data.loc[i - 1, 'macd_diff'] <= 0:
            data.loc[i, 'signals'] = 1
            data.loc[i, 'trade_type'] = 'long_open'
        elif data.loc[i, 'rsi_14'] > 70 and data.loc[i, 'macd_diff'] < 0 and data.loc[i - 1, 'macd_diff'] >= 0:
            data.loc[i, 'signals'] = -1
            data.loc[i, 'trade_type'] = 'short_open'
        elif data.loc[i, 'macd_diff'] > 0 and data.loc[i - 1, 'macd_diff'] <= 0:
            data.loc[i, 'signals'] = 2
            data.loc[i, 'trade_type'] = 'long_reversal'
        elif data.loc[i, 'macd_diff'] < 0 and data.loc[i - 1, 'macd_diff'] >= 0:
            data.loc[i, 'signals'] = -2
            data.loc[i, 'trade_type'] = 'short_reversal'

    data.to_csv(output_csv_path, index=False)

    # local stats about signals
    total_data_points = len(data)
    signal_counts = data['signals'].value_counts()
    print(f"Total Data Points: {total_data_points}")
    print("Signal Counts:")
    for signal, count in signal_counts.items():
        print(f"  Signal {signal}: {count}")

def plot_signals(input_csv_path):
    data = pd.read_csv(input_csv_path)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data['datetime'], y=data['close'], mode='lines', name='Close Price', line=dict(color='blue', width=1),
    ))

    buy_signals = data[data['signals'] == 1]
    fig.add_trace(go.Scatter(
        x=buy_signals['datetime'], y=buy_signals['close'],
        mode='markers', name='Buy Signal',
        marker=dict(color='green', symbol='triangle-up', size=10),
    ))

    sell_signals = data[data['signals'] == -1]
    fig.add_trace(go.Scatter(
        x=sell_signals['datetime'], y=sell_signals['close'],
        mode='markers', name='Sell Signal',
        marker=dict(color='red', symbol='triangle-down', size=10),
    ))

    long_reversals = data[data['signals'] == 2]
    fig.add_trace(go.Scatter(
        x=long_reversals['datetime'], y=long_reversals['close'],
        mode='markers', name='Long Reversal',
        marker=dict(color='orange', symbol='circle', size=10),
    ))

    short_reversals = data[data['signals'] == -2]
    fig.add_trace(go.Scatter(
        x=short_reversals['datetime'], y=short_reversals['close'],
        mode='markers', name='Short Reversal',
        marker=dict(color='purple', symbol='x', size=10),
    ))

    fig.update_layout(
        title='Trading Signals',
        xaxis_title='Datetime',
        yaxis_title='Price',
        legend_title='Legend',
        template='plotly_white',
        xaxis=dict(rangeslider=dict(visible=True)),
    )

    # saving plot as html
    fig.write_html('/Users/shivanshgupta/Desktop/zelta hack/random_outputs/signals_plot_BTC_2019_2023_15m.html')
    fig.show()

if __name__ == "__main__":
    input_csv_path = "/Users/shivanshgupta/Desktop/zelta hack/engineered_data/BTC_2019_2023_15m.csv"
    output_csv_path = "/Users/shivanshgupta/Desktop/zelta hack/random_outputs/signals_BTC_2019_2023_15m.csv"
    
    # Generate the signals and save to CSV
    generate_signals(input_csv_path, output_csv_path)
    
    # Plot the signals
    plot_signals(output_csv_path)
