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

async def get_tipo_mantenimiento() -> list[TipoMantenimiento]:
    try:
        tipos = []
        for tipo in coll.find():
            tipo["id"] = str(tipo["_id"])
            del tipo["_id"]
            tipos.append(TipoMantenimiento(**tipo))
        return tipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_tipo_mantenimiento_by_id(tipo_mantenimiento_id: str) -> TipoMantenimiento:
    try:
        tipo_mantenimiento = coll.find_one({"_id": ObjectId(tipo_mantenimiento_id)})
        if not tipo_mantenimiento:
            raise HTTPException(status_code=404, detail="Tipo de mantenimiento no encontrado")

        tipo_mantenimiento["id"] = str(tipo_mantenimiento["_id"])
        del tipo_mantenimiento["_id"]  # Eliminar el campo _id de MongoDB al momento de crear el objeto TipoMantenimiento
        return TipoMantenimiento(**tipo_mantenimiento)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_tipo_mantenimiento(tipo_id:str, tipo_mantenimiento:TipoMantenimiento) -> TipoMantenimiento:
    try: 
        tipo_mantenimiento.description = tipo_mantenimiento.description.strip().lower()
        
        existing_tipo = coll.find_one({"description":tipo_mantenimiento.description, "_id":{"$ne": ObjectId(tipo_id)}})
        if existing_tipo:
            raise HTTPException(status_code=400, detail="El tipo de mantenimiento ya existe")
        
        result = coll.update_one({"_id": ObjectId(tipo_id)}, {"$set":tipo_mantenimiento.model_dump(exclude={"id"})})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Tipo de mantenimiento no encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 

async def delete_tipo_mantenimiento(tipo_id: str) -> TipoMantenimiento:
    try:
        coll_mantenimientos = get_collection("mantenimientos")
        existing_mantenimiento = coll_mantenimientos.find_one({"id_tipo_mantenimiento": tipo_id})
        if existing_mantenimiento:
            raise HTTPException(status_code=400, detail="El tipo tiene mantenimientos asociados, no se puede eliminar")

        result = coll.delete_one({"_id": ObjectId(tipo_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="tipo de mantenimiento no encontrado")
        
        return {"message": "Tipo de mantenimiento eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))