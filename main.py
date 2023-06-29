# Front end to database manager.  This version is the CLI "front end".

# TODO: Very large rewrite, consolidate everything into one list instead of old and new.
# TODO: Validate all edit fields against table requirements.
# TODO: Validate edit fields, change none to blanks / underscores.
# TODO: Convert date formats. Users should see/enter MM/DD/YYYY.
# TODO: Expand on list fields to offer edit options to existing data.
# TODO: Validate the various option select fields to protect against bad inputs.
# TODO: Go through and standardize input lines.
# TODO: List commands for each input. Maybe use a list of acceptable commands in each call?
# TODO: Reorganize functions and label / document.

# Standard library imports.
from datetime import datetime
import os

# Third party imports.

# Local application/library specific imports.
from database_manager import *


def show_menu():
    while True:
        print(f"==[ MAIN MENU ]{'=' * (os.get_terminal_size().columns - 15)}")
        print("1)  Search for asset")
        print("2)  Edit existing asset")
        # print("3)  TEST METHOD")
        print("0)  Exit")
        print()
        menu_input = input("Enter option: ")

        if menu_input == "1" or menu_input.lower() == "search":
            clear_screen()
            search_assets()
        elif menu_input == "2" or menu_input.lower() == "edit":
            clear_screen()
            edit_asset()
        elif menu_input == "3":
            clear_screen()
            test_method()
        elif menu_input == "0" or menu_input.lower() in ("exit", "quit", "bye"):
            clear_screen()
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


def get_input(prompt: str):
    print('Type "back" to return to main menu.')
    print('Type "exit" to termininate program.\n')
    user_input = input(prompt)

    if user_input.lower() in ["back"]:
        clear_screen()
        show_menu()
    elif user_input.lower() in ["clear"]:
        clear_screen()
    elif user_input.lower() in ["exit", "quit", "bye"]:
        clear_screen()
        if close_database():
            exit()
    else:
        return user_input


def search_assets():
    while True:
        user_input = get_input("Search for asset: ")
        if user_input is None:
            continue
        else:
            results_old, results_new, number_migrated, number_duplicate = search(user_input)
            if results_old == "Empty Search" and results_new == "Empty Search":
                print("Please input a full or partial entry to search.\n")
                continue
            else:
                for results_index in results_old:
                    print()
                    output_limited_old(results_index)
                    print("-" * os.get_terminal_size().columns)
                for results_index in results_new:
                    print()
                    output_limited_new(results_index)
                    print("-" * os.get_terminal_size().columns)
                
                print(f"Found {len(results_old) + len(results_new)} result{'' if (len(results_old) + len(results_new)) == 1 else 's'}.")
                if number_migrated:
                    print(f"{number_migrated} migrated 'old' entr{'y' if number_migrated == 1 else 'ies'} hidden.")
                if number_duplicate:
                    print(f"{number_duplicate} entr{'y' if number_duplicate == 1 else 'ies'} marked duplicate hidden.")
                print("=" * os.get_terminal_size().columns)
        

def search(search_for):
    search_results_old = []
    search_results_new = []
    migrated_count = 0
    duplicate_count = 0
    
    search_return = search_database(search_for)
    if search_return == "Empty Search":
        return search_return, search_return, search_return, search_return
    
    for search_return_index in search_return:
        if search_return_index["table"] in config.new_tables:
            search_results_new.append(search_return_index)
        else:
            if search_return_index["is_migrated"]:
                migrated_count += 1
            elif search_return_index["is_duplicate"]:
                duplicate_count += 1
            else:
                search_results_old.append(search_return_index)
                
    return search_results_old, search_results_new, migrated_count, duplicate_count


def edit_asset():
    while True:
        option_number = 0
        
        user_input = get_input("Search for asset: ")
        if user_input is None:
            continue
        else:
            results_old, results_new, number_migrated, number_duplicate = search(user_input)
            if results_old == "Empty Search" and results_new == "Empty Search":
                print("Please input a full or partial entry to search.\n")
                continue
            elif (len(results_old) + len(results_new)) == 0:
                print("Found 0 results.\n")
                continue
            elif (len(results_old) + len(results_new)) > 15:
                print("Too many results, please refine your search.\n")
                continue
            else:
                if (len(results_old) + len(results_new)) > 1:
                    for results_index in results_old:
                        option_number += 1
                        print()
                        print(f"Option {option_number})\n")
                        output_limited_old(results_index)
                        print("-" * os.get_terminal_size().columns)
                    for results_index in results_new:
                        option_number += 1
                        print()
                        print(f"Option {option_number})\n")
                        output_limited_new(results_index)
                        print("-" * os.get_terminal_size().columns)
                    print(f"Found {len(results_old) + len(results_new)} result{'' if (len(results_old) + len(results_new)) == 1 else 's'}.")
                    print("=" * os.get_terminal_size().columns)
                
                while True:
                    if (len(results_old) + len(results_new)) == 1:
                        option_select = 1
                    else:
                        option_select = get_input("Select asset to edit: ")
                        print()
                        if option_select is None:
                            break
                    
                    if int(option_select) <= len(results_old):
                        selected_option = check_migrations_duplicates(results_old[int(option_select)-1]['Serial'])
                        edit_screen(selected_option)
                    else:
                        option_select = int(option_select) - len(results_old)
                        selected_option = check_migrations_duplicates(results_new[int(option_select)-1]['serial'])
                        edit_screen(selected_option)
                    break
        edit_screen(selected_option)


