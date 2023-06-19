# Front end to database manager.  This version is the CLI "front end".
# Currently, this program only searches the original tables.


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
    migrated_count = 0
    duplicate_count = 0
    
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
                    print()
                    if search_return_index["table"] in ["IT_Assets", "IT_Assets_Test"]:
                        output_new_table(search_return_index)
                    else:
                        if not search_return_index["is_migrated"] and not search_return_index["is_duplicate"]:
                            output_old_tables(search_return_index)
                        if search_return_index["is_migrated"]:
                            migrated_count += 1
                        if search_return_index["is_duplicate"] and not search_return_index["is_migrated"]:
                            duplicate_count += 1
                    print("-" * os.get_terminal_size().columns)
                print(f"Found {len(search_return)} result{'' if len(search_return) == 1 else 's'}.")
                if migrated_count:
                    print(f"{migrated_count} migrated 'old' entr{'y' if migrated_count == 1 else 'ies'} hidden.")
                if duplicate_count:
                    print(f"{duplicate_count} entr{'y' if duplicate_count == 1 else 'ies'} marked duplicate hidden.")
                print("=" * os.get_terminal_size().columns)


def output_new_table(search_dictionary):
    print(f"Seral Number: {check_result_value(search_dictionary.get('serial', 'keyMissing'))}")
    print(f"Model: {check_result_value(search_dictionary.get('model', 'keyMissing'))}")
    print(f"Asset Number: {check_result_value(search_dictionary.get('asset_number', 'keyMissing'))}")
    if search_dictionary["device_type"].lower() in ["fork truck computer", "scanning gun"]:
        print(f"Fork Truck: {check_result_value(search_dictionary.get('fork_truck_number', 'keyMissing'))}")
    print(f"IP Address: {check_result_value(search_dictionary.get('Ip_Address', 'keyMissing'))}")
    print(f"Notes: {check_result_value(search_dictionary.get('notes', 'keyMissing'))}")
    print(f"\nFound in table {search_dictionary['table']} under {search_dictionary['column']} as {search_dictionary.get(search_dictionary['column'], 'Error')}.")


def output_old_tables(search_dictionary):    
    print(f"Seral Number: {check_result_value(search_dictionary.get('Serial', 'keyMissing'))}")
    print(f"Model: {check_result_value(search_dictionary.get('Model', 'keyMissing'))}")
    print(f"Asset Number: {check_result_value(search_dictionary.get('Asset', 'keyMissing'))}")
    if search_dictionary["table"] in ["IT_Assets_FT", "IT_Assets_SG"]:
        print(f"Fork Truck: {check_result_value(search_dictionary.get('Fork_Truck_No', 'keyMissing'))}")
    print(f"IP Address: {check_result_value(search_dictionary.get('Ip_Address', 'keyMissing'))}")
    print(f"Notes: {check_result_value(search_dictionary.get('Current_User', 'keyMissing'))}")
    print(f"\nFound in table {search_dictionary['table']} under {search_dictionary['column']} as {search_dictionary.get(search_dictionary['column'], 'Error')}.")
    print("Migration Status: This device has not yet been migrated to the new tracking table.")


def check_result_value(value):
    if value == "keyMissing":
        return ""
    elif value == "" or value is None:
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
