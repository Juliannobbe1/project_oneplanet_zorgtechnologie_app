from abc import ABC, abstractmethod
import pandas as pd
from loguru import logger

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
        logger.trace("Attempting to process XML file '{file}' into DataFrame", file=file)
        file_contents = file.read()
        df = pd.read_xml(file_contents)
        logger.trace("Successfully processed XML file '{file}' into DataFrame")
        return df

class JSONProcessor(FileProcessor):
    def process(self, file):
        logger.trace("Attempting to process JSON file '{file}' into DataFrame", file=file)
        df = pd.read_json(file)
        logger.trace("Successfully processed JSON file '{file}' into DataFrame")
        return df

class CSVProcessor(FileProcessor):
    def process(self, file):
        logger.trace("Attempting to process CSV file '{file}' into DataFrame", file=file)
        df = pd.read_csv(file)
        logger.trace("Successfully processed CSV file '{file}' into DataFrame")
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
        logger.trace("Attempting to create file processor for file '{file}'", file=file)
        if file.filename.endswith('.xml'):
            xml_processor = XMLProcessor()
            logger.trace("Created XML file processor for file '{file}'", file=file)
            return xml_processor
        elif file.filename.endswith('.json'):
            json_processor = JSONProcessor()
            logger.trace("Created JSON file processor for file '{file}'", file=file)
            return json_processor
        elif file.filename.endswith('.csv'):
            csv_processor = CSVProcessor()
            logger.trace("Creating CSV file processor for file '{file}'", file=file)
            return csv_processor
        else:
            logger.error("Unsupported file type: '{file}'", file=file)
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
