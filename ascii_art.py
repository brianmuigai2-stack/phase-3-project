# ascii_art.py
from colors import Colors

def show_welcome_banner():
    """Display ASCII art welcome banner with colors"""
    banner = f"""
{Colors.CYAN}████████████████████████████████████████████████████████████████████████████████
█                                                                            █
█  {Colors.BLUE}░██████╗░██████╗░█████╗░██╗░░░██╗██████╗░██╗██████████╗██╗░░░██╗  ░█████╗░{Colors.CYAN}  █
█  {Colors.BLUE}██╔════╝░██╔════╝██╔══██╗██║░░░██║██╔══██╗██║╚══██╔══╝╚██╗░██╔╝  ██╔══██╗{Colors.CYAN}  █
█  {Colors.BLUE}╚█████╗░░█████╗░░██║░░╚═╝██║░░░██║██████╔╝██║░░░██║░░░░╚████╔╝░  ██║░░██║{Colors.CYAN}  █
█  {Colors.BLUE}░╚═══██╗░██╔══╝░░██║░░██╗██║░░░██║██╔══██╗██║░░░██║░░░░░╚██╔╝░░  ██║░░██║{Colors.CYAN}  █
█  {Colors.BLUE}██████╔╝░███████╗╚█████╔╝╚██████╔╝██║░░██║██║░░░██║░░░░░░██║░░░  ╚█████╔╝{Colors.CYAN}  █
█  {Colors.BLUE}╚═════╝░░╚══════╝░╚════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░░╚═╝░░░░░░╚═╝░░░  ░╚════╝░{Colors.CYAN}  █
█                                                                            █
█  {Colors.MAGENTA}░██████╗░██╗░░░██╗░████╗░██████╗░██████╗░  ░██████╗░███████╗███╗░░██╗{Colors.CYAN}    █
█  {Colors.MAGENTA}██╔════╝░██║░░░██║██╔══██╗██╔══██╗██╔══██╗  ██╔════╝░██╔════╝████╗░██║{Colors.CYAN}    █
█  {Colors.MAGENTA}██║░░██╗░██║░░░██║███████║██████╔╝██║░░██║  ██║░░██╗░█████╗░░██╔██╗██║{Colors.CYAN}    █
█  {Colors.MAGENTA}██║░░╚██╗██║░░░██║██╔══██║██╔══██╗██║░░██║  ██║░░╚██╗██╔══╝░░██║╚████║{Colors.CYAN}    █
█  {Colors.MAGENTA}╚██████╔╝╚██████╔╝██║░░██║██║░░██║██████╔╝  ╚██████╔╝███████╗██║░╚███║{Colors.CYAN}    █
█  {Colors.MAGENTA}░╚═════╝░░╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝{Colors.CYAN}    █
█                                                                            █
█                    {Colors.YELLOW}PASSWORD SECURITY & GENERATOR{Colors.CYAN}                     █
█                                                                            █
█                        {Colors.GREEN}Created by: Brian Muigai{Colors.CYAN}                      █
█                                                                            █
█  {Colors.WHITE}┌─────────────────────────────────────────────────────────────────────────┐{Colors.CYAN}  █
█  {Colors.WHITE}│  Advanced Password Analysis & Generation System              │{Colors.CYAN}  █
█  {Colors.WHITE}│  Multi-User Support with Breach Tracking                     │{Colors.CYAN}  █
█  {Colors.WHITE}│  Complete Statistics & History Dashboard                     │{Colors.CYAN}  █
█  {Colors.WHITE}└─────────────────────────────────────────────────────────────────────────┘{Colors.CYAN}  █
█                                                                            █
████████████████████████████████████████████████████████████████████████████████{Colors.RESET}

{Colors.GREEN}Welcome to the Ultimate Password Security System!{Colors.RESET}
{Colors.CYAN}Created by: {Colors.BRIGHT}{Colors.GREEN}Brian Muigai{Colors.RESET}

{Colors.WHITE}Key Features:{Colors.RESET}
{Colors.CYAN}- Advanced password strength analysis with detailed scoring{Colors.RESET}
{Colors.CYAN}- Secure password generation with customizable options{Colors.RESET}  
{Colors.CYAN}- Multi-user support with comprehensive tracking{Colors.RESET}
{Colors.CYAN}- Complete statistics and breach management{Colors.RESET}

    """
    print(banner)

def show_strength_meter(score):
    """Display visual strength meter with colors"""
    bars = score // 10
    color = Colors.strength_color(score)
    
    # Choose fill character based on score
    if score >= 80:
        fill_char = "█"  # Solid for excellent
    elif score >= 60:
        fill_char = "▓"  # Dense for good
    elif score >= 40:
        fill_char = "▒"  # Medium for fair
    else:
        fill_char = "░"  # Light for poor
    
    meter = f"{Colors.WHITE}[{color}"
    
    for i in range(10):
        if i < bars:
            meter += fill_char
        else:
            meter += " "
    
    meter += f"{Colors.WHITE}] {color}{score}/100{Colors.RESET}"
    return meter