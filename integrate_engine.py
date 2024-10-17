from rule_api import create_rule, combine_rules, evaluate_rule

# Author: Ujjawal Pathak
# GitHub: https://github.com/Xspidy7

def main():
    """
    Main function to demonstrate the rule engine functionality.
    This creates rules, combines them, and evaluates against user data.
    """

    # Create a new rule for age
    rule_id = create_rule('{"type": "operand", "value": {"attribute": "age", "operator": ">", "value": 18}}')

    # Create another rule for income
    rule_id2 = create_rule('{"type": "operand", "value": {"attribute": "income", "operator": ">", "value": 50000}}')

    # Combine the rules
    combined_rule_expression = combine_rules([rule_id, rule_id2])

    # Evaluate the combined rule against user data
    user_data = {"age": 25, "country": "USA", "income": 60000}
    result = evaluate_rule(combined_rule_expression, user_data)

    # Output the evaluation result
    if result:
        print("The user satisfies the rule.")
    else:
        print("The user does not satisfy the rule.")

# Entry point of the script
if __name__ == "__main__":
    main()
