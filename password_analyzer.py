# password_analyzer.py
import re
from datetime import datetime

class PasswordAnalyzer:
    def __init__(self):
        self.common_passwords = [
            "password", "123456", "password123", "admin", "qwerty",
            "letmein", "welcome", "monkey", "dragon", "master"
        ]
    
    def analyze_password(self, password):
        """Comprehensive password analysis"""
        score = 0
        feedback = []
        
        # Length scoring
        length = len(password)
        if length >= 16:
            score += 35
            feedback.append("Excellent length (16+ characters)")
        elif length >= 12:
            score += 30
            feedback.append("Good length (12+ characters)")
        elif length >= 8:
            score += 20
            feedback.append("Adequate length (8+ characters)")
        else:
            feedback.append("Too short - use at least 8 characters")
        
        # Character variety
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_symbol = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password))
        
        variety_count = sum([has_lower, has_upper, has_digit, has_symbol])
        
        if variety_count == 4:
            score += 35
            feedback.append("Excellent character variety")
        elif variety_count == 3:
            score += 25
            feedback.append("Good character variety")
        elif variety_count == 2:
            score += 15
            feedback.append("Limited character variety")
        else:
            feedback.append("Poor character variety - mix letters, numbers, symbols")
        
        # Pattern detection
        if re.search(r'(.)\1{2,}', password):
            score -= 10
            feedback.append("Avoid repeating characters")
        
        if re.search(r'(012|123|234|345|456|567|678|789|890)', password):
            score -= 15
            feedback.append("Avoid sequential numbers")
        
        if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
            score -= 15
            feedback.append("Avoid sequential letters")
        
        # Common password check
        if password.lower() in self.common_passwords:
            score -= 30
            feedback.append("This is a commonly used password")
        
        # Dictionary word check (simplified)
        if len(password) > 4 and password.lower().isalpha():
            score -= 10
            feedback.append("Avoid using dictionary words")
        
        # Ensure score is within bounds
        score = max(0, min(100, score))
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
        elif score >= 60:
            strength = "Strong"
        elif score >= 40:
            strength = "Medium"
        elif score >= 20:
            strength = "Weak"
        else:
            strength = "Very Weak"
        
        return {
            'score': score,
            'strength': strength,
            'feedback': feedback,
            'length': length,
            'has_lower': has_lower,
            'has_upper': has_upper,
            'has_digit': has_digit,
            'has_symbol': has_symbol
        }
    
    def get_improvement_suggestions(self, analysis):
        """Get specific suggestions for password improvement"""
        suggestions = []
        
        if analysis['length'] < 8:
            suggestions.append("Increase length to at least 8 characters")
        elif analysis['length'] < 12:
            suggestions.append("Consider using 12+ characters for better security")
        
        if not analysis['has_upper']:
            suggestions.append("Add uppercase letters (A-Z)")
        if not analysis['has_lower']:
            suggestions.append("Add lowercase letters (a-z)")
        if not analysis['has_digit']:
            suggestions.append("Add numbers (0-9)")
        if not analysis['has_symbol']:
            suggestions.append("Add special characters (!@#$%^&*)")
        
        if analysis['score'] < 60:
            suggestions.append("Consider using a password generator for better security")
        
        return suggestions