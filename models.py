# models.py
"""Database models for the password security application."""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from database import Base
import bcrypt

# Association table for many-to-many relationship between breaches and password_tests
breach_password_association = Table(
    'breach_password_association',
    Base.metadata,
    Column('breach_id', Integer, ForeignKey('breaches.id'), primary_key=True),
    Column('password_test_id', Integer, ForeignKey('password_tests.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

    password_tests = relationship("PasswordTest", back_populates="user", cascade="all, delete-orphan")
    breaches = relationship("Breach", back_populates="user", cascade="all, delete-orphan")

    @property
    def test_count(self):
        return len([t for t in self.password_tests if not t.is_generated])

    @property
    def generation_count(self):
        return len([t for t in self.password_tests if t.is_generated])

    @property
    def breach_count(self):
        return len(self.breaches)

    def get_average_test_score(self):
        if not self.password_tests:
            return 0
        return sum(test.score for test in self.password_tests) / len(self.password_tests)

    def get_latest_test(self):
        return self.password_tests[-1] if self.password_tests else None

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username})>"

class PasswordTest(Base):
    __tablename__ = "password_tests"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    is_generated = Column(Boolean, default=False)

    user = relationship("User", back_populates="password_tests")
    breaches = relationship("Breach", secondary=breach_password_association, back_populates="affected_passwords")

    @property
    def is_strong(self):
        return self.score >= 60

    @property
    def strength_category(self):
        if self.score >= 60:
            return "Strong"
        else:
            return "Weak"

    @property
    def breach_count(self):
        return len(self.breaches)

    def __repr__(self):
        return f"<PasswordTest(id={self.id}, score={self.score})>"

class Breach(Base):
    __tablename__ = "breaches"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    breach_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)  # "Low", "High"

    user = relationship("User", back_populates="breaches")
    affected_passwords = relationship("PasswordTest", secondary=breach_password_association, back_populates="breaches")

    @property
    def affected_password_count(self):
        return len(self.affected_passwords)

    @property
    def severity_level(self):
        return 2 if self.severity == "High" else 1

    def add_affected_password(self, password_test):
        if password_test not in self.affected_passwords:
            self.affected_passwords.append(password_test)

    def __repr__(self):
        return f"<Breach(id={self.id}, name={self.breach_name}, severity={self.severity})>"