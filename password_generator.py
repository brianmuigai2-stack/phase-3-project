# password_generator.py
import random
import string

class PasswordGenerator:
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length=12, use_uppercase=True, use_digits=True, use_symbols=True):
        """Generate a secure password with specified criteria"""
        chars = self.lowercase
        
        if use_uppercase:
            chars += self.uppercase
        if use_digits:
            chars += self.digits
        if use_symbols:
            chars += self.symbols
        
        # Ensure at least one character from each selected type
        password = [random.choice(self.lowercase)]
        
        if use_uppercase:
            password.append(random.choice(self.uppercase))
        if use_digits:
            password.append(random.choice(self.digits))
        if use_symbols:
            password.append(random.choice(self.symbols))
        
        # Fill remaining length with random characters
        for _ in range(length - len(password)):
            password.append(random.choice(chars))
        
        # Shuffle the password
        random.shuffle(password)
        return ''.join(password)
    
    def generate_multiple(self, count=5, length=12):
        """Generate multiple password options"""
        passwords = []
        for _ in range(count):
            passwords.append(self.generate_password(length))
        return passwords