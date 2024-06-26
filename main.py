from cs50 import SQL
from prettytable import PrettyTable
import sys
import os

if not "database.db" in os.listdir(os.getcwd()):
    open("database.db", "w").close()

# Initiating the database
db = SQL("sqlite:///database.db")

# Database is empty, if it contains table, no content in the table


def initialize_tables():
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS "history" (
                "user_id"       INTEGER NOT NULL,
                "medicine_id"   INTEGER NOT NULL,
                "quantity"      NUMERIC NOT NULL,
                "amount"        NUMERIC NOT NULL
        );
        
        """
    )
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS "users" (
                "user_id"       INTEGER NOT NULL UNIQUE,
                "first_name"    TEXT NOT NULL,
                "last_name"     TEXT NOT NULL,
                "cash"  NUMERIC NOT NULL,
                PRIMARY KEY("user_id" AUTOINCREMENT)
        );
        """
    )
    db.execute(
        """
        
        CREATE TABLE IF NOT EXISTS "medicines" (
                "medicine_id"   INTEGER NOT NULL UNIQUE,
                "name"  TEXT NOT NULL UNIQUE,
                "dosage"        NUMERIC NOT NULL,
                "price" NUMERIC NOT NULL,
                "quantity"      INTEGER NOT NULL,
                PRIMARY KEY("medicine_id" AUTOINCREMENT)
        );
        """
    )


def take_input_as_numeric(
    message: str = "Enter the number",
    error_message: str = "Please enter a valid number",
    negative_allowed: bool = False,
    decimal_allowed: bool = True,
    zero: bool = False,
):
    """
    Takes input from the user as integer
    Parameters:
    message (str) - The message to be displayed to the user
    error_message (str) - The error message to be displayed to the user
    negative_allowed (bool) - Whether negative numbers are allowed or not
    Returns:
    int - The integer entered by the user
    """

    # Running a while Loop
    while True:

        # Getting the input from the user while displaying the message
        userinput = input(message)

        # Try-except block
        try:

            # Try to convert to decimal
            decimal_value = float(userinput)

            # If zero is allowed and the decimal value is zero itself
            if zero and decimal_value == 0:

                # Return the decimal of the userinput
                return decimal_value

            # If the negative allowed is allowed
            if negative_allowed:

                # If the decimal is allowed
                if decimal_allowed:

                    # Return the decimal value
                    return decimal_value

                # If decimal value is not allowed
                else:

                    # If the decimal value is an integer
                    if decimal_value == int(decimal_value):

                        # Return the integer of the decimal value
                        return int(decimal_value)

                    # If the decimal value is an not integer
                    else:

                        # Print the error message
                        print(error_message)

                        # Print the input again
                        userinput = input(message)

            # If the negative allowed is not allowed
            else:

                # If decimal is allowed
                if decimal_allowed:

                    # Return the decimal value
                    return decimal_value

                # If decimal is not allowed
                else:

                    # If the decimal value is an integer
                    if decimal_value == int(decimal_value):

                        # Return an integral value of the decimal
                        return int(decimal_value)

                    # If decimal value is not an integer
                    else:

                        # Print an error message
                        print(error_message)

                        # Print the input again
                        userinput = input(message)

        # If the operation faces ValueError
        except ValueError:

            # Print the error message
            print(error_message)

            # Taking the input again
            userinput = input(message)


def input_in_options(
    message: str,
    options: list,
    error_message: str = "Invalid option",
):
    """
    Asks for the input from a given option
    If the userinput is not in the given options, it asks for the input again
    """

    # Running a while loop
    while True:

        # Getting the input from the user
        userinput = input(message)

        # If the lower case of the userinput is not in the list generated by lowercasing all the options of the given list
        if userinput.lower().strip() in [str(option).lower() for option in options]:

            # Return the userinput
            return userinput

        # Else
        else:

            # Print the error message
            print(error_message)

            # Ask for the input again
            userinput = input(message)


def take_input_as_string(
    message: str = "Enter your input: ", error_message: str = "Invalid input"
):
    """
    Taking input as string, the string might not be empty
    """

    # Running a while loop
    while True:

        # Taking the user input
        userinput = input(message)

        # If the userinput is None (length of the userinput is zero)
        if userinput is None:

            # Prining the error message
            print(error_message)

            # Asking for the user for the input again
            userinput = input(message)

        # If the userinput is not empty
        else:

            # Return the userinputs
            return userinput


