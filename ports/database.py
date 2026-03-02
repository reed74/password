from abc import ABC, abstractmethod

class ScanHistoryRepository(ABC):
    @abstractmethod
    def is_already_scanned(self, file_hash: str) -> bool:
        """Verifica si el hash ya existe en la base de datos."""
        pass

    @abstractmethod
    def save_safe_file(self, file_name: str, file_hash: str):
        """Guarda el hash de un archivo que sabemos que está limpio."""
        pass