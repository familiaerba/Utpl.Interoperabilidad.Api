from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Comprador (BaseModel):
    cedula: int 
    nombre: str 
    venta: int 
    item: int 

compradorList = []

@app.post("/comprador", response_model=Comprador)
def crear_comprador(cliente: Comprador):
    compradorList.append(cliente)
    return cliente

@app.get("/comprador", response_model=List[Comprador])
def get_comprador():
    return compradorList

@app.get("/comprador/{cedula_id}", response_model=Comprador)
def obtener_comprador (cedula_id: int):
    for comprador in compradorList:
        if cedula == cedula:
            return comprador
    raise HTTPException(status_code=404, detail="Persona no encontrada")

@app.get("/")
def read_root():
    return {"Hello": "frase para comprobar deber"}