def edit_screen(asset):
    keys_list = list(asset.keys())
    list_fields = ("asset_reference", "notes")
    date_fields = ("deployment_date", "purchase_date", "contract_expiration_date", "last_seen")
    
    while True:
        clear_screen()
        option_number = 0
        ignore_keys = ["last_seen", "is_verified", "table", "column"]
        
        for key in asset:
            if key not in ignore_keys:
                option_number += 1
                if asset.get(key) is None:
                    print(f"{option_number})  {key}: {'_' * 10}")
                else:
                    print(f"{option_number})  {key}: {asset.get(key)}")
        print("\nCommands:\nsave: Save and go back to main menu.  back: Discard and go back to main menu.  exit: Discard and quit program.: ")
        option_select = input("\nEnter command or Select field to edit: ")
        if option_select.strip() is None or option_select.strip() == "":
            continue
        elif option_select.strip().lower() == "save":
            pass
        elif option_select.strip().lower() == "back":
            clear_screen()
            show_menu()
        elif option_select.strip().lower() == "exit":
            clear_screen()
            if close_database():
                exit()
                
        elif 0 <= int(option_select)-1 < len(keys_list)-len(ignore_keys):
            if keys_list[int(option_select)-1] in list_fields:
                value_list = [item.strip() for item in asset[keys_list[int(option_select)-1]].split("--")]
                edit_list_data(value_list)
                asset[keys_list[int(option_select)-1]] = " -- ".join(value_list)

            elif keys_list[int(option_select)-1] in date_fields:
                date_data = asset[keys_list[int(option_select)-1]]
                print(f"{keys_list[int(option_select)-1]} current date: {date_data}")
                date_validation = False
                if date_data == "":
                    continue
                else:
                    while not date_validation:
                        date_data = input("Enter new date (YYYY-MM-DD)")
                        if not date_data:
                            break
                        else:
                            date_validation = validate_entry(date_data)
                        if not date_validation:
                            print("Invalid date format (YYYY-MM-DD).")
                    if date_data:
                        print(f"New date: {date_data}")
                        if input("Type cancel to reverse or press enter to save and continue: ").lower() == "cancel":
                            continue
                        else:
                            asset[keys_list[int(option_select)-1]] = date_data

            else:
                text_data = asset[keys_list[int(option_select)-1]]
                print(f"{keys_list[int(option_select)-1]} current data: {text_data}")
                text_data = input("New data (note: the old data will be deleted): ")
                if text_data == "":
                    continue
                else:
                    print(f"New data: {text_data}")
                    if input("Type cancel to reverse or press enter to save and continue: ").lower() == "cancel":
                        continue
                    else:
                        asset[keys_list[int(option_select)-1]] = text_data                        
        else:
            continue


def edit_list_data(notes_list):
    clear_screen()
    while True:
        option_number = 0
        print("\nCurrent notes:\n")
        for note in notes_list:
            option_number += 1
            print(f"{option_number})  {note}")
        option_number += 1
        print(f"{option_number})  <Add new note>")
        option_select = input("\nSelect note to replace or delete, or back to return to the edit screen: ")
        if option_select.strip() is None or option_select.strip() == "":
            continue
        elif option_select.lower() == "back":
            return notes_list
        elif int(option_select) > len(notes_list):
            new_note = input("New note: ")
            notes_list.append(new_note)
            continue
        elif 0 <= int(option_select)-1 < len(notes_list):
            print(f"Current note: {notes_list[int(option_select)-1]}")
            command_input = input("1) Replace note  2) Delete note  3) Cancel: ")
            if command_input == "1":
                new_note = input("New note: ")
                if input("The new note will replace the old one.  Press enter to continue or type cancel to cancel.:"):
                    continue
                else:
                    notes_list[int(option_select)-1] = new_note
                    continue
            elif command_input == "2":
                delete_input = input("Are you sure you want to delete this note? yes/no: ")
                if delete_input == "yes":
                    del notes_list[int(option_select)-1]
                elif delete_input == "no":
                    continue
        else:
            continue


def validate_entry(data, field_type):
    if field_type == "date":
        try:
            datetime.strptime(data, "%Y-%m-%d")
            return True
        except ValueError:
            return False


