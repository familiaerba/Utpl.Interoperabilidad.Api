from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
import uuid
import pymongo

from fastapi_versioning import VersionedFastAPI, version
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from auth import authenticate
cliente = pymongo.MongoClient("mongodb+srv://alexerba:alex2004@cluster0.tghbhkk.mongodb.net/?retryWrites=true&w=majority")
database = cliente ["deber"]
coleccion = database["clientes"]

description = """
Utpl tnteroperabilidad API  crea un cliente, buscar en la base y/o eliminarlo. 

## Cliente

 agragar un cliente.
 listar los clientes registrados.

"""
tags_metadata = [
    {
        "name":"cliente",
        "description":"Permite realizar un crud completo de un cliente registrado en el comercio (listar)"
    }
]

app = FastAPI(
    title="Utpl Interoperabilidad APP",
    description= description,
    version="tarea",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Alexander Erba",
        "url": "https://github.com/familiaerba/Utpl.Interoperabilidad.Api.git",
        "email": "familia-erba@hotmail.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    }, 
    openapi_tags = tags_metadata   
)

#para agregar seguridad a nuestro api
security = HTTPBasic()
class ClienteRepositorio (BaseModel):
    id: str
    nombre: str
    cantPro: int
    cedula: Optional[str] = None
    ciudad: Optional[str] = None

class ClienteEntrada (BaseModel):
    nombre:str
    cantPro:int
    ciudad: Optional[str] = None

class ClienteEntradaV2 (BaseModel):
    nombre:str
    cantPro:int
    cedula:str
    ciudad: Optional[str] = None




clienteList = []

@app.post("/cliente", response_model=ClienteRepositorio, tags = ["cliente"])
@version(1, 0)
async def crear_cliente(clienteE: ClienteEntrada):
    itemcliente = ClienteRepositorio (id= str(uuid.uuid4()), nombre = clienteE.nombre, cantPro = clienteE.cantPro, ciudad = clienteE.ciudad)
    resultadoDB =  coleccion.insert_one(itemcliente.dict())
    return itemcliente

@app.post("/cliente", response_model=ClienteRepositorio, tags = ["cliente"])
@version(2, 0)
async def crear_Clientev2(clienteE: ClienteEntradaV2):
    itemcliente = ClienteRepositorio (id= str(uuid.uuid4()), nombre = clienteE.nombre, cantPro = clienteE.cantPro, ciudad = clienteE.ciudad, cedula = clienteE.cedula)
    resultadoDB =  coleccion.insert_one(itemcliente.dict())
    return itemcliente


@app.get("/cliente", response_model=List[ClienteRepositorio], tags=["cliente"])
@version(1, 0)
def get_Cliente():
    items = list(coleccion.find())
    print (items)
    return items

@app.get("/cliente/{cliente_id}", response_model=ClienteRepositorio , tags=["cliente"])
@version(1, 0)
def obtener_Cliente (cliente_id: str):
    item = coleccion.find_one({"id": cliente_id})
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrada")

@app.delete("/cliente/{cliente_id}", tags=["cliente"])
@version(1, 0)
def eliminar_Cliente (cliente_id: str):
    result = coleccion.delete_one({"id": cliente_id})
    if result.deleted_count == 1:
        return {"mensaje": "Cliente eliminada exitosamente"}
    else:
        raise HTTPException(status_code=404, detail="Cliente no encontrada")
   

@app.get("/")
def read_root():
    return {"Hello": "frase para comprobar deber en la nube 2"}

app = VersionedFastAPI(app)