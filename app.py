import os
import subprocess
import sys

def install_requirements():
    """Installe les dépendances depuis requirements.txt si elles ne sont pas déjà installées."""
    try:
        import discord
    except ImportError:
        print("Les dépendances ne sont pas installées. Installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    else:
        print("Toutes les dépendances sont déjà installées.")

def run_bot():
    """Lance le fichier main.py."""
    os.system(f"{sys.executable} main.py")

if __name__ == "__main__":
    install_requirements()
    run_bot()