def output_limited_old(result_dictionary):
    print(f"Serial Number: {check_result_value(result_dictionary.get('Serial', 'keyMissing'))}")
    print(f"Model: {check_result_value(result_dictionary.get('Model', 'keyMissing'))}")
    print(f"Asset Number: {check_result_value(result_dictionary.get('Asset', 'keyMissing'))}")
    if result_dictionary["table"] in ["IT_Assets_FT", "IT_Assets_SG"]:
        print(f"Fork Truck: {check_result_value(result_dictionary.get('Fork_Truck_No', 'keyMissing'))}")
    print(f"IP Address: {check_result_value(result_dictionary.get('Ip_Address', 'keyMissing'))}")
    print(f"Notes: {check_result_value(result_dictionary.get('Current_User', 'keyMissing'))}")
    print(f"\nFound in table {result_dictionary['table']} under {result_dictionary['column']} as {result_dictionary.get(result_dictionary['column'], 'Error')}.")
    print("Migration Status: This device has not yet been migrated to the new tracking table.")


def output_limited_new(result_dictionary):
    print(f"Seral Number: {check_result_value(result_dictionary.get('serial', 'keyMissing'))}")
    print(f"Device Type: {check_result_value(result_dictionary.get('device_type', 'keyMissing'))}")
    print(f"Model: {check_result_value(result_dictionary.get('model', 'keyMissing'))}")
    print(f"Asset Number: {check_result_value(result_dictionary.get('asset_number', 'keyMissing'))}")
    if result_dictionary["device_type"].lower() in ["fork truck computer", "scanning gun"]:
        print(f"Fork Truck: {check_result_value(result_dictionary.get('fork_truck_number', 'keyMissing'))}")
    print(f"IP Address: {check_result_value(result_dictionary.get('Ip_Address', 'keyMissing'))}")
    print(f"Notes: {check_result_value(result_dictionary.get('notes', 'keyMissing'))}")
    print(f"\nFound in table {result_dictionary['table']} under {result_dictionary['column']} as {result_dictionary.get(result_dictionary['column'], 'Error')}.")


def output_full(result_dictionary):
    for key in result_dictionary:
        if key not in ["table", "column", "is_verified"]:
            print(f"{key}: {result_dictionary[key]}")


def check_result_value(value):
    if value == "keyMissing":
        return ""
    elif value == "" or value is None:
        return ""
    else:
        return str(value)


def check_migrations_duplicates(serial):
    results_old, results_new, number_migrated, number_duplicate = search(serial)
    
    if len(results_new) >= 2:
        print()
        print("!" * os.get_terminal_size().columns)
        print("Please send a message to the IT department with the following information.")
        print("Copy / Paste if possible.\n\n")
        print("Duplicate(s) has been detected in the new IT Assets table:")
        for dictionary in results_new:
            output_limited_new(dictionary)
            print("-" * os.get_terminal_size().columns)
            print()
        print("!" * os.get_terminal_size().columns)
        print()
        input("Press enter when you are ready to continue.")
    
    if len(results_old) == 0 and len(results_new) == 0:
        return False
    elif len(results_old) == 0 and len(results_new) == 1:
        selected_asset = results_new[0]
    elif len(results_old) == 1 and len(results_new) == 0:
        selected_asset = migrate_asset(results_old[0])
    elif len(results_old) >= 2 and len(results_new) == 0:
        selected_asset = process_duplicates(results_old + results_new)
        migrate_asset(selected_asset)
    else:
        selected_asset = process_duplicates(results_old + results_new)
        for dictionary in results_old:
            edit_field(dictionary, "is_migrated", 1)
    return selected_asset


def migrate_asset(asset_dictionary):
    return(asset_dictionary)


def process_duplicates(duplicates_list):
    migrated = False
    migrated_duplicates_list = []
    option_number = 0
    
    for dictionary in duplicates_list:
        if dictionary["table"] in config.new_tables:
            migrated = True
            migrated_duplicates_list.append(dictionary)
    
    if not migrated:
        for dictionary in duplicates_list:
            option_number += 1
            print(f"Option {option_number})\n")
            output_full(dictionary)
            print("-" * os.get_terminal_size().columns)
    else:
        for dictionary in migrated_duplicates_list:
            option_number += 1
            print(f"Option {option_number})\n")
            output_full(dictionary)
            print("-" * os.get_terminal_size().columns)
    print("=" * os.get_terminal_size().columns)
    
    option_select = int(input("Choose which entry to keep: "))
    if not migrated:
        for index, dictionary in enumerate(duplicates_list):
            if index == option_select - 1:
                continue
            else:
                edit_field(dictionary, "is_duplicate", 1)
        return duplicates_list[int(option_select)-1]
    else:
        for index, dictionary in enumerate(duplicates_list):
            if dictionary["table"] in config.new_tables:
                continue
            else:
                edit_field(dictionary, "is_duplicate", 1)
        return migrated_duplicates_list[int(option_select)-1]
    

def edit_field(asset_dictionary, field, value):
    asset_dictionary[field] = value
    if asset_dictionary["table"] in config.new_tables:
        match = "asset_number"
    else:
        match = "Asset"
    edit_database_test(asset_dictionary, field, match)


def test_method():
    pass


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
