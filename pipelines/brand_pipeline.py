from bson import ObjectId

def get_brand_pipeline() -> list:
    return [
        {
            '$addFields': {
                'id': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$lookup': {
                'from': 'motorcycles', 
                'localField': 'id', 
                'foreignField': 'id_marca', 
                'as': 'result'
            }
        }, {
            '$group': {
                '_id': {
                    'id': '$id', 
                    'description': '$description', 
                    'active': '$active'
                }, 
                'number_of_motos': {
                    '$sum': {
                        '$size': '$result'
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'id': '$_id.id', 
                'description': '$_id.description', 
                'active': '$_id.active', 
                'number_of_motos': '$number_of_motos'
            }
        }
    ]
    
def validate_brand_is_assigned(id:str) -> list:
    return [
        {
            "$match" : {
                "$_id" : ObjectId(id)
            }  
        },{
            '$addFields': {
                'id': {
                    '$toString': '$_id'
                }
            }
        }, {
            '$lookup': {
                'from': 'motorcycles', 
                'localField': 'id', 
                'foreignField': 'id_marca', 
                'as': 'result'
            }
        }, {
            '$group': {
                '_id': {
                    'id': '$id', 
                    'description': '$description', 
                    'active': '$active'
                }, 
                'number_of_motos': {
                    '$sum': {
                        '$size': '$result'
                    }
                }
            }
        }, {
            '$project': {
                '_id': 0, 
                'id': '$_id.id', 
                'description': '$_id.description', 
                'active': '$_id.active', 
                'number_of_motos': 1
            }
        }
    ]