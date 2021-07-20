'''This module has 2 functions:
   1) get user input.
   2) formatting print and output.'''

from datetime import datetime as dt
from rich.console import Console
from tabulate import tabulate
import pandas as pd


def uiprint(text):
    '''formatting input message'''
    console = Console()
    # console.print("[bold yellow]-[bold yellow]"*80)
    inputvalue = console.input(" "*7 + "[yellow]" + text + "[yellow]")
    # console.print("[bold yellow]-[bold yellow]"*80)
    return inputvalue


def errorprint(error):
    '''formatting error message'''
    console = Console()
    console.print("[bold red]x[bold red]"*80)
    console.print("{:^90}".format("[red]ERROR MESSAGE[red]"))
    console.print("{:^120}".format(" :dizzy_face: [bold red]" + error + "[bold red] :dizzy_face: "))
    console.print("{:^90}".format("[red]PLEASE TRY AGAIN[red]"))
    console.print("[bold red]x[bold red]"*80)


def discl_print(info):
    '''formatting information to users'''
    console = Console()
    console.print("[bold yellow]|[bold yellow]"+"{:^78}".format(info)+"[bold yellow]|[bold yellow]")


def print_table(dataframe, tablename):
    '''formatting dataframe to get pretty table outputs'''
    headerlist = list(dataframe.columns.values)
    console = Console()
    print("{:*^90}".format(tablename))
    print(tabulate(dataframe, headers=headerlist, tablefmt="fancy_grid"))
    print("{:*^90}".format("END OF THE TABLE"))
    # console.print("\
    #     [green][If the table looks strange,you can magnify the terminal window.]\
    #     \n        [If everything's fine, just ignore me.][green]")


def get_date(start):
    '''Get date, valid date format'''
    while True:
        try:
            text = "PLEASE ENTER {} DATE (YYYY-MM-DD): ".format(start)
            date = uiprint(text)
            date = dt.strptime(date, "%Y-%m-%d")
            return date
            break
        except ValueError:
            errorprint(" INVALID DATE FORMAT ")


def get_symbol():
    '''Get ticker symbol, valid if it contains non-alphabet or non-number'''
    while True:
        symbol = uiprint("PLEASE ENTER A TICKER SYMBOL (eg. AMZN): ")
        if symbol.isalnum():
            return symbol
            break
        else:
            errorprint(" TIKER SYMBOL CONTAINS ILLEGAL CHARACTORS ")


def get_mav_value():
    '''Get moving average days, it has to be integer, and has to >1'''
    while True:
        try:
            ma_num = int(uiprint("PLEASE ENTER A MOVING AVERAGE NUMBER (n>1): "))
            if ma_num > 1:
                return ma_num
                break
            else:
                errorprint(" THE NUMBER SHOULD > 1 ")
        except ValueError:
            errorprint(" IT'S NOT A NUMBER OR THE NUMBER IS TOOOOOO BIG ")


def main():
    get_date("START")

if __name__ == '__main__':
    main()
