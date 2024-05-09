import re

def validate_email_and_password(email, password):
    if not email or not password:
        return "Email and password are required"

    # Check if the email is in a valid format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid email format"

    # Add more password validation checks as needed
    # For example, you can check if the password meets certain criteria (e.g., length requirements)

    return True


def validate_user(email, password):
    if not email or not password:
        return "Email and password are required"
    # Add more validation checks as needed
    # For example, you can check if the email is in a valid format
    # or if the password meets certain criteria
    return True

def validate_book(title, author, category, user_id):
    if not title or not author or not category or not user_id:
        return "All fields (title, author, category, user_id) are required"

    # Add additional validation checks as needed
    # For example, you might want to check if the user_id is a valid user in your system
    # or if the category is from an allowed list of categories

    return True