from models.tipo_empleado import TipoEmpleado
from utils.mongodb import get_collection
from fastapi import HTTPException
from bson import ObjectId

coll = get_collection("tipos_empleado")  # Obtiene la colección de tipos de empleados desde MongoDB

async def create_tipo_empleado(tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    try:
        tipo_empleado.descripcion = tipo_empleado.descripcion.strip().lower() # Normaliza la descripción del tipo de    empleado

        existing_tipo_empleado = coll.find_one({"descripcion": tipo_empleado.descripcion})
        if existing_tipo_empleado:
            raise HTTPException(status_code=400, detail="El tipo de empleado ya existe")

        tipo_empleado_dict = tipo_empleado.model_dump(exclude={"id"})
        inserted = coll.insert_one(tipo_empleado_dict)
        tipo_empleado.id = str(inserted.inserted_id)
        return tipo_empleado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_tipo_empleados() -> list[TipoEmpleado]:
    try:
        tipo_empleados = []
        for tipo_empleado in coll.find(): #Busca todos los tipos de empleados en la colección
            # Convierte el ObjectId de MongoDB a string y elimina el campo _id
            # coll.find() devuelve un cursor, que es un iterable de documentos
            tipo_empleado["id"] = str(tipo_empleado["_id"])
            del tipo_empleado["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto TipoEmpleado
            tipo_empleados.append(TipoEmpleado(**tipo_empleado))
        return tipo_empleados
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_tipo_empleado_by_id(tipo_empleado_id: str) -> TipoEmpleado:
    try:
        tipo_empleado = coll.find_one({"_id": ObjectId(tipo_empleado_id)})
        if not tipo_empleado:
            raise HTTPException(status_code=404, detail="Tipo de empleado no encontrado")

        tipo_empleado["id"] = str(tipo_empleado["_id"])
        del tipo_empleado["_id"] # Eliminar el campo _id de MongoDB al momento de crear el objeto TipoEmpleado
        return TipoEmpleado(**tipo_empleado)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_tipo_empleado(tipo_empleado_id: str, tipo_empleado: TipoEmpleado) -> TipoEmpleado:
    try:
        tipo_empleado.descripcion = tipo_empleado.descripcion.strip().lower()
        # Verifica si ya existe un tipo de empleado con la misma descripción, excepto el que se está actualizando
        existing_tipo_empleado = coll.find_one({"descripcion": tipo_empleado.descripcion, "_id": {"$ne": ObjectId(tipo_empleado_id)}}) # $ne significa "no igual a"
        # Verifica si ya existe un tipo de empleado con la misma descripción, excepto el que se está actualizando
        if existing_tipo_empleado: # Si ya existe un tipo de empleado con la misma descripción, se lanza una excepción
            raise HTTPException(status_code=400, detail="El tipo de empleado ya existe")

        result = coll.update_one(
            {"_id": ObjectId(tipo_empleado_id)},
            {"$set": tipo_empleado.model_dump(exclude={"id"})}
        )
        
        # Si no se actualizó ningún documento, significa que no se encontró la marca
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Tipo de empleado no encontrado")

        tipo_empleado.id = tipo_empleado_id
        return tipo_empleado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_tipo_empleado(tipo_empleado_id: str) -> TipoEmpleado: # Eliminar un tipo de empleado por su ID
    try:
        coll_empleado = get_collection("empleados")  # Obtiene la colección de empleados desde MongoDB
        # Verifica si hay empleados asociados a este tipo de empleado
        existing_empleados = coll_empleado.find_one({"tipo_empleado_id": ObjectId(tipo_empleado_id)})
        if existing_empleados:
            raise HTTPException(status_code=400, detail="No se puede eliminar el tipo de empleado porque hay empleados asociados a él")
        
        result = coll.delete_one({"_id": ObjectId(tipo_empleado_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Tipo de empleado no encontrado")

        return {"message": "Tipo de empleado eliminado exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))