def is_user_registered(user_id: int):
    """
    Checks if the user is registered.
    Returns True if the user is registered else False.
    """

    # Checking if the user is registered
    user_registrant = db.execute(
        """
        SELECT * FROM users
        WHERE user_id = ?
        """,
        user_id,
    )

    # If the length of the list returned is zero
    return len(user_registrant) == 1


def is_user_registered_name(first_name: str, last_name: str):
    """
    Checks if the user is registered.
    Returns True if the user is registered else False.
    """

    # Checking if the user is registered
    user_registrant = db.execute(
        """
        SELECT * FROM users
        WHERE first_name = ? AND
        last_name = ?
        """,
        first_name,
        last_name,
    )

    # If the length of the list returned is zero
    return len(user_registrant) == 1


def register_user(first_name: str, last_name: str):
    """
    Registers the user in the database,
    Returns the new user details if the user is registered else returns False.
    """

    # Checking if the user is in the database
    if not is_user_registered_name(first_name, last_name):

        # Inserting the user in the database
        new_user = db.execute(
            """
            INSERT INTO users
            (first_name, last_name, cash)
            VALUES
            (?, ?, ?)
            """,
            first_name,
            last_name,
            10000,
        )

        # Returing the user object
        return new_user

    # If the user is already registered
    else:
        return False


def get_user_details(user_id: int):
    """
    Returns the user details for the user id
    """

    # Returning the cash details
    user_details = db.execute(
        """
        SELECT * FROM users
        WHERE user_id = ?
        """,
        user_id,
    )

    # If the length of the output is one
    if len(user_details) == 1:

        # Return the user details
        return user_details[0]

    # If the length of the list is greater than 1
    elif len(user_details) > 1:

        # Return the error
        return "Multiple users"

    # If the length of the list is zero
    else:

        # Return the error
        return "No such users"


def add_cash(user_id: int, cash: float):
    """
    Adds cash to the user account and returns the user_id
    """

    # Updating the cash
    cash_added_user = db.execute(
        """
        UPDATE users
        SET cash = cash + ?
        WHERE user_id = ?
        """,
        cash,
        user_id,
    )

    # Returning the count of matched items
    return cash_added_user


def get_medicine_details(medicine_id: int):
    """
    Returns a dictionary containing the details of the medicine fetched by the medicine id provided
    Returns an error if the medicine id is not found in the database or more than one medicine with the same id found
    """

    # Querying the database
    medicine = db.execute(
        """
        SELECT * FROM medicines 
        WHERE medicine_id = ?
        """,
        medicine_id,
    )

    # If the list returned is only 1
    if len(medicine) == 1:

        # Return the medicine
        return medicine[0]

    # If the list is empty
    if len(medicine) == 0:

        # Return an error message
        return "No such medicine"

    # If the list contains elements more than one
    if len(medicine) > 1:

        # Return an error message
        return "More than one such medicine found"


def buy_medicine(user_id: int, medicine_id: int, user_cash: float, quantity: int):
    """
    Buys a medicine for the user with the specified user id, medicine id, user cash and quantity
    """

    # Getting the medicine details
    medicine = get_medicine_details(medicine_id)

    # If the function returns an error
    if medicine in ["No such medicine", "More than one such medicine found"]:

        # Return the error
        return "Error while fetching medicine details"

    # Fetching the price of the medicine
    price = medicine["price"]

    # Calculating the total amount by multiplying the price and the quantity
    total_amount = price * quantity

    # If the total amount to be paid is greater than the user's account balance
    if user_cash < total_amount:

        # Return an error
        return "Not sufficient cash"

    # Otherwise, update the user balance
    update_cash = db.execute(
        """
    UPDATE users
    SET cash = cash - ?
    WHERE user_id = ?
    """,
        total_amount,
        user_id,
    )

    if update_cash > 1:
        return "More than one user with the same User ID found"
    elif update_cash < 1:
        return "No such user"

    # Update the user's buy history
    update_history = db.execute(
        """
    INSERT INTO history
    (user_id, medicine_id, quantity, amount)
    VALUES
    (?, ?, ?, ?)
    """,
        user_id,
        medicine_id,
        quantity,
        total_amount,
    )

    # Returning a dictionary containing the total quantiy, price and total amount
    return {
        "total_quantity": quantity,
        "total_amount": total_amount,
        "price": price,
    }


