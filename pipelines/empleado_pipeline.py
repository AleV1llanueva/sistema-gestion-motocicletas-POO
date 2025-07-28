from bson import ObjectId

def validate_user_pipeline(user_id:str) -> dict:
    return [
    {
        '$match': {
            '_id': ObjectId(user_id), 
            'active': True
        }
    }, {
        '$project': {
            'id': {
                '$toString': '$_id'
            }, 
            'nombre_completo': {
                '$concat': [
                    '$name', ' ', '$lastname'
                ]
            }, 
            'email': '$email'
        }
    }
]