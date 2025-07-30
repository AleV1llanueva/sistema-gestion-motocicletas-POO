from bson import ObjectId
from fastapi import HTTPException

def get_ingreso_moto_by_id_pipeline(ingreso_moto_id: str) -> dict:
    return [{
            '$match': {
                '$expr': {
                    '$eq': ['$_id', { '$toObjectId': ingreso_moto_id }]
                }
            }
        },

    {
        '$addFields': {
            'motocicleta': '', 
            'id_modelos_obj': {
                '$toObjectId': '$id_modelo'
            }
        }
    }, {
        '$lookup': {
            'from': 'modelos', 
            'localField': 'id_modelos_obj', 
            'foreignField': '_id', 
            'as': 'modelo_obj'
        }
    }, {
        '$unwind': '$modelo_obj'
    }, {
        '$addFields': {
            'id_motocicleta_obj': {
                '$toObjectId': '$modelo_obj.id_motocicleta'
            }, 
            'id_categoria_obj': {
                '$toObjectId': '$modelo_obj.id_categoria'
            }
        }
    }, {
        '$lookup': {
            'from': 'motorcycles', 
            'localField': 'id_motocicleta_obj', 
            'foreignField': '_id', 
            'as': 'motocicleta_obj'
        }
    }, {
        '$unwind': '$motocicleta_obj'
    }, {
        '$lookup': {
            'from': 'categorias', 
            'localField': 'id_categoria_obj', 
            'foreignField': '_id', 
            'as': 'categoria_obj'
        }
    }, {
        '$unwind': '$categoria_obj'
    }, {
        '$addFields': {
            'id_marca_obj': {
                '$toObjectId': '$motocicleta_obj.id_marca'
            }, 
            'id': {
                '$toString': '$_id'
            }
        }
    }, {
        '$lookup': {
            'from': 'brands', 
            'localField': 'id_marca_obj', 
            'foreignField': '_id', 
            'as': 'marca_obj'
        }
    }, {
        '$unwind': '$marca_obj'
    }, {
        '$lookup': {
            'from': 'recomendaciones', 
            'localField': 'id', 
            'foreignField': 'id_ingreso_moto', 
            'as': 'recomendacion_obj'
        }
    }, {
        '$unwind': '$recomendacion_obj'
    }, {
        '$lookup': {
            'from': 'mantenimientos', 
            'localField': 'id', 
            'foreignField': 'id_ingreso', 
            'as': 'mantenimientos_obj'
        }
    }, {
        '$unwind': '$mantenimientos_obj'
    }, {
        '$addFields': {
            'id_cliente_obj': {
                '$toObjectId': '$id_cliente'
            }, 
            'id_empleado_obj': {
                '$toObjectId': '$id_empleado'
            }
        }
    }, {
        '$lookup': {
            'from': 'users', 
            'localField': 'id_cliente_obj', 
            'foreignField': '_id', 
            'as': 'cliente_obj'
        }
    }, {
        '$unwind': '$cliente_obj'
    }, {
        '$lookup': {
            'from': 'empleados', 
            'localField': 'id_empleado_obj', 
            'foreignField': '_id', 
            'as': 'empleado_obj'
        }
    }, {
        '$unwind': '$empleado_obj'
    }, {
        '$addFields': {
            'id_user_empleado': {
                '$toObjectId': '$empleado_obj.id_usuario'
            }
        }
    }, {
        '$lookup': {
            'from': 'users', 
            'localField': 'id_user_empleado', 
            'foreignField': '_id', 
            'as': 'user_empleado_obj'
        }
    }, {
        '$unwind': '$user_empleado_obj'
    }, {
        '$group': {
            '_id': '$_id', 
            'cliente': {
                '$first': {
                    '$concat': [
                        '$cliente_obj.name', ' ', '$cliente_obj.lastname'
                    ]
                }
            }, 
            'motocicleta': {
                '$first': {
                    '$concat': [
                        '$marca_obj.description', ' ', '$motocicleta_obj.name', ' ', '$modelo_obj.nombre'
                    ]
                }
            }, 
            'estado_act': {
                '$first': '$estado'
            }, 
            'empleado': {
                '$first': '$id_empleado'
            }, 
            'mantenimientos': {
                '$push': '$mantenimientos_obj'
            }, 
            'costo': {
                '$sum': '$mantenimientos_obj.costo'
            }, 
            'recomendacion': {
                '$first': '$mantenimientos_obj.description'
            }
        }
    },{
  '$addFields': {
    'mantenimientos': {
      '$map': {
        'input': '$mantenimientos',
        'as': 'm',
        'in': {
          'id_ingreso': '$$m.id_ingreso',
          'id_empleado': '$$m.id_empleado',
          'id_tipo_mantenimiento': '$$m.id_tipo_mantenimiento',
          'description': '$$m.description',
          'costo': '$$m.costo'
        }
      }
    }
  }
}

    
    ,{
        '$project': {
            '_id': 0,
            'id': 1,
            'cliente': 1,
            'motocicleta': 1,
            'estado_act': 1,
            'empleado': 1,
            'mantenimientos': 1,
            'costo': 1,
            'recomendacion': 1
        }
    }
]