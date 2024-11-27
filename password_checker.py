def check_password_strength(password):
    score = 0
    feedback = []
    
    # Check length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Password is too short. Use at least 8 characters.")
    
    # Check for uppercase
    if any(c.isupper() for c in password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")
    
    # Check for lowercase
    if any(c.islower() for c in password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")
    
    # Check for numbers
    if any(c.isdigit() for c in password):
        score += 1
    else:
        feedback.append("Add numbers.")
    
    # Check for special characters
    special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    if any(c in special_chars for c in password):
        score += 1
    else:
        feedback.append("Add special characters.")
        
    # Return results
    strength = {
        0: "Very Weak",
        1: "Weak",
        2: "Moderate",
        3: "Strong",
        4: "Very Strong",
        5: "Excellent"
    }
    
    return {
        "score": score,
        "strength": strength[score],
        "feedback": feedback
    }

# Example usage
def main():
    while True:
        password = input("Enter a password to check (or 'quit' to exit): ")
        if password.lower() == 'quit':
            break
            
        result = check_password_strength(password)
        print(f"\nStrength: {result['strength']} (Score: {result['score']}/5)")
        
        if result['feedback']:
            print("\nImprovement suggestions:")
            for suggestion in result['feedback']:
                print(f"- {suggestion}")
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()