import os
import sys
from dotenv import load_dotenv
from ports.repository import FileRepository
from ports.database import ScanHistoryRepository
from adapters.file_system import LocalFileRepository
from adapters.git_repository import GitFileRepository
from adapters.postgres_adapter import PostgresScanRepository
from core.scanner import SecretScanner

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def get_db_config():
    """
    Extrae la configuración de la base de datos desde el entorno.
    Si falta alguna variable crítica, devolverá None o lanzará un aviso.
    """
    config = {
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432")
    }

    if not config["dbname"] or not config["password"]:
        return None
    return config

def main():
    
    if len(sys.argv) < 2:
        print("\n Error: Falta el objetivo de escaneo.")
        print("Uso: python3 -m main <ruta_local_o_url_git>")
        print("Ejemplo: python3 -m main https://github.com/usuario/repo.git")
        return

    target = sys.argv[1]

    # Configuración de la Base de Datos 
    db_params = get_db_config()
    if not db_params:
        print(" Error: Configuración de base de datos incompleta en el archivo .env")
        print("Asegúrate de tener DB_NAME, DB_USER y DB_PASS definidos.")
        return

    try:
        db_repo = PostgresScanRepository(db_params)
    except Exception as e:
        print(f"Error al conectar con PostgreSQL: {e}")
        return

    if target.startswith(("http://", "https://", "git@")) or target.endswith(".git"):
        print(f" Detectado objetivo remoto. Usando adaptador Git...")
        file_repo = GitFileRepository()
    else:
        print(f" Detectado objetivo local. Usando adaptador de Sistema de Archivos...")
        file_repo = LocalFileRepository()

    scanner = SecretScanner(file_repo, db_repo)

    print(f"Iniciando escaneo de seguridad en: {target}\n")
    print("-" * 50)

    try:
        results = scanner.scan(target)

        if not results:
            print("\nResultado: No se encontraron secretos y los archivos nuevos han sido registrados como seguros.")
        else:
            print(f"\n¡ALERTA! Se han encontrado posibles secretos en {len(results)} archivo(s):")
            for r in results:
                print(f"\nArchivo: {r['file']}")
                for match in r['secrets']:
                    print(f"   Tipo: {match[0]} | Valor: {match[1]}")
            
            print("\nEstos archivos no se han guardado en la base de datos de 'vistos' para su revisión manual.")

    except Exception as e:
        print(f" Ocurrió un error durante el escaneo: {e}")

    print("-" * 50)
    print(" Proceso finalizado.")

if __name__ == "__main__":
    main()