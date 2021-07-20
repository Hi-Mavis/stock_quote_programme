import matplotlib.pyplot as plt
import numpy as np
import mplfinance as mpf
import userinput as ui
from sklearn.linear_model import LinearRegression
import getdata


def desc_anal(hist_data):
    '''Descriptive analytics based on closing price.'''
    desc = hist_data[["Close"]].describe().round(1)
    # add range to descriptive analytics
    desc.loc["range"] = desc.loc["max"] - desc.loc["min"]
    # add coefficient of variation to descriptive analytics
    desc.loc["cv"] = (desc.loc["std"] / desc.loc["mean"]).round(1)
    ui.print_table(desc, "DESCRIPTIVE ANALYTICS")


def wma(hist_data, mav):
    '''Add weighted moving average column to hist_data.'''
    weights = np.arange(1, mav+1)
    wmavg = hist_data["Close"].rolling(mav).apply(
        lambda prices: np.dot(prices, weights)/weights.sum(), raw=True)
    return wmavg


def macd(hist_data):
    '''Calculate the MACD and Signal Line indicators'''
    # Short Term EMA
    EMA12 = hist_data.Close.ewm(span=12, adjust=False).mean()
    # Long Term EMA
    EMA26 = hist_data.Close.ewm(span=26, adjust=False).mean()
    # get EMCD
    MACD = EMA12 - EMA26
    # Calcualte the signal line
    signal = MACD.ewm(span=9, adjust=False).mean()
    histogram = MACD - signal
    return MACD, signal, histogram


def trend(hist_data):
    '''prepare trend line data'''
    lr = LinearRegression()
    hist_data = hist_data.reset_index()
    x = np.array(hist_data.index).reshape(-1, 1)
    y = np.array(hist_data["Close"])
    lr.fit(x, y)
    hist_data["trend"] = lr.predict(x)
    hist_data.set_index("Date")
    price_trend = hist_data["trend"]
    return price_trend


def desc_graph(hist_data, symbol, mav):
    '''Historical stock price descriptive graph'''
    # customise candlestick gragh features
    mc = mpf.make_marketcolors(up="g", down="r", inherit=True)
    dmy = mpf.make_mpf_style(marketcolors=mc, mavcolors=["#4d79ff", "#d24dff"])
    kwargs = dict(type="candle", style=dmy, volume=True, ylabel="Price ($)",
                  title="\n {} Stock Price".format(symbol).upper())
    wmavg = wma(hist_data, mav)
    trendline = trend(hist_data)
    (MACD, signal, histogram) = macd(hist_data)
    addplot = [
               # add closing price, wma and trend lines to candlestick graph
               mpf.make_addplot(wmavg, color="orange", width=1),
               mpf.make_addplot(trendline, color="purple", width=1),
               mpf.make_addplot(hist_data["Close"], color="black", width=1),
               # add macd to a separate panel
               mpf.make_addplot(histogram, type='bar', width=0.7, panel=1,
                                color='dimgray', alpha=1, secondary_y=False),
               mpf.make_addplot(MACD, panel=1, color='r', title="MACD",
                                secondary_y=True),
               mpf.make_addplot(signal, panel=1, color='b', secondary_y=True)]
    # plot candlestick chart and addlines
    fig, axes = mpf.plot(hist_data, **kwargs, mav=(mav), volume_panel=2,
                         addplot=addplot, panel_ratios=(6, 2, 3), returnfig=True)
    # label lines
    label_main = ["M.A({} days)".format(mav), "WMA({} days)".format(mav),
                  "Trend Line", "Closing Price"]
    axes[0].legend(label_main)
    plt.show()


def main():
    (hist_data, symbol) = getdata.get_hist_data("symbol", "START", "END")
    desc_anal(hist_data)
    mav = ui.get_mav_value()
    desc_graph(hist_data, symbol, mav)


if __name__ == '__main__':
    main()
