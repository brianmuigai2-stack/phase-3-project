# password_checker.py
import bcrypt
from database import SessionLocal
from models import User, PasswordTest, Breach
from password_analyzer import PasswordAnalyzer
from password_generator import PasswordGenerator
from utils import with_loading
from sqlalchemy.orm import joinedload
import json
from datetime import datetime

class PasswordService:
    def __init__(self):
        self.analyzer = PasswordAnalyzer()
        self.generator = PasswordGenerator()

    # User management
    @with_loading("Creating user")
    def create_user(self, username: str, password: str) -> User:
        session = SessionLocal()
        try:
            exists = session.query(User).filter(User.username == username).first()
            if exists:
                raise ValueError(f"User '{username}' already exists")
            user = User(username=username)
            user.set_password(password)
            session.add(user)
            session.commit()
            session.refresh(user)
            
            # Add sample breach for new user
            sample_breach = Breach(user_id=user.id, breach_name="New User Security Check", severity="Low")
            session.add(sample_breach)
            session.commit()
            
            return user
        finally:
            session.close()

    def authenticate_user(self, username: str, password: str):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if user and user.check_password(password):
                return user
            return None
        finally:
            session.close()
    
    def get_user(self, username: str):
        session = SessionLocal()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()

    def get_all_users(self):
        session = SessionLocal()
        try:
            users = session.query(User).options(
                joinedload(User.password_tests),
                joinedload(User.breaches)
            ).all()
            for user in users:
                session.expunge(user)
            return users
        finally:
            session.close()

    # Password testing
    @with_loading("Analyzing password")
    def test_password(self, username: str, password: str) -> dict:
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            
            # Analyze password
            analysis = self.analyzer.analyze_password(password)
            
            # Store test result
            test = PasswordTest(
                user_id=user.id,
                score=analysis['score'],
                is_generated=False
            )
            session.add(test)
            session.commit()
            session.refresh(test)
            
            return {
                'test_id': test.id,
                'analysis': analysis,
                'suggestions': self.analyzer.get_improvement_suggestions(analysis)
            }
        finally:
            session.close()

    def get_test_history(self, username: str):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            tests = session.query(PasswordTest).options(
                joinedload(PasswordTest.breaches)
            ).filter(PasswordTest.user_id == user.id).all()
            
            # Detach from session to avoid lazy loading issues
            for test in tests:
                session.expunge(test)
            return tests
        finally:
            session.close()

    # Password generation
    @with_loading("Generating secure password")
    def generate_password(self, username: str, length=12, use_uppercase=True, use_digits=True, use_symbols=True):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            
            # Generate password
            password = self.generator.generate_password(length, use_uppercase, use_digits, use_symbols)
            analysis = self.analyzer.analyze_password(password)
            
            # Store generation record as a password test
            test = PasswordTest(
                user_id=user.id,
                score=analysis['score'],
                is_generated=True
            )
            session.add(test)
            session.commit()
            
            return {
                'password': password,
                'analysis': analysis,
                'test_id': test.id
            }
        finally:
            session.close()

    def generate_multiple_passwords(self, username: str, count=5, length=12):
        passwords = []
        for _ in range(count):
            result = self.generate_password(username, length)
            passwords.append(result)
        return passwords

    def get_generation_history(self, username: str):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            return session.query(PasswordTest).filter(
                PasswordTest.user_id == user.id,
                PasswordTest.is_generated == True
            ).all()
        finally:
            session.close()

    # Breach management
    @with_loading("Creating breach record")
    def create_breach(self, username: str, breach_name: str, breach_date: datetime, severity: str, description: str = None):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            
            breach = Breach(
                user_id=user.id,
                breach_name=breach_name,
                severity=severity
            )
            session.add(breach)
            session.commit()
            session.refresh(breach)
            return breach
        finally:
            session.close()

    def get_user_breaches(self, username: str):
        session = SessionLocal()
        try:
            user = session.query(User).filter(User.username == username).first()
            if not user:
                raise ValueError(f"User '{username}' not found")
            breaches = session.query(Breach).options(
                joinedload(Breach.affected_passwords)
            ).filter(Breach.user_id == user.id).all()
            
            # Detach from session to avoid lazy loading issues
            for breach in breaches:
                session.expunge(breach)
            return breaches
        finally:
            session.close()

    @with_loading("Associating password with breach")
    def associate_password_with_breach(self, breach_id: int, password_test_id: int):
        session = SessionLocal()
        try:
            breach = session.query(Breach).filter(Breach.id == breach_id).first()
            password_test = session.query(PasswordTest).filter(PasswordTest.id == password_test_id).first()
            
            if not breach:
                raise ValueError(f"Breach {breach_id} not found")
            if not password_test:
                raise ValueError(f"Password test {password_test_id} not found")
            
            breach.add_affected_password(password_test)
            session.commit()
            return breach
        finally:
            session.close()

    def get_breach_affected_passwords(self, breach_id: int):
        session = SessionLocal()
        try:
            breach = session.query(Breach).options(
                joinedload(Breach.affected_passwords)
            ).filter(Breach.id == breach_id).first()
            
            if not breach:
                raise ValueError(f"Breach {breach_id} not found")
            
            return breach.affected_passwords
        finally:
            session.close()

    # Statistics and analytics
    def get_user_stats(self, username: str):
        session = SessionLocal()
        try:
            user = session.query(User).options(
                joinedload(User.password_tests),
                joinedload(User.breaches)
            ).filter(User.username == username).first()
            
            if not user:
                raise ValueError(f"User '{username}' not found")
            
            avg_score = user.get_average_test_score()
            strong_passwords = len([t for t in user.password_tests if t.is_strong])
            generated_count = len([t for t in user.password_tests if t.is_generated])
            tested_count = len([t for t in user.password_tests if not t.is_generated])
            
            return {
                'username': user.username,
                'tests_performed': tested_count,
                'passwords_generated': generated_count,
                'average_score': round(avg_score, 2),
                'strong_passwords': strong_passwords,
                'breach_count': user.breach_count,
                'total_breaches': len(user.breaches)
            }
        finally:
            session.close()

    def get_weak_tests(self, threshold=40):
        session = SessionLocal()
        try:
            return session.query(PasswordTest).filter(PasswordTest.score < threshold).all()
        finally:
            session.close()

    def get_all_breaches(self):
        session = SessionLocal()
        try:
            breaches = session.query(Breach).options(
                joinedload(Breach.affected_passwords)
            ).all()
            
            # Detach from session to avoid lazy loading issues
            for breach in breaches:
                session.expunge(breach)
            return breaches
        finally:
            session.close()