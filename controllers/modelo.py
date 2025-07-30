from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

from models.modelo import Modelo

coll = get_collection("modelos") 

async def create_modelo(modelo: Modelo) -> Modelo:
    try:
        modelo.nombre = modelo.nombre.strip().lower() 
        modelo.id_motocicleta = modelo.id_motocicleta.strip().lower()
        modelo.id_categoria = modelo.id_categoria.strip().lower()
        
        coll_motorcycle = get_collection("motorcycles")
        existing_motorcycle = coll_motorcycle.find_one({"_id": ObjectId(modelo.id_motocicleta)})
        if not existing_motorcycle:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")
        
        coll_categoria = get_collection("categorias")
        existing_categoria = coll_categoria.find_one({"_id": ObjectId(modelo.id_categoria)})
        if not existing_categoria:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")
        
        existing_modelo = coll.find_one({"nombre": modelo.nombre})
        if existing_modelo:
            raise HTTPException(status_code=400, detail="El modelo ya existe")

        modelo_dict = modelo.model_dump(exclude={"id"})
        inserted = coll.insert_one(modelo_dict)
        modelo.id = str(inserted.inserted_id)
        return modelo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_modelos() -> list[Modelo]:
    try:
        modelos = []
        for modelo in coll.find():
            modelo["id"] = str(modelo["_id"])
            del modelo["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Modelo
            modelos.append(Modelo(**modelo))
        return modelos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_modelo_by_id(modelo_id: str) -> Modelo:
    try:
        
        modelo = coll.find_one({"_id": ObjectId(modelo_id)})
        if not modelo:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")

        modelo["id"] = str(modelo["_id"])
        del modelo["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Modelo
        return Modelo(**modelo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_modelo(modelo_id: str, modelo: Modelo) -> Modelo:
    try:
        modelo.nombre = modelo.nombre.strip().lower() 
        modelo.id_motocicleta = modelo.id_motocicleta.strip().lower()
        modelo.id_categoria = modelo.id_categoria.strip().lower()

        coll_motorcycle = get_collection("motorcycles")
        existing_motorcycle = coll_motorcycle.find_one({"_id": ObjectId(modelo.id_motocicleta)})
        if not existing_motorcycle:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")
        
        coll_categoria = get_collection("categorias")
        existing_categoria = coll_categoria.find_one({"_id": ObjectId(modelo.id_categoria)})
        if not existing_categoria:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")

        existing_modelo = coll.find_one({"nombre": modelo.nombre, "_id": {"$ne": ObjectId(modelo_id)}}) # $ne significa "no igual a"
        if existing_modelo and existing_modelo.id_motocicleta == modelo.id_motocicleta : 
            raise HTTPException(status_code=400, detail="El modelo ya existe dentro de la motocicleta seleccionada")
        
        result = coll.update_one(
            {"_id": ObjectId(modelo_id)},
            {"$set": modelo.model_dump(exclude={"id"})}
        )

        # Si no se actualizó ningún documento, significa que no se encontró la motocicleta
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")
        
        modelo.id = modelo_id
        return modelo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_modelo(modelo_id: str) -> Modelo: # Eliminar una motocicleta por su ID
    try:
        result = coll.delete_one({"_id": ObjectId(modelo_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Modelo no encontrado")

        return {"message": "Modelo eliminado  exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))