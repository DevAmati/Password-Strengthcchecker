import re
import hashlib
import os
from typing import Dict, List, Union
import json
from pathlib import Path

class PasswordStrengthChecker:
    def __init__(self):
        # Load common passwords and patterns
        self.common_passwords = self._load_common_passwords()
        self.keyboard_patterns = [
            'qwerty', 'asdfgh', '123456', 'zxcvbn',
            'qwertz', 'azerty'  # Different keyboard layouts
        ]
        
    def _load_common_passwords(self) -> set:
        # In a real project, you would load from a file
        return {
            'password123', 'admin123', '123456789', 'qwerty123',
            'letmein', 'welcome', 'monkey123', 'football', 'abc123'
        }
        
    def _check_length(self, password: str) -> tuple[int, List[str]]:
        score = 0
        feedback = []
        
        if len(password) >= 16:
            score += 3
        elif len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password is too short. Use at least 8 characters.")
            
        return score, feedback
        
    def _check_character_types(self, password: str) -> tuple[int, List[str]]:
        score = 0
        feedback = []
        
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
            
        return score, feedback
        
    def _check_patterns(self, password: str) -> tuple[int, List[str]]:
        score = 0
        feedback = []
        
        # Check for repeated characters
        if re.search(r'(.)\1{2,}', password):
            feedback.append("Avoid repeated characters (e.g., 'aaa').")
            score -= 1
            
        # Check for sequential numbers
        if re.search(r'(?:012|123|234|345|456|567|678|789)', password):
            feedback.append("Avoid sequential numbers.")
            score -= 1
            
        # Check for keyboard patterns
        lower_pass = password.lower()
        for pattern in self.keyboard_patterns:
            if pattern in lower_pass:
                feedback.append("Avoid keyboard patterns.")
                score -= 1
                break
                
        return score, feedback
        
    def _check_common_passwords(self, password: str) -> tuple[int, List[str]]:
        score = 0
        feedback = []
        
        # Hash the password for secure comparison
        hashed_pass = hashlib.sha256(password.encode()).hexdigest()
        
        if password.lower() in self.common_passwords:
            feedback.append("This is a commonly used password. Choose something unique.")
            score -= 2
            
        return score, feedback
        
    def _calculate_entropy(self, password: str) -> float:
        # Calculate password entropy (randomness)
        char_set_size = 0
        if any(c.isupper() for c in password): char_set_size += 26
        if any(c.islower() for c in password): char_set_size += 26
        if any(c.isdigit() for c in password): char_set_size += 10
        if any(not c.isalnum() for c in password): char_set_size += 32
        
        entropy = len(password) * (char_set_size.bit_length())
        return entropy
        
    def check_password(self, password: str) -> Dict[str, Union[int, str, List[str]]]:
        total_score = 0
        all_feedback = []
        
        # Run all checks
        length_score, length_feedback = self._check_length(password)
        char_score, char_feedback = self._check_character_types(password)
        pattern_score, pattern_feedback = self._check_patterns(password)
        common_score, common_feedback = self._check_common_passwords(password)
        
        # Combine scores and feedback
        total_score = length_score + char_score + pattern_score + common_score
        all_feedback.extend(length_feedback + char_feedback + pattern_feedback + common_feedback)
        
        # Calculate entropy bonus
        entropy = self._calculate_entropy(password)
        if entropy > 75:
            total_score += 1
            
        # Ensure score stays within bounds
        total_score = max(0, min(10, total_score))
        
        # Generate strength rating
        strength = {
            0: "Very Weak",
            1: "Very Weak",
            2: "Weak",
            3: "Weak",
            4: "Moderate",
            5: "Moderate",
            6: "Strong",
            7: "Strong",
            8: "Very Strong",
            9: "Very Strong",
            10: "Excellent"
        }[total_score]
        
        return {
            "score": total_score,
            "strength": strength,
            "feedback": all_feedback,
            "entropy": entropy
        }

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_strength_meter(score: int, max_score: int = 10):
    meter_width = 40
    filled = int((score / max_score) * meter_width)
    
    # Color codes
    colors = {
        'red': '\033[91m',
        'yellow': '\033[93m',
        'green': '\033[92m',
        'end': '\033[0m'
    }
    
    # Choose color based on score
    if score < 4:
        color = colors['red']
    elif score < 7:
        color = colors['yellow']
    else:
        color = colors['green']
        
    meter = f"{color}{'█' * filled}{'░' * (meter_width - filled)}{colors['end']}"
    return meter

def main():
    checker = PasswordStrengthChecker()
    
    while True:
        clear_screen()
        print("=== Password Strength Checker ===")
        print("\nEnter a password to check (or 'quit' to exit)")
        password = input("Password: ")
        
        if password.lower() == 'quit':
            break
            
        result = checker.check_password(password)
        
        clear_screen()
        print("\n=== Results ===")
        print(f"\nStrength: {result['strength']} (Score: {result['score']}/10)")
        print(f"Entropy: {result['entropy']:.2f} bits")
        print("\nStrength Meter:")
        print(display_strength_meter(result['score']))
        
        if result['feedback']:
            print("\nImprovement suggestions:")
            for suggestion in result['feedback']:
                print(f"• {suggestion}")
                
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")