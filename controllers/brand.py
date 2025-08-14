from models.brand import Brand
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

from pipelines.brand_pipeline import get_brand_pipeline, validate_brand_is_assigned

coll = get_collection("brands")

async def create_brand(brand: Brand) -> Brand:
    try:
        brand.description = brand.description.strip().lower() # Normaliza la descripción de la marca
        
        existing_brand = coll.find_one({"description": brand.description})
        if existing_brand:
            raise HTTPException(status_code=400, detail="La marca ya existe")

        brand_dict = brand.model_dump(exclude={"id"})
        inserted = coll.insert_one(brand_dict)
        brand.id = str(inserted.inserted_id)
        return brand
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_brands() -> list[Brand]:
    try:
        pipeline = get_brand_pipeline()
        brands = list(coll.aggregate(pipeline))
        
        # brands = []
        # for brand in coll.find():
        #     brand["id"] = str(brand["_id"])
        #     del brand["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Brand
        #     brands.append(Brand(**brand))
        return brands
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching brand: {str(e)}")
    
async def get_brand_by_id(brand_id: str) -> Brand:
    try:
        brand = coll.find_one({"_id": ObjectId(brand_id)})
        if not brand:
            raise HTTPException(status_code=404, detail="Marca no encontrada")
        
        brand["id"] = str(brand["_id"])
        del brand["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto Brand
        return Brand(**brand)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def update_brand(brand_id: str, brand: Brand) -> Brand:
    try:
        brand.description = brand.description.strip().lower()
        # Verifica si ya existe una marca con la misma descripción, excepto la que se está actualizando
        existing_brand = coll.find_one({"description": brand.description, "_id": {"$ne": ObjectId(brand_id)}}) # $ne significa "no igual a"
        # Verifica si ya existe una marca con la misma descripción, excepto la que se está actualizando
        if existing_brand: # Si ya existe una marca con la misma descripción, se lanza una excepción
            raise HTTPException(status_code=400, detail="La marca ya existe")
        
        result = coll.update_one(
            {"_id": ObjectId(brand_id)},
            {"$set": brand.model_dump(exclude={"id"})}
        )
        
        # Si no se actualizó ningún documento, significa que no se encontró la marca
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Marca no encontrada")
        
        brand.id = brand_id
        return brand
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    
async def desactivate_brand(brand_id : str) -> dict:
    try :
        pipeline = validate_brand_is_assigned(brand_id)
        assigned = list(coll.aggregate(pipeline))
        
        if assigned is None:
            raise HTTPException(status_code=404, detail="Brand not found")
        
        if assigned[0]["number_of_motos"] > 0:
            coll.update_one(
                {"_id" : ObjectId(brand_id)},
                {"$set" : {"active" : False}}
            )
            return {"message" : "Brand is assigned to motorcycles and has been desactivate"}
        else:
            coll.delete_one({"_id" : ObjectId(brand_id)})
            return {"message" : "Brand deleted sucefully"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error desactivating brand: {str(e)} ")


async def delete_brand(brand_id: str) -> Brand: # Eliminar una marca por su ID
    try:
        #Verifica si la marca tiene motocicletas asociadas
        coll_motorcycles = get_collection("motorcycles")
        existing_motorcycle = coll_motorcycles.find_one({"id_marca": brand_id})
        if existing_motorcycle: # Si ya existe una motocicleta con la misma marca, se lanza una excepción
            raise HTTPException(status_code=400, detail="No se puede eliminar la marca porque tiene motocicletas asociadas")

        result = coll.delete_one({"_id": ObjectId(brand_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Marca no encontrada")
        
        return {"message": "Marca eliminada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))