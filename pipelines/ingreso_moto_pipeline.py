from bson import ObjectId

def get_ingreso_moto_by_id_pipeline(ingreso_moto_id: str) -> dict:
    return [
    {
        '$match': {
            '_id': {
                '$toObjectId': ingreso_moto_id
            }
        }
    }, {
        '$addFields': {
            'id': {
                '$toString': '$_id'
            }
        }
    }, {
        '$lookup': {
            'from': 'mantenimientos', 
            'localField': 'id', 
            'foreignField': 'id_ingreso', 
            'as': 'mantenimientos'
        }
    }, {
        '$unwind': '$mantenimientos'
    }, {
        '$group': {
            '_id': '$_id', 
            'modelo': {
                '$first': '$id_modelo'
            }, 
            'cliente': {
                '$first': '$id_cliente'
            }, 
            'color': {
                '$first': '$color'
            }, 
            'empleado': {
                '$first': '$id_empleado'
            }, 
            'estado_actual': {
                '$first': '$id_estado_actual'
            }, 
            'fecha_ingreso': {
                '$first': '$fecha_ingreso'
            }, 
            'placa': {
                '$first': '$placa'
            }, 
            'vin': {
                '$first': '$vin'
            }, 
            'es_dueno': {
                '$first': '$es_dueno'
            }, 
            'descripcion': {
                '$first': '$descripcion_ingreso'
            }, 
            'total': {
                '$sum': '$mantenimientos.costo'
            }
        }
    }, {
        '$project': {
            '_id': '$_id', 
            'cliente': '$cliente', 
            'es_dueno': '$es_dueno', 
            'empleado': '$empleado', 
            'estado_actual': '$estado_actual', 
            'fecha_ingreso': '$fecha_ingreso', 
            'descripcion': '$descripcion', 
            'modelo': '$modelo', 
            'placa': '$placa', 
            'color': '$color', 
            'vin': '$vin', 
            'total': '$total'
        }
    }
]