def history():
    """
    Returns a PrettyTable list containing the history
    """
    # Creating a new PrettyTable
    p = PrettyTable()

    # Adding the required fields
    p.field_names = ["User ID", "Medicine ID", "Quantity", "Amount"]

    # Getting the history from the database
    history = db.execute(
        """
                    SELECT * FROM history
                    """
    )

    # For each log in the history
    for log in history:
        p.add_row(
            [
                log["user_id"],
                log["medicine_id"],
                log["quantity"],
                log["amount"],
            ]
        )

    return p


def add_medicine(name: str, quantity: int, price: float, dosage: int):
    """
    Adds a new medicine to the database
    """
    medicine_added = db.execute(
        """
        INSERT INTO medicines
        (name, quantity, price, dosage)
        VALUES
        (?, ?, ?, ?)
        """,
        name,
        quantity,
        price,
        dosage,
    )

    # Returns the medicine id of the newly added medicine
    return medicine_added


# Defining a dictionary to store the current user's details
current_user = {}


def main():
    """
    Main function
    """
    # Erasing all the previous user
    current_user = {}

    # Printing the welcome message with two new lines
    print("Welcome to Pharmacy!", end="\n\n")

    # Getting whether the person is an user or an admin
    user_or_admin = input_in_options(
        message="User (U) / Admin (A): ",
        options=["A", "U"],
    )

    if user_or_admin.upper().strip() == "A":
        # Getting the admin details
        username = take_input_as_string("Enter your username: ", "Invalid username")

        # If the username is not admin
        if username != "admin":

            # Printing an error message
            print("Invalid username!")

            # Returning
            return

        # If the username entered is 'admin'
        else:

            # Printing the welcome message
            print("\nWelcome, admin!")

            history_or_add = input_in_options(
                "Add Medicine (A) / History (H): ",
                ["A", "H"],
            )

            # If the user selects the history mode
            if history_or_add.upper().strip() == "H":

                # Running the history function
                print("\n", history())

                # Returing
                return

            elif history_or_add.upper().strip() == "A":

                # Getting the required parameters
                name = take_input_as_string("Enter the name: ", "Invalid name")

                # Checking if the medicine exists
                medicine_name_replica = db.execute(
                    """
                    SELECT name FROM medicines
                    WHERE name = ?""",
                    name,
                )

                # If the length of the output is zero
                if len(medicine_name_replica) != 0:

                    # Printing an error message
                    print("Medicine already exists")

                    # Returning the function
                    return

                # Fetching the quantity
                quantity = int(
                    take_input_as_numeric(
                        "Enter the tablets per strip: ",
                        "Invalid quantity",
                        decimal_allowed=False,
                    )
                )
                dosage = int(
                    take_input_as_numeric(
                        "Enter the dosage: ",
                        "Invalid dosage",
                        decimal_allowed=False,
                    )
                )
                price = int(
                    take_input_as_numeric(
                        "Enter the price: ",
                        "Invalid price",
                    )
                )

                # Officially adding the medicine
                new_medicine_id = add_medicine(name, quantity, price, dosage)

                print(
                    "\nNew medicine added with ID",
                    new_medicine_id,
                )

            else:

                # Printing an error message
                print("Invalid option!")

                # Returning
                return

    # If the person selects the User
    elif user_or_admin.upper().strip() == "U":

        # Ask the user for registering or logging in
        register_or_login = input_in_options(
            "Register (R) / Login (L): ",
            ["R", "L"],
        )

        # If the user wants to register
        if register_or_login.upper().strip() == "R":

            # Asking the user for first name
            first_name = take_input_as_string(
                "Enter the first name: ", "Invalid first name"
            )

            # Asking the user for last name
            last_name = take_input_as_string(
                "Enter the last name: ", "Invalid last name"
            )

            # Registering the user
            new_register = register_user(first_name, last_name)

            # If the function returns Fale
            if new_register is False:

                # Printing the message
                print("User already registered")

                # Returning
                return

            else:

                # Printing the user_id
                print("\nUser ID: ", new_register)

                # Printing the message
                print("User registered successfully")

                # Returning
                return

        # If the user wants to log in
        elif str(register_or_login).upper().strip() == "L":

            # Asking the user for user id
            log_in_user = take_input_as_numeric(
                "Enter your User ID: ", "Invalid User ID", decimal_allowed=False
            )

            # Checking if the user with the user id exists
            logged_user_registered = is_user_registered(log_in_user)

            # If the function returns False
            if logged_user_registered is False:

                # Printing an error message
                print("\nUser not registered")
                return

            # Setting the current user
            current_user = get_user_details(log_in_user)

            # Printing the welcome message
            print(
                "\nWelcome", current_user["first_name"], current_user["last_name"], "!"
            )

            # Asking the user if he wants to buy medicine or add cash
            add_or_buy = input_in_options(
                "Buy Medicine (M) / Add Cash (A): ",
                ["M", "A"],
            )

            # If the user wants to buy medicine
            if str(add_or_buy).upper().strip() == "M":

                # Fetching the medicine list
                raw_medicine_list = db.execute("SELECT * FROM medicines")

                # Generating a list of the available medicines
                medicines_in_stock = [
                    medicine["name"] for medicine in raw_medicine_list
                ]

                # Asking the user for the Medicine name and the quantity
                medicine_user_wants = take_input_as_string(
                    "Enter the name of medicine: "
                )

                # Modified medicine list containing the name in lower case
                modified_medicine_list = [
                    str(medicine_in_stock).lower()
                    for medicine_in_stock in medicines_in_stock
                ]

                # If the medicine user wants is in the available medicines
                if str(medicine_user_wants).lower() in modified_medicine_list:

                    # Getting the quantity
                    user_medicine_strips = take_input_as_numeric(
                        "Enter the number of strips: ",
                        "Invalid number of strips",
                        decimal_allowed=False,
                    )

                    # Getting the medicine id
                    user_medicine_id = raw_medicine_list[
                        modified_medicine_list.index(str(medicine_user_wants).lower())
                    ]["medicine_id"]

                    # Getting the output of the function to buy the medicines with the required parameters
                    buy_medicine_output = buy_medicine(
                        current_user["user_id"],
                        medicine_id=user_medicine_id,
                        user_cash=current_user["cash"],
                        quantity=user_medicine_strips,
                    )

                    # If the function returns a valid dictionary
                    if type(buy_medicine_output) == dict:

                        # Printing the success message
                        print("Bought medicine successfully")

                        # Subtract the total amount from the current user's cash
                        current_user["cash"] -= buy_medicine_output["total_amount"]

                        # Print the remaining cash
                        print("Current cash left (in Rupees):", current_user["cash"])

                        # Return the function
                        return

                    # If the function returns an error
                    else:

                        # Printing the error
                        print(buy_medicine_output)

                        # Returning the function
                        return

                # If the user entered an invalid name
                else:

                    # Printing an error message
                    print("Invalid medicine name")

                    # Returning the function
                    return

            # If the user wants to add cash
            elif str(add_or_buy).upper().strip() == "A":

                # Asking the user for the amount he wants to add
                cash_to_add = take_input_as_numeric(
                    "Enter the amount (in Rupees): ", "Invalid Amount"
                )

                # Adding the cash to the user account in the database
                add_cash(current_user["user_id"], cash_to_add)

                # Reflecting the change in the current user's dictionary
                current_user["cash"] += cash_to_add

                # Print the cash with the user
                print("Current cash (in Rupees):", current_user["cash"])

                # Returning the function
                return

            # If the user entered an option else than A or M
            else:

                # Printing the error message
                print("Invalid option")

                # Returning the function
                return

        # If the user entered neither R (for Registering) nor L (for Login)
        else:

            # Print an invalid option
            print("Invalid option")

            # Return an error
            return

    # If the user entered neither A (for Admin) nor U (for User)
    else:
        print("Invalid option")
        return

    # Returning the function
    return


if __name__ == "__main__":

    # Executing the main function in try-except block
    try:

        # Trying to create the table (if not exists)
        initialize_tables()

        # Try to run the program
        main()

    # If the user exits the program
    except KeyboardInterrupt:

        # Printing the message with an empty line
        print("You exited the program. \n")

    # Printing the thank you message
    print("\nThank you! Visit Again!")

    # Exiting the program
    sys.exit()
