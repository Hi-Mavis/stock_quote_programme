import desc_analytics
import pred_analytics
import stockinfo
from rich import print
import userinput as ui


def t_and_c():
    """Display terms and conditions from 'terms.txt'"""
    for line in open("terms.txt"):
        print(line, end="")


def display_welcome():
    welcome = "[bold yellow]WELCOME TO DMY'S STOCKQUOTE APPLICATION[bold yellow]  :smile: :moneybag:"
    print("[bold yellow]=[bold yellow]"*80)
    print(" "*80)
    print("{:^120}".format(welcome))
    print(" "*80)
    print("[bold yellow]=[bold yellow]"*80)


def display_disclaimer():
    print("[bold yellow]+[bold yellow]"+"[bold yellow]-[bold yellow]"*78+"[bold yellow]+[bold yellow]")
    ui.discl_print(" ")
    ui.discl_print("DISCLAIMER")
    ui.discl_print(" ")
    ui.discl_print("This application is only used for academic assignment")
    ui.discl_print("When making investment")
    ui.discl_print("Please don't trust the result from prediction function")
    ui.discl_print(" ")
    ui.discl_print("Cheers!")
    ui.discl_print(" ")
    print("[bold yellow]+[bold yellow]"+"[bold yellow]-[bold yellow]"*78+"[bold yellow]+[bold yellow]")


def display_menu():
    print("[bold yellow]-[bold yellow]"*80)
    print(" "*7 + ":scroll: [bold yellow] I AM MENU [bold yellow] :scroll:")
    print(" "*7 + "[bold yellow]1. Stock Basic Information Query[bold yellow]")
    print(" "*7 + "[bold yellow]2. Stock Quote Descriptive Analytics[bold yellow]")
    print(" "*7 + "[bold yellow]3. Stock Quote Prediction[bold yellow]")
    print(" "*7 + "[bold yellow]4. Read T&C[bold yellow]")
    print(" "*7 + "[bold red]0. Quit[bold red]")
    print("[bold yellow]-[bold yellow]"*80)


def process_choice(choice):
    while choice != "0":
        if choice == "1":
            stockinfo.main()  # need sub function
        elif choice == "2":
            desc_analytics.main()
        elif choice == "3":
            pred_analytics.main()
        elif choice == "4":
            t_and_c()   # need sub function
        else:
            ui.errorprint("I DONT HAVE THIS CHOICE")
        display_menu()
        choice = ui.uiprint("PLEASE CHOOSE A FUNCTION FROM MENU LIST: ")


def main():
    display_welcome()
    display_disclaimer()
    display_menu()
    choice = ui.uiprint("PLEASE CHOOSE A FUNCTION FROM MENU LIST: ")
    process_choice(choice)


if __name__ == '__main__':
    main()
