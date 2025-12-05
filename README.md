# Password Security & Generator CLI - Phase 3 Project

**Created by: Brian Muigai**  

```
██████████████████████████████████████████████████████████████████████████████
█                                                                            █
█  ░██████╗░███████╗░█████╗░██╗░░░██╗██████╗░██╗████████╗██╗░░░██╗  ░█████╗░  █
█  ██╔════╝░██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝╚██╗░██╔╝  ██╔══██╗  █
█  ╚█████╗░░█████╗░░██║░░╚═╝██║░░░██║██████╔╝██║░░░██║░░░░╚████╔╝░  ██║░░██║  █
█  ░╚═══██╗░██╔══╝░░██║░░██╗██║░░░██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░  ██║░░██║  █
█  ██████╔╝░███████╗╚█████╔╝╚██████╔╝██║░░██║██║░░░██║░░░░░░██║░░░  ╚█████╔╝  █
█  ╚═════╝░░╚══════╝░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░╚════╝░  █
█                                                                            █
█  ░██████╗░██╗░░░██╗░█████╗░██████╗░██████╗░  ░██████╗░███████╗███╗░░██╗    █
█  ██╔════╝░██║░░░██║██╔══██╗██╔══██╗██╔══██╗  ██╔════╝░██╔════╝████╗░██║    █
█  ██║░░██╗░██║░░░██║███████║██████╔╝██║░░██║  ██║░░██╗░█████╗░░██╔██╗██║    █
█  ██║░░╚██╗██║░░░██║██╔══██║██╔══██╗██║░░██║  ██║░░╚██╗██╔══╝░░██║╚████║    █
█  ╚██████╔╝╚██████╔╝██║░░██║██║░░██║██████╔╝  ╚██████╔╝███████╗██║░╚███║    █
█  ░╚═════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝    █
█                                                                            █
█                    PASSWORD SECURITY & GENERATOR                     █
█                                                                            █
█                        Created by: Brian Muigai                      █
█                                                                            █
█  ┌─────────────────────────────────────────────────────────────────────┐  █
█  │  Advanced Password Analysis & Generation System              │  █
█  │  Multi-User Support with Breach Tracking                     │  █
█  │  Complete Statistics & History Dashboard                     │  █
█  └─────────────────────────────────────────────────────────────────────┘  █
█                                                                            █
██████████████████████████████████████████████████████████████████████████████
```

**A cutting-edge password security CLI application** built with Python OOP principles, featuring three interconnected database tables and a stunning ASCII interface design.

## Quick Start

```bash
pip install -r requirements.txt
python3 main.py
```

## Features

- **Password Analysis** - Comprehensive scoring (0-100) with detailed feedback
- **Secure Generation** - Customizable password creation with multiple options
- **User Management** - Multi-user support with session tracking
- **Breach Tracking** - Security breach management and password association
- **Statistics** - Complete history and analytics dashboard
- **Professional UI** - ASCII art interface with color-coded output

## Architecture & Phase 3 Compliance

### Database Design
**Three interconnected tables** with proper relationships:
- **Users** - Account management with cascade relationships
- **PasswordTests** - Analysis/generation history with foreign keys
- **Breaches** - Security tracking with many-to-many associations

### Object-Oriented Implementation
**8 Core Classes** demonstrating proper OOP principles:
- `User`, `PasswordTest`, `Breach` - Data models with SQLAlchemy ORM
- `PasswordService` - Business logic controller
- `PasswordAnalyzer`, `PasswordGenerator` - Specialized utilities
- `InteractiveCLI` - User interface management
- `ASCIILoader` - Animation utility

### Key Methods & Properties
**Aggregate Methods:**
- `User.test_count`, `User.generation_count`, `User.breach_count`
- `User.get_average_test_score()`, `User.get_latest_test()`
- `PasswordTest.is_strong`, `PasswordTest.strength_category`
- `Breach.affected_password_count`, `Breach.severity_level`

**Association Methods:**
- `PasswordService.get_user_stats()` - Comprehensive analytics
- `PasswordService.associate_password_with_breach()` - Many-to-many relationships
- `Breach.add_affected_password()` - Password association management

## Usage

### Password Analysis
Analyzes passwords based on length, character variety, pattern detection, and common password databases with detailed feedback and improvement suggestions.

### Password Generation
Creates secure passwords with customizable options for length, character types, and generates multiple options for selection.

### Breach Management
Track security breaches and associate them with affected passwords using many-to-many relationships for comprehensive security monitoring.

## Technical Details

### Database Schema
```sql
-- Core tables with relationships
users (id, username, password_hash)
password_tests (id, user_id, score, is_generated)
breaches (id, user_id, breach_name, severity)
breach_password_association (breach_id, password_test_id)  -- Many-to-many
```

### OOP Principles
- **Encapsulation** - Private methods and controlled access
- **Inheritance** - SQLAlchemy Base class inheritance  
- **Polymorphism** - Method overriding and property decorators
- **Abstraction** - Clean interfaces hiding complexity

### Interface Preview
```
What would you like to do?
--------------------------
1. Initialize Database
2. User Management
3. Test Password Strength
4. Generate Secure Password
5. Breach Management
6. View History & Stats
7. Exit
```

## Troubleshooting

### Common Issues

**"no such table" or "no such column" errors:**
- Delete the database file: `rm -f password_checker.db`
- Run the app and select "1. Initialize Database" first
- This recreates tables with the correct schema

**"DetachedInstanceError" when creating users:**
- This is a SQLAlchemy session issue that has been fixed
- If it occurs, restart the application

**Passwords showing as "Medium" instead of "Strong":**
- Fixed in latest version - generated passwords now score 70/100 (Strong)
- Use 16+ character passwords for best scores
- Avoid common patterns, repeated characters, or dictionary words

**Sample users not appearing:**
- Delete database file and reinitialize
- Sample users: alice/password123, bob/mypassword, charlie/strongpass456

**Login issues:**
- Authentication is now required - you need both username and password
- Create a new user if you don't have credentials
- Use sample user credentials listed above

### Database Reset
If you encounter persistent issues:
```bash
rm -f password_checker.db
python3 main.py
# Select "1. Initialize Database"
```

---

**Phase 3 Compliance**: ✅ Classes with proper OOP syntax | ✅ Object relationships with foreign keys | ✅ Aggregate and association methods

This project demonstrates mastery of Python OOP concepts, database relationships, and CLI design while providing a practical password security tool.