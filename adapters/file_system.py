import os
from ports.repository import FileRepository

class LocalFileRepository(FileRepository):
    def get_files_content(self, path: str):
        # Verificamos si la ruta existe
        if not os.path.exists(path):
            print(f"Error: La ruta '{path}' no existe.")
            return

        for root, _, files in os.walk(path):
            for file in files:
                full_path = os.path.join(root, file)
                print(f"Analizando: {full_path}") 
                try:
                    with open(full_path, 'r', encoding='utf-8') as f:
                        yield file, f.read()
                except Exception as e:
                    print(f"Skipping {file}: {e}")
                    continue