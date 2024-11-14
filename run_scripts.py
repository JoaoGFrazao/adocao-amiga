import subprocess
import time
import sys

# Lista de scripts a serem executados na ordem desejada
scripts = [
    'superuser_script.py',
    'popula_usuario.py',
    'popula_cachorro.py',
    'popula_gato.py',
    'popula_tags.py',
    'popula_galeria.py',
    'popula_animais.py'
]

for script in scripts:
    # Executa cada script e aguarda a conclusão
    result = subprocess.run([sys.executable, script], capture_output=True, text=True)
    time.sleep(3)
    # Verifica se a execução foi bem-sucedida
    if result.returncode == 0:
        print(f'{script} executado com sucesso.')
    else:
        print(f'Erro ao executar {script}: {result.stderr}')
