# Import necessary libraries
import pandas_datareader.data as pdr
import datetime
import matplotlib.pyplot as plt

# Download historical data for required stocks
ticker = "MSFT"
ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today() - datetime.timedelta(1825), datetime.date.today())


def atr(o_df, n):
    """
    function to calculate True Range and Average True Range
    :param o_df:
    :param n:
    :return:
    """
    df = o_df.copy()
    df['H-L'] = abs(df['High'] - df['Low'])
    df['H-PC'] = abs(df['High'] - df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low'] - df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)
    df['ATR'] = df['TR'].rolling(n).mean()
    df2 = df.drop(['H-L', 'H-PC', 'L-PC'], axis=1)
    return df2


def bollinder_band(o_df, n):
    """
    function to calculate Bollinger Band
    :param o_df:
    :param n:
    :return:
    """
    df = o_df.copy()
    df["MA"] = df['Adj Close'].rolling(n).mean()
    df["BB_up"] = df["MA"] + 2 * df['Adj Close'].rolling(n).std(ddof=0)
    df["BB_dn"] = df["MA"] - 2 * df['Adj Close'].rolling(n).std(ddof=0)
    df["BB_width"] = df["BB_up"] - df["BB_dn"]
    df.dropna(inplace=True)
    return df


# Visualizing bollinger Band of the stocks for last 100 data points
bollinder_band(ohlcv, 20).iloc[-100:, [-4, -3, -2]].plot(title="Bollinger Band")
plt.show()
