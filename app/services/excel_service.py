import pandas as pd
from typing import Dict, List, Any
import io

class ExcelService:
    @staticmethod
    def read_excel_file(file_content: bytes, sheet_name: str = None) -> Dict[str, List[Dict[str, Any]]]:
        """
        Lee un archivo Excel y devuelve su contenido como diccionario.
        
        Args:
            file_content: Contenido binario del archivo Excel
            sheet_name: Nombre de la hoja específica a leer (opcional)
            
        Returns:
            Diccionario con los datos del Excel
        """
        try:
            # Leer el archivo Excel desde el contenido binario
            excel_file = io.BytesIO(file_content)
            
            if sheet_name:
                # Leer una hoja específica
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                return {sheet_name: df.to_dict(orient='records')}
            else:
                # Leer todas las hojas
                excel_data = pd.read_excel(excel_file, sheet_name=None)
                return {sheet: df.to_dict(orient='records') for sheet, df in excel_data.items()}
                
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Excel: {str(e)}")
    
    @staticmethod
    def get_sheet_names(file_content: bytes) -> List[str]:
        """
        Obtiene los nombres de todas las hojas del archivo Excel.
        
        Args:
            file_content: Contenido binario del archivo Excel
            
        Returns:
            Lista con los nombres de las hojas
        """
        try:
            excel_file = io.BytesIO(file_content)
            excel_file = pd.ExcelFile(excel_file)
            return excel_file.sheet_names
        except Exception as e:
            raise ValueError(f"Error al obtener los nombres de las hojas: {str(e)}")
