# cli.py
from password_checker import PasswordService
from database import init_db
from ascii_art import show_welcome_banner, show_strength_meter
from colors import Colors
from utils import ASCIILoader
import time
from datetime import datetime

class InteractiveCLI:
    def __init__(self):
        self.service = PasswordService()
        self.running = True
        self.current_user = None
        
        # Menu definitions
        self.menus = {
            "main": ("What would you like to do?", [
                "Initialize Database", "User Management", "Test Password Strength",
                "Generate Secure Password", "Breach Management", "View History & Stats", "Exit"
            ]),
            "user": ("User Management", [
                "Create New User", "Login as User", "List All Users", "Back to Main Menu"
            ]),
            "test": ("Password Testing", [
                "Test a Password", "View Test History", "Find Weak Passwords", "Back to Main Menu"
            ]),
            "generate": ("Password Generation", [
                "Generate Single Password", "Generate Multiple Options", "View Generation History", "Back to Main Menu"
            ]),
            "breach": ("Breach Management", [
                "Report New Breach", "View My Breaches", "Associate Password with Breach", "Back to Main Menu"
            ]),
            "stats": ("History & Statistics", [
                "My Statistics", "Test History", "Generation History", "System Overview", "Back to Main Menu"
            ])
        }

    def show_menu(self, menu_key):
        """Display numbered menu and get user choice"""
        title, options = self.menus[menu_key]
        print(f"\n{Colors.CYAN}{title}{Colors.RESET}")
        print(Colors.BLUE + "-" * len(title) + Colors.RESET)
        
        for i, option in enumerate(options, 1):
            print(f"{Colors.YELLOW}{i}.{Colors.WHITE} {option}{Colors.RESET}")
        
        while True:
            try:
                choice = input(f"\n{Colors.GREEN}Enter your choice (1-{len(options)}): {Colors.RESET}")
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                else:
                    print(Colors.error(f"Please enter a number between 1 and {len(options)}"))
            except ValueError:
                print(Colors.error("Please enter a valid number"))
    
    def handle_error(self, e):
        """Centralized error handling"""
        print(Colors.error(f"Error: {e}"))
    
    def get_input(self, prompt, default=""):
        """Get user input with optional default"""
        value = input(f"{Colors.CYAN}{prompt}: {Colors.RESET}") or default
        return value if value else None

    def init_database(self):
        loader = ASCIILoader("Initializing database")
        loader.start()
        try:
            time.sleep(1)
            init_db()
            loader.stop()
            print(Colors.success("Database initialized successfully!"))
        except Exception as e:
            loader.stop()
            self.handle_error(e)

    def create_user(self):
        username = self.get_input("Enter username")
        if not username:
            return
        
        import getpass
        password = getpass.getpass(f"{Colors.CYAN}Enter password: {Colors.RESET}")
        if not password:
            return
        
        try:
            user = self.service.create_user(username, password)
            print(Colors.success(f"User created successfully: {username}"))
        except ValueError as e:
            self.handle_error(e)

    def login_user(self):
        username = self.get_input("Enter username")
        if not username:
            return
        
        import getpass
        password = getpass.getpass(f"{Colors.CYAN}Enter password: {Colors.RESET}")
        if not password:
            return
        
        try:
            user = self.service.authenticate_user(username, password)
            if not user:
                print(Colors.error("Invalid username or password"))
                return
            
            self.current_user = user
            print(Colors.success(f"Logged in as {username}"))
        except ValueError as e:
            self.handle_error(e)

    def list_users(self):
        try:
            users = self.service.get_all_users()
            if not users:
                print(Colors.warning("No users found"))
                return
            
            print(f"\n{Colors.CYAN}All Users:{Colors.RESET}")
            for user in users:
                print(f"{Colors.WHITE}{user.username} - Tests: {user.test_count}, Generated: {user.generation_count}, Breaches: {user.breach_count}{Colors.RESET}")
        except Exception as e:
            self.handle_error(e)

    def test_password(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        import getpass
        password = getpass.getpass(f"{Colors.MAGENTA}Enter password to test: {Colors.RESET}")
        if not password:
            return
        
        try:
            result = self.service.test_password(self.current_user.username, password)
            analysis = result['analysis']
            
            score_color = Colors.strength_color(analysis['score'])
            print(f"\n{Colors.CYAN}Password Analysis:{Colors.RESET}")
            print(f"Score: {score_color}{analysis['score']}/100 - {analysis['strength']}{Colors.RESET}")
            print(f"Strength Meter: {show_strength_meter(analysis['score'])}")
            print(f"Length: {analysis['length']} | Lower: {analysis['has_lower']} | Upper: {analysis['has_upper']} | Digits: {analysis['has_digit']} | Symbols: {analysis['has_symbol']}")
            
            if analysis['feedback']:
                print(f"\nFeedback: {', '.join(analysis['feedback'])}")
            if result['suggestions']:
                print(f"Suggestions: {', '.join(result['suggestions'])}")
                    
        except ValueError as e:
            self.handle_error(e)

    def generate_password(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        length = int(self.get_input("Password length (default 16)", "16"))
        use_uppercase = self.get_input("Include uppercase? (y/n, default y)", "y").lower() != 'n'
        use_digits = self.get_input("Include numbers? (y/n, default y)", "y").lower() != 'n'
        use_symbols = self.get_input("Include symbols? (y/n, default y)", "y").lower() != 'n'
        
        try:
            result = self.service.generate_password(
                self.current_user.username, length, use_uppercase, use_digits, use_symbols
            )
            
            analysis = result['analysis']
            score_color = Colors.strength_color(analysis['score'])
            print(f"\n{Colors.GREEN}Generated: {Colors.BRIGHT}{result['password']}{Colors.RESET}")
            print(f"Strength: {score_color}{analysis['strength']} ({analysis['score']}/100){Colors.RESET}")
            print(f"Meter: {show_strength_meter(analysis['score'])}")
            
        except ValueError as e:
            self.handle_error(e)

    def generate_multiple_passwords(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        count = int(self.get_input("How many passwords? (default 5)", "5"))
        length = int(self.get_input("Password length (default 16)", "16"))
        
        try:
            results = self.service.generate_multiple_passwords(self.current_user.username, count, length)
            
            print(f"\n{Colors.GREEN}Generated {count} Options:{Colors.RESET}")
            for i, result in enumerate(results, 1):
                analysis = result['analysis']
                score_color = Colors.strength_color(analysis['score'])
                print(f"{i}. {result['password']} - {score_color}{analysis['strength']} ({analysis['score']}/100){Colors.RESET}")
                
        except ValueError as e:
            self.handle_error(e)

    def create_breach(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        breach_name = self.get_input("Enter breach name")
        if not breach_name:
            return
        
        print("Severity levels: Low, High")
        severity = self.get_input("Enter severity", "Low")
        if severity not in ["Low", "High"]:
            severity = "Low"
        
        try:
            breach = self.service.create_breach(
                self.current_user.username, breach_name, datetime.now(), severity
            )
            print(Colors.success(f"Breach '{breach.breach_name}' created successfully"))
        except ValueError as e:
            self.handle_error(e)

    def view_user_breaches(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        try:
            breaches = self.service.get_user_breaches(self.current_user.username)
            if not breaches:
                print(Colors.warning("No breaches found"))
                return
            
            print(f"\n{Colors.RED}Security Breaches:{Colors.RESET}")
            for breach in breaches:
                severity_color = Colors.RED if breach.severity == "High" else Colors.YELLOW
                print(f"{breach.breach_name} - {severity_color}{breach.severity}{Colors.RESET} - Affected: {breach.affected_password_count}")
        except ValueError as e:
            self.handle_error(e)

    def view_test_history(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        try:
            tests = self.service.get_test_history(self.current_user.username)
            if not tests:
                print(Colors.warning("No test history found"))
                return
            
            print(f"\n{Colors.CYAN}Test History:{Colors.RESET}")
            for test in tests:
                score_color = Colors.strength_color(test.score)
                print(f"Test ID {test.id} - {score_color}{test.score}/100 {test.strength_category}{Colors.RESET} - Breaches: {test.breach_count}")
                
        except ValueError as e:
            self.handle_error(e)

    def view_generation_history(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        try:
            generations = self.service.get_generation_history(self.current_user.username)
            if not generations:
                print(Colors.warning("No generation history found"))
                return
            
            print(f"\n{Colors.CYAN}Generation History:{Colors.RESET}")
            for gen in generations:
                print(f"Test ID {gen.id} - Score: {gen.score}/100 - {gen.strength_category}")
                
        except ValueError as e:
            self.handle_error(e)

    def view_user_stats(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        try:
            stats = self.service.get_user_stats(self.current_user.username)
            avg_color = Colors.strength_color(stats['average_score'])
            
            print(f"\n{Colors.CYAN}Statistics for {stats['username']}:{Colors.RESET}")
            print(f"Tests: {stats['tests_performed']} | Generated: {stats['passwords_generated']} | Strong: {stats['strong_passwords']}")
            print(f"Average Score: {avg_color}{stats['average_score']}/100{Colors.RESET} | Breaches: {stats['breach_count']}")
            
        except ValueError as e:
            self.handle_error(e)

    def find_weak_passwords(self):
        threshold = int(self.get_input("Enter weakness threshold (default 40)", "40"))
        
        try:
            weak_tests = self.service.get_weak_tests(threshold)
            if not weak_tests:
                print(Colors.success(f"No passwords found below threshold {threshold}"))
                return
            
            print(f"\n{Colors.RED}Weak Passwords (< {threshold}):{Colors.RESET}")
            for test in weak_tests:
                print(f"User {test.user_id} - {Colors.RED}{test.score}/100 {test.strength_category}{Colors.RESET} - Test ID: {test.id}")
                
        except Exception as e:
            self.handle_error(e)

    def associate_password_with_breach(self):
        if not self.current_user:
            print(Colors.error("Please login first"))
            return
        
        try:
            breaches = self.service.get_user_breaches(self.current_user.username)
            tests = self.service.get_test_history(self.current_user.username)
            
            if not breaches or not tests:
                print(Colors.warning("Need both breaches and password tests to associate"))
                return
            
            print(f"\n{Colors.CYAN}Breaches:{Colors.RESET}")
            for i, breach in enumerate(breaches, 1):
                print(f"{i}. {breach.breach_name} ({breach.severity})")
            
            breach_idx = int(input("Select breach number: ")) - 1
            if breach_idx < 0 or breach_idx >= len(breaches):
                print(Colors.error("Invalid selection"))
                return
            
            print(f"\n{Colors.CYAN}Password Tests:{Colors.RESET}")
            for i, test in enumerate(tests[:10], 1):
                test_type = "Generated" if test.is_generated else "Tested"
                print(f"{i}. {test_type} - {test.score}/100 (ID: {test.id})")
            
            test_idx = int(input("Select test number: ")) - 1
            if test_idx < 0 or test_idx >= len(tests[:10]):
                print(Colors.error("Invalid selection"))
                return
            
            self.service.associate_password_with_breach(breaches[breach_idx].id, tests[test_idx].id)
            print(Colors.success(f"Associated with breach '{breaches[breach_idx].breach_name}'"))
            
        except (ValueError, IndexError) as e:
            self.handle_error(e)

    def system_overview(self):
        try:
            users = self.service.get_all_users()
            weak_tests = self.service.get_weak_tests(40)
            all_breaches = self.service.get_all_breaches()
            
            total_tests = sum(user.test_count for user in users)
            total_generations = sum(user.generation_count for user in users)
            
            print(f"\n{Colors.CYAN}System Overview:{Colors.RESET}")
            print(f"Users: {len(users)} | Tests: {total_tests} | Generated: {total_generations}")
            print(f"Weak Tests: {Colors.RED}{len(weak_tests)}{Colors.RESET} | Breaches: {Colors.RED}{len(all_breaches)}{Colors.RESET}")
            
        except Exception as e:
            self.handle_error(e)

    def run(self):
        show_welcome_banner()
        
        # Menu action mappings
        actions = {
            "user": {
                "Create New User": self.create_user,
                "Login as User": self.login_user,
                "List All Users": self.list_users
            },
            "test": {
                "Test a Password": self.test_password,
                "View Test History": self.view_test_history,
                "Find Weak Passwords": self.find_weak_passwords
            },
            "generate": {
                "Generate Single Password": self.generate_password,
                "Generate Multiple Options": self.generate_multiple_passwords,
                "View Generation History": self.view_generation_history
            },
            "breach": {
                "Report New Breach": self.create_breach,
                "View My Breaches": self.view_user_breaches,
                "Associate Password with Breach": self.associate_password_with_breach
            },
            "stats": {
                "My Statistics": self.view_user_stats,
                "Test History": self.view_test_history,
                "Generation History": self.view_generation_history,
                "System Overview": self.system_overview
            }
        }
        
        while self.running:
            print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
            if self.current_user:
                print(Colors.info(f"Logged in as: {self.current_user.username}"))
            
            choice = self.show_menu("main")
            
            if choice == "Initialize Database":
                self.init_database()
            elif choice == "Exit":
                self.running = False
                print(Colors.success("Goodbye!"))
            else:
                # Handle submenu navigation
                menu_map = {
                    "User Management": "user",
                    "Test Password Strength": "test", 
                    "Generate Secure Password": "generate",
                    "Breach Management": "breach",
                    "View History & Stats": "stats"
                }
                
                if choice in menu_map:
                    menu_key = menu_map[choice]
                    while True:
                        sub_choice = self.show_menu(menu_key)
                        if sub_choice == "Back to Main Menu":
                            break
                        elif sub_choice in actions[menu_key]:
                            actions[menu_key][sub_choice]()

if __name__ == "__main__":
    cli = InteractiveCLI()
    cli.run()