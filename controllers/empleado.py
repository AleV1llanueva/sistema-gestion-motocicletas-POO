import logging
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

from pipelines.empleado_pipeline import validate_user_pipeline

from models.empleado import Empleado

coll = get_collection("empleados")

async def create_empleado(empleado: Empleado) -> dict:
    try:
        #Verificacion de que ningun otro empleado tenga al referencia al usuario
        existing_empleado = coll.find_one({"id_usuario":empleado.id_usuario})
        if existing_empleado:
            raise HTTPException(status_code=400, detail="El usuario ya esta asociado a otro empleado")
        
        coll_users = get_collection("users")
        
        #Validar que existe el usuario y que este activo
         
        user_validate_pipeline = validate_user_pipeline(empleado.id_usuario)
        existing_user = list(coll_users.aggregate(user_validate_pipeline))
        
        
        if not existing_user:
            raise HTTPException(status_code=404, detail="El usuario de referencia no existe o no esta activo ")

        # existing_user = coll_users.find_one({"_id": ObjectId(empleado.id_usuario)})
        
        # if not existing_user:
        #     raise HTTPException(status_code=404, detail="Usuario no encontrado, no podemos registrar el empleado")
        
        #Verificar que existe el tipo de emppleado
        coll_tipos_empleados = get_collection("tipos_empleado")
        existing_tipo_empleado = coll_tipos_empleados.find_one({"_id": ObjectId(empleado.id_tipo_empleado)})
        if not existing_tipo_empleado:
            raise HTTPException(status_code=404, detail="Tipo de empleado no encontrado")
        
        empleado_dict = empleado.model_dump(exclude={"id"})
        inserted = coll.insert_one(empleado_dict)
        empleado.id = str(inserted.inserted_id)
        
        for user in existing_user:
            user.pop('_id', None)  # elimina el campo si existe
        
        return {
            "message" : "Empleado creado correctamente",
            "info_empleado" : empleado,
            "info_user" : existing_user
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def delete_empleado(empleado_id: str) -> Empleado:
    try:
        result = coll.find_one({"_id": ObjectId(empleado_id)})
        
        if not result:
            raise HTTPException(status_code=404, detail="Empleado no encontrado")
        
        result = coll.update_one({"_id":ObjectId(empleado_id)}, {"$set" : {"active": False}})
        
        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No se pudo eliminar el usuario")
        
        return {"message": "Empleado eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
async def get_empleados(telefono: str = None) -> dict:
    try:
        if telefono:
            #Buscar empleado por numero de telefono
            empleado_exist = coll.find_one({"telefono" : telefono})
            if not empleado_exist:
                return{
                    "success" : False,
                    "message" : "Empleado no encontrado",
                    "data" : None
                }
            else:
                empleado_exist['id'] = str(empleado_exist['_id'])
                del empleado_exist['_id']
                empleado_doc = Empleado(**empleado_exist)
                return{
                    "success" : True,
                    "message" : "El empleado a sido encontrado",
                    "data": empleado_doc
                }
        empleados = []
        for doc in coll.find():
            doc['_id'] = str(doc['_id'])
            del doc['_id']
            empleado = Empleado(**doc)
            empleados.append(empleado)
        
        if not empleados:
            return {
                "success" : False,
                "message" : "No se encontro ningun empleado",
                "data" : None
            }
            
        return {
            "success" : True,
            "message" : "Se ha recibido la lista de empleados",
            "data" : empleados
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))