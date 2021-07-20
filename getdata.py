# use real time data from yfinance
# 1. get_data specify error message
import yfinance as yf
import userinput as ui
from datetime import timedelta


def get_hist_data(symbol, start, end):
    '''get historical stock price.
       this function is useful for both descriptive and predictive analysis'''
    while True:
        startdate = ui.get_date("{}".format(start))
        enddate = ui.get_date("{}".format(end))
        # the gap between Start date and end date should be more that 7 days
        # just to make mylife easier
        if enddate.toordinal() - startdate.toordinal() > 7:
            symbol = ui.get_symbol()
            # yfinance cannot get the enddate data
            enddate = enddate + timedelta(days=1)
            hist_data = yf.download(symbol, startdate, enddate)
            if not hist_data.empty:
                return hist_data, symbol
                break
            else:
                ui.errorprint("NO DATA FOUND. REASONS COULD BE:\
                      \n1. The ticker symbol may be invalid.\
                      \n2. No data during the selected date range.")
        else:
            ui.errorprint(" DATE RANGE SHOULD BE MORE THAN 7 DAYS ")


def main():
    get_hist_data("symbol", "start", "end")


if __name__ == '__main__':
    main()
