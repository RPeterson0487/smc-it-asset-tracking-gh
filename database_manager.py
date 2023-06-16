"""Back end: This will be the access point for the database and tables."""

# Standard library imports.
import os

# Third party imports.
import mariadb

# Local application/library specific imports.

# Global Variables
_maria_database = None
"""Global variable: Database object."""
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
        host=host_name,
        user=database_username,
        passwd=database_password,
        database=database_name,
    )

    global _database_cursor
    _database_cursor = _maria_database.cursor(dictionary=True)


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
    Each result is passed to the _output_search_result function to be processed
    and sent back to the front end.

    Args:
        search_input: The term to search for in the tables' fields.
        
    Returns:
        A list of dictionaries mapping SQL columns to table row fields.
        example: 
        ({'Asset':'123456','IP':'1.1.1.1'},{'Asset':'7890','IP':'2.2.2.2'})

    """
    table_tuple = (
        "IT_Assets_DT",
        "IT_Assets_FT",
        "IT_Assets_LT",
        "IT_Assets_PR",
        "IT_Assets_SG",
        "IT_Assets_SV",
        "IT_Assets_SW",
        "IT_Assets_TB",
        "IT_Assets_TC",
        "IT_Assets",
        "IT_Assets_Test",
    )
    results = []

    if not search_input.strip():
        return "Empty Search"
    else:
        for table_index in table_tuple:
            column_list = []

            _database_cursor.execute("""
                SHOW COLUMNS
                FROM {table}
            """.format(table=table_index))

            table_row = _database_cursor.fetchone()
            while table_row is not None:
                column_list.append(table_row["Field"])
                table_row = _database_cursor.fetchone()

            for column_index in column_list:
                _database_cursor.execute("""
                    SELECT *
                    FROM {table}
                    WHERE {column}
                    LIKE '%{search}%'
                """.format(table=table_index, column=column_index, search=search_input))

                column_row = _database_cursor.fetchone()
                while column_row is not None:
                    column_row["table"] = table_index
                    column_row["column"] = column_index
                    results.append(column_row)
                    column_row = _database_cursor.fetchone()
        return results


if __name__ == "__main__":
    print("Whoops!  You've started this from the wrong module.")