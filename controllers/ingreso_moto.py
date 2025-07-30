import re
from models.ingreso_moto import IngresoMoto
from fastapi import HTTPException
from utils.mongodb import get_collection
from bson import ObjectId
from pipelines.ingreso_moto_pipeline import get_ingreso_moto_by_id_pipeline

coll = get_collection("ingresos_motos")

async def create_ingreso_moto(ingreso: IngresoMoto) -> IngresoMoto:
    
    try: 
        if not ingreso.id_modelo or not ingreso.id_cliente or not ingreso.id_empleado:
            raise HTTPException(status_code=400, detail="Modelo, cliente y empleado son requeridos")
        
        if not re.match(r"^[A-Z0-9]{1,10}$", ingreso.placa):
            raise HTTPException(status_code=400, detail="Placa inválida")
        
        if not re.match(r"^[A-HJ-NPR-Z0-9]{17}$", ingreso.vin):
            raise HTTPException(status_code=400, detail="VIN inválido")

        ingreso_dict = ingreso.model_dump(exclude={"id"})
        result = coll.insert_one(ingreso_dict)
        ingreso.id = str(result.inserted_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return ingreso

async def get_ingreso_moto_by_id(ingreso_id: str) -> dict:
    try:
        
        pipeline = get_ingreso_moto_by_id_pipeline(ingreso_id)
        result = list(coll.aggregate(pipeline))
        
        if not result :
            raise HTTPException(status_code=404, detail="ingreso no encontrado")
        
        doc = result
        
        def convert_object_ids_recursive(obj):
            if isinstance(obj, dict):
                return {
            k: convert_object_ids_recursive(v)
            for k, v in obj.items()
                }
            elif isinstance(obj, list):
                return [convert_object_ids_recursive(i) for i in obj]
            elif isinstance(obj, ObjectId):
                return str(obj)
            else:
                return obj
        
        doc = convert_object_ids_recursive(result[0])

        
        return doc

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))