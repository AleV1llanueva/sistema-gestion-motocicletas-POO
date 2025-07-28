import re
from models.matenimiento import Mantenimiento
from fastapi import HTTPException
from utils.mongodb import get_collection
from bson import ObjectId

coll = get_collection("mantenimientos")

async def create_mantenimiento(mantenimiento: Mantenimiento) -> Mantenimiento:

    try:
        mantenimiento_dict = mantenimiento.model_dump(exclude={"id"})
        result = coll.insert_one(mantenimiento_dict)
        mantenimiento.id = str(result.inserted_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return mantenimiento

async def get_mantenimiento_by_id(mantenimiento_id: str) -> Mantenimiento:
    try:
        if not ObjectId.is_valid(mantenimiento_id):
            raise HTTPException(status_code=400, detail="ID inválido")

        mantenimiento = coll.find_one({"_id": ObjectId(mantenimiento_id)})
        if not mantenimiento:
            raise HTTPException(status_code=404, detail="Mantenimiento no encontrado")

        mantenimiento["id"] = str(mantenimiento["_id"])
        del mantenimiento["_id"]  # Eliminar el campo _id de MongoDB al momento de crear el objeto Mantenimiento
        return Mantenimiento(**mantenimiento)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))