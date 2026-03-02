from abc import ABC, abstractmethod

class FileRepository(ABC):
    @abstractmethod
    def get_files_content(self, path: str):
        """Generador que devuelve (nombre_archivo, contenido)"""
        pass