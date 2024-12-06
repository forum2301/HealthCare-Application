import mysql.connector  # Import the MySQL Connector library for connecting and interacting with a MySQL database

def get_connection():
    """
    Establishes and returns a connection to the MySQL database.
    This function uses the `mysql.connector.connect` method to establish a connection
    with the database using specific credentials and database information.
    
    Returns:
        mysql.connector.connection_cext.CMySQLConnection: A connection object for interacting with the MySQL database.
    """
    return mysql.connector.connect(  # Create and return a connection object
        host="localhost",     # Hostname or IP address of the MySQL server (use "localhost" for local setup)
        user="forum",         # Username with permissions to access the database (replace with your MySQL user)
        password="Mumbai@123",  # Password associated with the provided username (replace with your MySQL password)
        database="healthcare"  # Name of the database to connect to (ensure this database exists on the server)
    )
