import yfinance as yf
import pandas as pd
import userinput as ui


def get_company_list():
    return pd.read_csv("companylist.csv")


def get_local_info(local_list, symbol):
    '''Get stock information from local file.'''
    local_list = local_list[["Symbol", "Name", "MarketCap", "Sector", "industry"]]
    local_info = local_list[
        (local_list.Symbol.str.lower().str.contains(symbol.lower()))
        | (local_list.Name.str.lower().str.contains(symbol.lower()))]
    return local_info


def get_online_info(symbol):
    '''Get stock information from online resource.'''
    stock = yf.Ticker(symbol)
    title = ["symbol", "shortName", "marketCap", "sector", "industry"]
    basic_dic = {i: stock.info[i] for i in title}
    online_info = pd.DataFrame(basic_dic, index=[0])
    return online_info


def main():
    '''Get stock information from local file first.
    If no information available, then get stock information from online source.
    If still no information available, ask user to try again.'''
    local_list = get_company_list()
    while True:
        symbol = ui.get_symbol()
        local_info = get_local_info(local_list, symbol)
        if not local_info.empty:
            ui.print_table(local_info, "STOCK BASIC INFOMATION")
            break
        else:
            try:
                online_info = get_online_info(symbol)
                ui.print_table(online_info,  "STOCK BASIC INFOMATION")
                break
            except KeyError:
                ui.errorprint("THE TICKER SYMBOL DOES NOT EXIST")
            except ValueError:
                ui.errorprint("THE TICKER SYMBOL DOES NOT EXIST")


if __name__ == '__main__':
    main()
