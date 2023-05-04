from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Libro (BaseModel):
    id: int
    titulo: str
    tipo: int
    autor: Optional[str] = None

libroList = []

@app.post("/libros", response_model=Libro)
def crear_libro(libro: Libro):
    libroList.append(libro)
    return libro

@app.get("/libros", response_model=List[Libro])
def get_libros():
    return libroList

@app.get("/libros/{libro_id}", response_model=Libro)
def obtener_libro (libro_id: int):
    for libro in libroList:
        if libro.id == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="libro no encontrado")

@app.get("/")
def read_root():
    return {"Hello": "Interoperabilidad 2"}
