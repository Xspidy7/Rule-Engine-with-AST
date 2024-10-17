from api import create_rule, combine_rules, evaluate_rule
import mysql.connector
import os  # Import os for environment variables

# Author: Ujjawal Pathak
# GitHub: https://github.com/Xspidy7

def establish_connection():
    """
    Establish a connection to the MySQL database.
    
    Returns:
        db: MySQL database connection object.
        cursor: Cursor object to execute queries.
    """
    try:
        db = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=os.getenv("DB_PASSWORD", "Chetan333!!##"),  # Use environment variable for sensitive info
            database="sys"
        )
        cursor = db.cursor()
        return db, cursor
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        exit(1)  # Exit if the connection fails

def main():
    # Establish a database connection
    db, cursor = establish_connection()

    # Test create_rule function
    rule_expression = '{"type": "operand", "value": 5}'
    rule_id = create_rule(rule_expression)
    print(f"Rule created with ID: {rule_id}")

    # Test combine_rules function
    combined_expression = combine_rules([rule_id])
    print(f"Combined rule expression: {combined_expression}")

    # Test evaluate_rule function
    user_data = {"value": 5}
    result = evaluate_rule(rule_id, user_data)
    print(f"Evaluation result: {result}")

    # Clean up: close the cursor and database connection
    cursor.close()
    db.close()

# Entry point of the script
if __name__ == "__main__":
    main()
