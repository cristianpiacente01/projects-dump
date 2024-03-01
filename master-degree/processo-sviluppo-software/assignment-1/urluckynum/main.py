from app.argparser import create_parser     # Needed to create the arguments parser.
from app.db import create_connection        # Needed to create the MySQL connection.
from app.lucky import show_lucky_number     # Needed to execute the application.


# Main function.
def main():

    # Create the arguments parser.
    parser = create_parser()

    # Parse the arguments.
    args = parser.parse_args()

    # Create a MySQL connection.
    connection = create_connection(args)

    # Check if the connection was successful.
    if connection is None:
        return  # Connection failed.

    # Try to execute the application logic.
    try:
        show_lucky_number(connection, args.gitlab_user)
    finally:
        # Close the MySQL connection if it is still open.
        if connection.is_connected():
            connection.close()


# Check if the script is being run directly or imported as a module.
if __name__ == "__main__":
    # Run the main function if the script is being run directly.
    main()