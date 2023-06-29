"""Back end: This will be the access point for the database and tables."""
# Need to set config file

# Standard library imports.

# Third party imports.
import mariadb

# Local application/library specific imports.
import config_it_asset_tracking as config

# Global Variables
_maria_database = None
"""Global variable: Database connection object."""
_database_cursor = None
"""Global variable: Database cursor object. """


def connect_database(host_name, database_name, database_username, database_password):
    """Establishes connection to MariaDB database and initializes the cursor.

    Connects to MariaDB database using database information (host and database
    name) and authentication information (username and password) passed from
    front end.  Also creates a single database cursor object for queries.
    Database and cursor objects are global variables for use by other functions.

    Args:
        host_name: Host name or IP of database server.
        database_name: Database name to use when connecting to server.
        database_username: Username used for authentication with server.
        database_password: Password used for authentication with server.
    """
    global _maria_database
    _maria_database = mariadb.connect(
        host = host_name,
        user = database_username,
        passwd = database_password,
        database = database_name,
    )

    global _database_cursor
    _database_cursor = _maria_database.cursor(dictionary = True)


def close_database():
    """Closes connection to the database.

    Returns:
        True: At the moment, this is regardless of close status.  Will
            eventually return status to let front end know it's done.
    """
    print("Closing connection.\n\n")
    _database_cursor.close()
    _maria_database.close()
    return (True)


def search_database(search_input):
    """Searches through tables for search result in any field.

    Makes a list of all table columns in each table listed in the table_list
    list and searches through them for the search passed in from the front end.
    Each result is added to a dictionary to be passed back to the front end.

    Args:
        search_input: The term to search for in the tables' fields.
        
    Returns:
        A list of dictionaries mapping SQL columns to table row fields.
        example: 
        ({'Asset':'123456','IP':'1.1.1.1'},{'Asset':'7890','IP':'2.2.2.2'})

    """
    results = []
    results_count = 0

    if not search_input.strip():
        return "Empty Search"
    else:
        for table_index in config.search_tables:
            columns = _build_column_list(table_index)
            
            for column_index in columns:
                _database_cursor.execute(f"""
                    SELECT *
                    FROM {table_index}
                    WHERE {column_index}
                    LIKE '%{search_input}%'
                """)

                column_row = _database_cursor.fetchone()
                while column_row is not None:
                    column_row["table"] = table_index
                    column_row["column"] = column_index
                    if not _check_for_duplicates(column_row, results):
                        results.append(column_row)
                    column_row = _database_cursor.fetchone()
                    results_count += 1
        
        #print(f"(Backend dropped {results_count - len(results)})")
        return results


def edit_database_test(edit_dictionary, edit_field, edit_match):
    print(f"""\n
        UPDATE {edit_dictionary['table']}
        SET {edit_field} = {edit_dictionary[edit_field]}
        WHERE {edit_match} = {edit_dictionary[edit_match]}
    \n""")


def edit_database_single(edit_dictionary, edit_field, edit_match):
    _database_cursor.execute(f"""
        UPDATE {edit_dictionary['table']}
        SET {edit_field} = {edit_dictionary[edit_field]}
        WHERE {edit_match} = {edit_dictionary[edit_match]}
    """)
    
    _maria_database.commit()


def new_database_entry(new_entry):
    columns = ', '.join(new_entry.keys())
    values = ', '.join(['%s'] * len(new_entry))
    insert_query = f"""
        INSERT INTO {config.insert_table}
        ({columns})
        VALUES ({values})
    """
    
    for entry in new_entry.items():
        _database_cursor.execute(insert_query, entry)
    
    _maria_database.commit()


def _build_column_list(table):
    column_list = []
    
    _database_cursor.execute(f"""
                SHOW COLUMNS
                FROM {table}
            """)

    table_row = _database_cursor.fetchone()
    while table_row is not None:
        column_list.append(table_row["Field"])
        table_row = _database_cursor.fetchone()
        
    return column_list


def _check_for_duplicates(dictionary, dictionary_list):
    ignore_keys = ["column"]
    
    if not dictionary_list:
        return False
    else:
        for d in dictionary_list:
            duplicate = True
            for key in d:
                if key not in ignore_keys and d.get(key) != dictionary.get(key):
                    duplicate = False
                    break
            if duplicate:
                return True
        return False


if __name__ == "__main__":
    print("Whoops!  You've started this from the wrong module.")
