from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId


from models.motorcycle import Motorcycle
from pipelines.motorcycles_pipeline import get_motorcycles_with_brand_pipeline

coll = get_collection("motorcycles")  # Obtiene la colección de motocicletas de MongoDB

async def create_motorcycle(motorcycle: Motorcycle) -> Motorcycle:
    try:
        motorcycle.name = motorcycle.name.strip().lower() # Normaliza el nombre de la motocicleta
        motorcycle.id_marca = motorcycle.id_marca.strip().lower() # Normaliza el id de la marca
        
        #Validacion de que el id de la marca pertenezca a una marca existente
        coll_brands = get_collection("brands")
        existing_brand = coll_brands.find_one({"_id": ObjectId(motorcycle.id_marca)})
        if not existing_brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada")

        existing_motorcycle = coll.find_one({"name": motorcycle.name})
        if existing_motorcycle:
            raise HTTPException(status_code=400, detail="La motocicleta ya existe")

        motorcycle_dict = motorcycle.model_dump(exclude={"id"})
        inserted = coll.insert_one(motorcycle_dict)
        motorcycle.id = str(inserted.inserted_id)
        return motorcycle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_motorcycles() -> list[Motorcycle]:
    try:
        
        
        pipeline = get_motorcycles_with_brand_pipeline()
        motorcycle_result = list(coll.aggregate(pipeline))
        
        if not motorcycle_result:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")

        return motorcycle_result   # Devuelve el primer (y único) resultado de la agregación
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error al obtener la motocicleta: " + str(e))
        
    #     motorcycles = []
    #     for motorcycle in coll.find():
    #         motorcycle["id"] = str(motorcycle["_id"])
    #         del motorcycle["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Motorcycle
    #         motorcycles.append(Motorcycle(**motorcycle))
    #     return motorcycles
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=str(e))

async def get_motorcycle_by_id(motorcycle_id: str) -> Motorcycle:
    try:
        
        motorcycle = coll.find_one({"_id": ObjectId(motorcycle_id)})
        if not motorcycle:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")

        motorcycle["id"] = str(motorcycle["_id"])
        del motorcycle["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Motorcycle
        return Motorcycle(**motorcycle)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_motorcycle(motorcycle_id: str, motorcycle: Motorcycle) -> Motorcycle:
    try:
        motorcycle.name = motorcycle.name.strip().lower()
        motorcycle.id_marca = motorcycle.id_marca.strip().lower() # Normaliza el id de la marca

        #Validacion de que el id de la marca pertenezca a una marca existente
        coll_brands = get_collection("brands")
        existing_brand = coll_brands.find_one({"_id": ObjectId(motorcycle.id_marca)})
        
        if not existing_brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada, asegúrese de que el id de la marca sea correcto")

        # Verifica si ya existe una motocicleta con el mismo nombre, excepto la que se está actualizando
        existing_motorcycle = coll.find_one({"name": motorcycle.name, "_id": {"$ne": ObjectId(motorcycle_id)}}) # $ne significa "no igual a"
        if existing_motorcycle and existing_motorcycle.id_marca == motorcycle.id_marca : 
            raise HTTPException(status_code=400, detail="La motocicleta ya existe dentro de la marca seleccionada")
        
        result = coll.update_one(
            {"_id": ObjectId(motorcycle_id)},
            {"$set": motorcycle.model_dump(exclude={"id"})}
        )

        # Si no se actualizó ningún documento, significa que no se encontró la motocicleta
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada, asegúrese de que el id de la motocicleta sea correcto")
        
        motorcycle.id = motorcycle_id
        return motorcycle
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def delete_motorcycle(motorcycle_id: str) -> Motorcycle: # Eliminar una motocicleta por su ID
    try:
        result = coll.delete_one({"_id": ObjectId(motorcycle_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Motocicleta no encontrada")

        return {"message": "Motocicleta eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))