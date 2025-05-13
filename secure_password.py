import re

def is_secure_password(password):
    """Checks if a password is secure based on length, case, and digits (no special character required)."""
    
    # Minimum 8 characters
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # At least one uppercase letter
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter"
    
    # At least one lowercase letter
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter"
    
    # At least one digit
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is secure"

# Example usage: