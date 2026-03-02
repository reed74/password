import os
import tempfile
from git import Repo
from ports.repository import FileRepository

class GitFileRepository(FileRepository):
    def get_files_content(self, repo_url: str):
        # Creamos un directorio temporal para no ensuciar tu PC
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"Clonando {repo_url} en directorio temporal...")
            Repo.clone_from(repo_url, tmpdir)
            
            for root, _, files in os.walk(tmpdir):
                # Saltamos la carpeta .git para no buscar en el historial interno
                if '.git' in root:
                    continue
                    
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, tmpdir)
                    
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                            yield relative_path, f.read()
                    except Exception:
                        continue