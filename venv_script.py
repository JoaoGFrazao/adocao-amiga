import os
import subprocess
import sys

def create_and_setup_virtualenv():
    # Define o nome do diretório do ambiente virtual
    venv_dir = "venv"

    # Cria o ambiente virtual
    print("Criando o ambiente virtual...")
    subprocess.run([sys.executable, "-m", "venv", venv_dir])

    # Ativa o ambiente virtual (método específico para cada sistema operacional)
    activate_script = os.path.join(venv_dir, "Scripts", "activate") if os.name == "nt" else os.path.join(venv_dir, "bin", "activate")
    
    # Instala as dependências do arquivo requirements.txt
    print("Instalando dependências do requirements.txt...")
    subprocess.run([os.path.join(venv_dir, "bin", "pip") if os.name != "nt" else os.path.join(venv_dir, "Scripts", "pip"), "install", "-r", "requirements.txt"])

    print("Ambiente virtual criado e dependências instaladas com sucesso.")

if __name__ == "__main__":
    create_and_setup_virtualenv()
