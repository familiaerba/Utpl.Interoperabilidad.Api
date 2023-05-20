from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Cliente (BaseModel):
    cedula: int 
    nombre: str 
    venta: int 
    item: int 

clienteList = []

@app.post("/client", response_model=Cliente)
def crear_comprador(cliente: Cliente):
    clienteList.append(cliente)
    return cliente

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
