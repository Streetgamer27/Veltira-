#!/usr/bin/env python3
"""CyberForge - Advanced Hacking Dashboard with Enhanced Error Handling"""
import os
import sys
import time
import subprocess
import requests
import json
import threading
import signal
import logging
from typing import Optional, Dict, List
import hashlib
import base64
import random

# Setup Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[logging.FileHandler('cyberforge.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

try:
    import speech_recognition as sr
    import pyttsx3
    import openai
    from colorama import Fore, Back, Style, init
    from rich.console import Console
    from rich.table import Table
    from pyfiglet import Figlet
except ImportError as e:
    logger.error(f"Missing dependency: {e}")
    sys.exit(1)

init(autoreset=True)
console = Console()

# Initialize Audio Systems
try:
    recognizer = sr.Recognizer()
    tts_engine = pyttsx3.init()
    AUDIO_AVAILABLE = True
except:
    recognizer = None
    tts_engine = None
    AUDIO_AVAILABLE = False

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE")
if OPENAI_API_KEY != "YOUR_OPENAI_API_KEY_HERE":
    openai.api_key = OPENAI_API_KEY

class CyberForge:
    def __init__(self):
        self.current_user = None
        self.is_voice_active = False
        self.running_tools = {}
        self.github_repos = []
        self.session_log = []
        signal.signal(signal.SIGINT, self._handle_interrupt)
        signal.signal(signal.SIGTERM, self._handle_interrupt)
        logger.info("CyberForge initialized")
    
    def _handle_interrupt(self, sig, frame):
        logger.info("Interrupt received")
        print(f"\n{Fore.RED}[!] Shutting down...{Style.RESET_ALL}")
        if AUDIO_AVAILABLE and tts_engine:
            try:
                self.speak("Goodbye!")
            except:
                pass
        sys.exit(0)
    
    def clear_screen(self):
        try:
            os.system('clear' if os.name == 'posix' else 'cls')
        except Exception as e:
            logger.warning(f"Clear screen error: {e}")
    
    def type_effect(self, text, delay=0.03):
        try:
            for char in text:
                print(char, end='', flush=True)
                time.sleep(delay)
            print()
        except Exception as e:
            logger.error(f"Type effect error: {e}")
            print(text)
    
    def matrix_effect(self, duration=3):
        try:
            subprocess.run(['cmatrix', '-u', '3', '-C', 'green'], timeout=duration, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        except:
            pass
    
    def speak(self, text):
        if not AUDIO_AVAILABLE or not tts_engine:
            return
        try:
            tts_engine.say(text)
            tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"TTS error: {e}")
    
    def listen(self, timeout=5):
        if not AUDIO_AVAILABLE or not recognizer:
            return ""
        try:
            with sr.Microphone() as source:
                print(f"{Fore.CYAN}[AI]{Style.RESET_ALL} Listening...")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=timeout)
                command = recognizer.recognize_google(audio).lower()
                logger.info(f"Voice: {command}")
                return command
        except:
            return ""
    
    def ai_chat(self, message):
        if OPENAI_API_KEY == "YOUR_OPENAI_API_KEY_HERE":
            return "AI Error: API key not set"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are CyberForge AI, a hacking assistant. Be cool and technical."},
                    {"role": "user", "content": message}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"AI error: {e}")
            return f"AI error: {str(e)}"
    
    def login_system(self):
        self.clear_screen()
        try:
            f = Figlet(font='slant')
            print(Fore.RED + f.renderText('CYBERFORGE'))
        except:
            print(Fore.RED + "=== CYBERFORGE ===")
        
        print(Fore.GREEN + "Advanced Hacking Dashboard\n")
        users = {
            "admin": hashlib.sha256("cyberforge".encode()).hexdigest(),
            "hacker": hashlib.sha256("password123".encode()).hexdigest(),
            "root": hashlib.sha256("toor".encode()).hexdigest()
        }
        
        print(f"{Fore.YELLOW}Users: admin(cyberforge) | hacker(password123) | root(toor)")
        try:
            username = input(f"{Fore.CYAN}Username: {Style.RESET_ALL}").strip()
            password = input(f"{Fore.RED}Password: {Style.RESET_ALL}").strip()
            
            if not username or not password:
                logger.warning("Empty credentials")
                print(f"{Fore.RED}[!] Empty credentials!")
                time.sleep(2)
                return False
            
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            if username in users and users[username] == password_hash:
                self.current_user = username
                logger.info(f"Login: {username}")
                self.startup_animation()
                return True
            else:
                logger.warning(f"Failed login: {username}")
                print(f"{Fore.RED}Access Denied!")
                time.sleep(2)
                return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False
    
    def startup_animation(self):
        self.clear_screen()
        try:
            self.matrix_effect(2)
        except:
            pass
        self.clear_screen()
        
        for font in ["cyberforge", "hacking", "matrix", "doom", "ogre"]:
            try:
                f = Figlet(font=font)
                print(Fore.GREEN + f.renderText('CYBERFORGE'))
                time.sleep(1)
                self.clear_screen()
            except:
                continue
        
        try:
            print(Fore.RED + Figlet(font='slant').renderText('CYBERFORGE'))
        except:
            print(Fore.RED + "CYBERFORGE")
        
        print(f"{Fore.YELLOW}[{Fore.GREEN}✓{Fore.YELLOW}] Welcome back, {self.current_user.upper()}!")
        print(f"{Fore.CYAN}[{Fore.GREEN}✓{Fore.CYAN}] AI Assistant Online")
        print(f"{Fore.MAGENTA}[{Fore.GREEN}✓{Fore.MAGENTA}] Live Dashboard Active\n")
        self.speak(f"Welcome back {self.current_user}")
        logger.info("Startup animation completed")
    
    def run_command(self, cmd, timeout=30):
        try:
            logger.warning(f"Shell: {cmd[:50]}...")
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, check=False)
            return result.stdout + result.stderr
        except subprocess.TimeoutExpired:
            error = f"Timeout after {timeout}s"
            logger.error(error)
            return error
        except Exception as e:
            logger.error(f"Command error: {e}")
            return f"Error: {str(e)}"
    
    def github_install(self, repo_url):
        try:
            repo_name = repo_url.split('/')[-1].replace('.git', '')
            logger.info(f"Installing: {repo_name}")
            print(f"{Fore.YELLOW}Cloning {repo_name}...")
            
            cmd = f"git clone {repo_url} temp_tools/{repo_name} && cd temp_tools/{repo_name} && chmod +x *"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60, check=False)
            
            if result.returncode == 0:
                print(f"{Fore.GREEN}✓ Installed {repo_name}")
                logger.info(f"Installed: {repo_name}")
                self.github_repos.append(repo_name)
                return True
            else:
                logger.error(f"Install failed: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"GitHub error: {e}")
            return False
    
    def live_dashboard(self):
        while True:
            try:
                self.clear_screen()
                try:
                    print(Fore.RED + Figlet(font='small').renderText('CYBERFORGE'))
                except:
                    print(Fore.RED + "=== CYBERFORGE ===")
                
                table = Table(title=f"Dashboard - {self.current_user}")
                table.add_column("Module", style="cyan")
                table.add_column("Status", style="green")
                table.add_column("Action", style="magenta")
                
                tools = {
                    "1": ["🔍 NMAP Scanner", "Ready", "scan"],
                    "2": ["🔓 HYDRA Brute", "Ready", "brute"],
                    "3": ["📶 WIFITE WiFi", "Ready", "wifi"],
                    "4": ["🤖 AI Assistant", "Online", "ai"],
                    "5": ["📥 GitHub Install", "Ready", "github"],
                    "6": ["📊 System Info", "Live", "sysinfo"],
                    "7": ["🎤 Voice Mode", f"{'ON' if self.is_voice_active else 'OFF'}", "voice"],
                    "0": ["❌ Exit", "Safe", "exit"]
                }
                
                for key, (name, status, action) in tools.items():
                    table.add_row(name, status, action)
                
                console.print(table)
                print(f"\n{Fore.YELLOW}Commands: type number...")
                
                if self.is_voice_active:
                    voice_cmd = self.listen()
                    if voice_cmd:
                        self.handle_voice_command(voice_cmd)
                
                cmd = input(f"\n{Fore.CYAN}CyberForge> {Style.RESET_ALL}").lower().strip()
                if cmd:
                    self.handle_command(cmd)
                    self.session_log.append(f"Cmd: {cmd}")
            except KeyboardInterrupt:
                self._handle_interrupt(None, None)
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    def handle_voice_command(self, command):
        try:
            logger.info(f"Voice cmd: {command}")
            if "nmap" in command or "scan" in command:
                self.nmap_scan()
            elif "help" in command:
                self.speak("Commands available")
            elif "exit" in command:
                self.speak("Goodbye")
                sys.exit(0)
        except Exception as e:
            logger.error(f"Voice error: {e}")
    
    def handle_command(self, cmd):
        try:
            logger.info(f"Cmd: {cmd}")
            if cmd == "1" or "nmap" in cmd:
                self.nmap_scan()
            elif cmd == "2" or "hydra" in cmd:
                self.hydra_brute()
            elif cmd == "3" or "wifi" in cmd:
                self.wifite_attack()
            elif cmd == "4" or "ai" in cmd:
                self.ai_interactive()
            elif cmd == "5" or "github" in cmd:
                self.github_menu()
            elif cmd == "6" or "sysinfo" in cmd:
                self.system_info()
            elif cmd == "7" or "voice" in cmd:
                self.toggle_voice()
            elif cmd == "0" or "exit" in cmd:
                print(f"{Fore.RED}Shutting down...")
                self.speak("Goodbye")
                sys.exit(0)
            else:
                print(f"{Fore.RED}Unknown command")
        except Exception as e:
            logger.error(f"Cmd error: {e}")
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    def nmap_scan(self):
        try:
            logger.info("NMAP started")
            target = input(f"{Fore.CYAN}Target: {Style.RESET_ALL}").strip()
            if not target:
                print(f"{Fore.RED}No target")
                return
            
            print(f"{Fore.YELLOW}Scanning {target}...")
            self.speak(f"Scanning {target}")
            result = self.run_command(f"nmap -sV -A {target}")
            print(f"{Fore.GREEN}{result}")
            input(f"\n{Fore.YELLOW}Press Enter...")
        except Exception as e:
            logger.error(f"NMAP error: {e}")
            print(f"{Fore.RED}Error: {e}")
    
    def hydra_brute(self):
        try:
            logger.info("Hydra started")
            print(f"{Fore.RED}⚠️  Use Responsibly!")
            target = input(f"{Fore.CYAN}Target: {Style.RESET_ALL}").strip()
            if not target:
                return
            
            service = input(f"{Fore.CYAN}Service: {Style.RESET_ALL}").strip()
            if not service:
                return
            
            user = input(f"{Fore.CYAN}Username: {Style.RESET_ALL}").strip()
            if not user:
                return
            
            passlist = input(f"{Fore.CYAN}Wordlist: {Style.RESET_ALL}").strip()
            if not passlist:
                return
            
            cmd = f"hydra -l {user} -P {passlist} {target} {service}"
            print(f"{Fore.YELLOW}Running: {cmd}")
            result = self.run_command(cmd, timeout=300)
            print(result)
            input(f"\n{Fore.YELLOW}Press Enter...")
        except Exception as e:
            logger.error(f"Hydra error: {e}")
            print(f"{Fore.RED}Error: {e}")
    
    def wifite_attack(self):
        try:
            logger.info("WiFite started")
            print(f"{Fore.YELLOW}Starting WiFi attack...")
            self.speak("WiFi attack")
            result = self.run_command("wifite")
            if result:
                print(result)
        except Exception as e:
            logger.error(f"WiFite error: {e}")
            print(f"{Fore.RED}Error: {e}")
    
    def ai_interactive(self):
        try:
            logger.info("AI session")
            print(f"{Fore.CYAN}🤖 AI Active (exit to quit)")
            self.speak("AI online")
            
            while True:
                try:
                    user_input = input(f"{Fore.MAGENTA}You: {Style.RESET_ALL}").strip()
                    if not user_input:
                        continue
                    if user_input.lower() == 'exit':
                        break
                    
                    response = self.ai_chat(user_input)
                    print(f"{Fore.CYAN}AI: {response}")
                    self.speak(response)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    logger.error(f"AI error: {e}")
        except Exception as e:
            logger.error(f"AI session error: {e}")
    
    def github_menu(self):
        try:
            logger.info("GitHub menu")
            print(f"{Fore.YELLOW}📥 GitHub Installer")
            repo = input(f"{Fore.CYAN}URL: {Style.RESET_ALL}").strip()
            if not repo:
                return
            os.makedirs("temp_tools", exist_ok=True)
            self.github_install(repo)
        except Exception as e:
            logger.error(f"GitHub error: {e}")
    
    def system_info(self):
        try:
            logger.info("System info")
            info = self.run_command("neofetch --config /dev/null")
            print(info)
            input(f"\n{Fore.YELLOW}Press Enter...")
        except Exception as e:
            logger.error(f"Sysinfo error: {e}")
    
    def toggle_voice(self):
        try:
            if not AUDIO_AVAILABLE:
                print(f"{Fore.RED}Voice unavailable")
                return
            
            self.is_voice_active = not self.is_voice_active
            status = "ON" if self.is_voice_active else "OFF"
            print(f"{Fore.GREEN}Voice: {status}")
            self.speak(f"Voice {status}")
            logger.info(f"Voice: {status}")
        except Exception as e:
            logger.error(f"Voice error: {e}")
    
    def run(self):
        try:
            logger.info("Main loop")
            os.makedirs("temp_tools", exist_ok=True)
            
            while True:
                try:
                    if not self.login_system():
                        continue
                    self.live_dashboard()
                except KeyboardInterrupt:
                    self._handle_interrupt(None, None)
                except Exception as e:
                    logger.error(f"Loop error: {e}")
        except Exception as e:
            logger.critical(f"Fatal: {e}")
            sys.exit(1)

def main():
    try:
        logger.info("===== START =====")
        os.system("mkdir -p temp_tools")
        cyberforge = CyberForge()
        cyberforge.run()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Fatal: {e}")
        sys.exit(1)
    finally:
        logger.info("===== END =====")

if __name__ == "__main__":
    main()
