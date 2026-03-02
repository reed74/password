import hashlib
import re

class SecretScanner:
    def __init__(self, file_repo, db_repo):
        self.file_repo = file_repo
        self.db_repo = db_repo
        self.pattern = re.compile(r'(password|api_key|secret|token)\s*[:=]\s*["\']?([\w-]+)["\']?', re.IGNORECASE)

    def _calculate_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def scan(self, path: str):
        findings = []
        for name, content in self.file_repo.get_files_content(path):
            file_hash = self._calculate_hash(content)

            # 1. ¿Ya lo conocemos y estaba limpio? Lo saltamos.
            if self.db_repo.is_already_scanned(file_hash):
                print(f"Saltando (ya escaneado y limpio): {name}")
                continue

            matches = self.pattern.findall(content)
            
            if matches:
                # Si tiene secretos, no lo guardamos como "limpio"
                findings.append({"file": name, "secrets": matches})
            else:
                # 2. Si está limpio, guardamos su hash para la próxima vez
                self.db_repo.save_safe_file(name, file_hash)
                
        return findings