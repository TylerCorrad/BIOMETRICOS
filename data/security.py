from pathlib import Path
from cryptography.fernet import Fernet

try:
    clave = (Path.cwd() / "secret.key").read_text().encode()
    fernet = Fernet(clave)
except FileNotFoundError:
    # Generar una nueva clave y guardarla en un archivo
    clave = Fernet.generate_key()
    (Path.cwd() / "secret.key").write_text(clave.decode())
    fernet = Fernet(clave)

def encriptar(texto: str) -> str:
    return fernet.encrypt(texto.encode()).decode()


def desencriptar(texto_encriptado: str) -> str:
    return fernet.decrypt(texto_encriptado.encode()).decode()
