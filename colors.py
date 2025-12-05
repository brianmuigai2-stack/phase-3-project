# colors.py
from colorama import init, Fore, Back, Style

# Initialize colorama for cross-platform support
init(autoreset=True)

class Colors:
    # Text colors
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    
    # Styles
    BRIGHT = Style.BRIGHT
    DIM = Style.DIM
    RESET = Style.RESET_ALL
    
    @staticmethod
    def success(text):
        return f"{Fore.GREEN}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def error(text):
        return f"{Fore.RED}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def warning(text):
        return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def info(text):
        return f"{Fore.CYAN}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def highlight(text):
        return f"{Fore.MAGENTA}{Style.BRIGHT}{text}{Style.RESET_ALL}"
    
    @staticmethod
    def strength_color(score):
        if score >= 80:
            return Fore.GREEN
        elif score >= 60:
            return Fore.YELLOW
        elif score >= 40:
            return Fore.MAGENTA
        else:
            return Fore.RED