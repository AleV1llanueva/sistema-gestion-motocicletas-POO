import re
from models.ingreso_moto import IngresoMoto
from fastapi import HTTPException
from utils.mongodb import get_collection
from bson import ObjectId

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

async def get_ingreso_moto_by_id(ingreso_id: str) -> IngresoMoto:
    try:
        if not ObjectId.is_valid(ingreso_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        ingreso = coll.find_one({"_id": ObjectId(ingreso_id)})
        if not ingreso:
            raise HTTPException(status_code=404, detail="Ingreso no encontrado")

        ingreso["id"] = str(ingreso["_id"])
        del ingreso["_id"]  # Eliminar el campo _id de MongoDB al momento de crear el objeto IngresoMoto
        return IngresoMoto(**ingreso)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))