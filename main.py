from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import pymongo

cliente = pymongo.MongoClient("mongodb+srv://alexerba:alex2004@cluster0.tghbhkk.mongodb.net/?retryWrites=true&w=majority")
database = cliente ["deber"]
coleccion = database["clientes"]

description = """
Utpl tnteroperabilidad API  crea un cliente, buscar en la base y/o eliminarlo. 

## CLIENTE

Tu puedes agragar un cliente.
Tu puedes listar los clientes registrados.

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
    version="semana 11",
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



class Cliente (BaseModel):
    id: str
    cedula: int 
    nombre: str 
    venta: int 
    item: int 

class ClienteEntrada (BaseModel):
    cedula: int 
    nombre: str 
    venta: int 
    item: int 


clienteList = []

@app.post("/client", response_model=Cliente, tags = ["clientes"])
async def crear_comprador(cliente: ClienteEntrada):
    itemCliente = Cliente (id=str(uuid.uuid4()), cedula = cliente.cedula, nombre = cliente.nombre, venta = cliente.venta, item = cliente.item)
    respuestaBase = coleccion.insert_one(itemCliente.dict())
    return itemCliente

@app.get("/client", response_model=List[Cliente])
def get_comprador():
    return clienteList

@app.get("/client/{cedula_id}", response_model=Cliente)
def obtener_comprador (cedula_id: int):
    for comprador in clienteList:
        if cedula == cedula:
            return comprador
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

@app.get("/")
def read_root():
    return {"Hello": "frase para comprobar deber en la nube"}
