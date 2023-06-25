from abc import ABC, abstractmethod
import pandas as pd

class FileProcessor(ABC):
    @abstractmethod
    def process(self, file):
        """
        Process the file and return the processed DataFrame.
        
        Args:
            file: File object to be processed.
        
        Returns:
            The processed DataFrame.
        """
        pass

class XMLProcessor(FileProcessor):
    def process(self, file):
        file_contents = file.read()
        df = pd.read_xml(file_contents)
        return df

class JSONProcessor(FileProcessor):
    def process(self, file):
        df = pd.read_json(file)
        return df

class CSVProcessor(FileProcessor):
    def process(self, file):
        df = pd.read_csv(file)
        return df


class FileHandler:
    def __init__(self):
        pass
    
    def create_file_processor(self, file):
        """
        Create the appropriate FileProcessor instance based on the file's extension.
        
        Args:
            file: File object to be processed.
        
        Returns:
            An instance of the appropriate FileProcessor subclass.
        
        Raises:
            ValueError: If the file type is not supported.
        """
        if file.filename.endswith('.xml'):
            return XMLProcessor()
        elif file.filename.endswith('.json'):
            return JSONProcessor()
        elif file.filename.endswith('.csv'):
            return CSVProcessor()
        else:
            raise ValueError("Unsupported file type.")

    def process_file(self,file):
        """
        Process the uploaded file.
        
        Args:
            file: File object to be processed.
        
        Returns:
            The result of the file processing.
        
        Raises:
            ValueError: If the file type is not supported.
            Exception: If there is an error during file processing.
        """
        try:
            processor = self.create_file_processor(file)
            df = processor.process(file)
             
            return df 
        except Exception as e:
            # Handle exceptions or error messages appropriately
            raise e
