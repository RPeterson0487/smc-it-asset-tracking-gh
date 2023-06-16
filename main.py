# Front end to database manager.  This version is the CLI "front end".
# Currently, this program only searches the original tables.

# TODO Add check to not return more than one of the exact same result (i.e., 123456)
# TODO Expand search to the new table.

# Standard library imports.

# Third party imports.

# Local application/library specific imports.
from database_manager import *


def show_menu():
    while True:
        print("==[ MAIN MENU ]" + "=" * (os.get_terminal_size().columns - 15))
        print("1)  Search for asset")
        # print("2)  To be announced")
        # print("3)  Also to be announced")
        print("0)  Exit")
        print()
        menu_input = input("Enter option: ")

        if menu_input == "1" or menu_input.lower() == "search":
            clear_screen()
            search()
        elif menu_input == "2":
            clear_screen()
        elif menu_input == "3":
            clear_screen()
        elif menu_input == "0" or menu_input.lower() in ("exit", "quit", "bye"):
            if close_database():
                exit()
        else:
            clear_screen()
            print("Invalid input, please try again.\n")


def clear_screen():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")


def search():
    while True:
        print('Type "back" to return to main menu.')
        print('Type "exit" to termininate program.\n')
        user_input = input("What to search for: ")

        if user_input.lower() in ["back"]:
            clear_screen()
            show_menu()
        elif user_input.lower() in ["clear"]:
            clear_screen()
            continue
        elif user_input.lower() in ["exit", "quit", "bye"]:
            if close_database():
                exit()
        else:
            search_return = search_database(user_input)
            if search_return == "Empty Search":
                print("Please input a full or partial entry to search.\n")
            else:
                for search_return_index in search_return:
                    print("\nSerial Number: " +
                          check_result_value(search_return_index.get(
                              "Serial", "keyMissing")))
                    print(
                        "Asset Number: " + check_result_value(
                            search_return_index.get("Asset", "keyMissing")))
                    if search_return_index["table"] == "IT_Assets_FT" or \
                            search_return_index["table"] == "IT_Assets_SG":
                        print("Fork Truck: " + check_result_value(
                            search_return_index.get("Fork_Truck_No", "keyMissing")))
                    print(
                        "IP Address: " + check_result_value(
                            search_return_index.get("Ip_Address", "keyMissing")))
                    print(
                        "Note: " + check_result_value(search_return_index.get(
                            "Current_User", "keyMissing")))
                    print("\nFound in table " + search_return_index["table"] +
                          "\nunder " + search_return_index["column"] + " as " + str(
                        search_return_index.get(
                            search_return_index["column"], "Error")))
                    print("-" * os.get_terminal_size().columns)

            print("=" * os.get_terminal_size().columns)


def check_result_value(value):
    if value == "keyMissing":
        return ""
    elif value == "" or value == None:
        return ""
    else:
        return str(value)


def main():
    host = "REDACTED"
    database = "REDACTED"
    username = "REDACTED"
    password = "REDACTED"

    clear_screen()
    connect_database(host, database, username, password)
    show_menu()


if __name__ == "__main__":
    main()
