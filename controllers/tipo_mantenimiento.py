import re
from models.tipo_mantenimiento import TipoMantenimiento
from fastapi import HTTPException
from utils.mongodb import get_collection
from bson import ObjectId

coll = get_collection("tipos_mantenimiento")

async def create_tipo_mantenimiento(tipo_mantenimiento: TipoMantenimiento) -> TipoMantenimiento:

    try:
        
        tipo_mantenimiento_dict = tipo_mantenimiento.model_dump(exclude={"id"})
        result = coll.insert_one(tipo_mantenimiento_dict)
        tipo_mantenimiento.id = str(result.inserted_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return tipo_mantenimiento

async def get_tipo_mantenimiento_by_id(tipo_mantenimiento_id: str) -> TipoMantenimiento:
    try:
        if not ObjectId.is_valid(tipo_mantenimiento_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        tipo_mantenimiento = coll.find_one({"_id": ObjectId(tipo_mantenimiento_id)})
        if not tipo_mantenimiento:
            raise HTTPException(status_code=404, detail="Tipo de mantenimiento no encontrado")

        tipo_mantenimiento["id"] = str(tipo_mantenimiento["_id"])
        del tipo_mantenimiento["_id"]  # Eliminar el campo _id de MongoDB al momento de crear el objeto TipoMantenimiento
        return TipoMantenimiento(**tipo_mantenimiento)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))