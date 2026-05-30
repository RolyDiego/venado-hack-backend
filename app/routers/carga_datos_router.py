from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from fastapi.responses import JSONResponse
from app.services.excel_service import ExcelService

router = APIRouter()

@router.post("/excel")
async def upload_excel(
    file: UploadFile = File(...),
    sheet_name: str = Query(None, description="Nombre de la hoja específica a leer (opcional)")
):
    """
    Endpoint para recibir y leer un archivo Excel.
    
    Args:
        file: Archivo Excel a procesar
        sheet_name: Nombre de la hoja específica (opcional, si no se especifica lee todas las hojas)
        
    Returns:
        Diccionario con los datos del Excel organizados por hojas
    """
    # Validar que el archivo sea un Excel
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
    
    try:
        # Leer el contenido del archivo
        file_content = await file.read()
        
        # Procesar el archivo Excel
        excel_service = ExcelService()
        data = excel_service.read_excel_file(file_content, sheet_name)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Archivo Excel procesado exitosamente",
                "filename": file.filename,
                "data": data,
                "sheets": list(data.keys())
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el archivo: {str(e)}")

@router.post("/excel/hojas")
async def get_excel_sheets(file: UploadFile = File(...)):
    """
    Endpoint para obtener los nombres de las hojas de un archivo Excel.
    
    Args:
        file: Archivo Excel a procesar
        
    Returns:
        Lista con los nombres de las hojas
    """
    # Validar que el archivo sea un Excel
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="El archivo debe ser un Excel (.xlsx o .xls)")
    
    try:
        # Leer el contenido del archivo
        file_content = await file.read()
        
        # Obtener los nombres de las hojas
        excel_service = ExcelService()
        sheet_names = excel_service.get_sheet_names(file_content)
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Hojas obtenidas exitosamente",
                "filename": file.filename,
                "sheets": sheet_names
            }
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener las hojas: {str(e)}")
