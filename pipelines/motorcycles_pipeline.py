from bson import ObjectId

def get_motorcycles_with_brand_pipeline() -> list:
    return [
        {
            "$addFields": {
                "id_marca_obj": {"$toObjectId": "$id_marca"}
            }
        },
        {"$lookup": {
            "from": "brands",
            "localField": "id_marca_obj",
            "foreignField": "_id",
            "as": "marca"
        }},
        {"$unwind": "$marca"},
        {"$project": {
            "_id": 0,
            "id": {"$toString": "$_id"},  # Convierte el _id a string y lo asigna a id            
            "id_marca": "$id_marca",  # Incluye el id de la marca
            "name": "$name",
            "brand_name": "$marca.description",
        }}
    ]