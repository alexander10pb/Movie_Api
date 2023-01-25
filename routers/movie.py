from fastapi import APIRouter
from fastapi import Depends ,Path, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from config.database import Session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.jwt_bearer import JWTBearer
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model= list[Movie], status_code= 200, dependencies=[Depends(JWTBearer())])
def get_movies() -> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies_service()
    return JSONResponse(status_code= 200, content=jsonable_encoder(result))

@movie_router.get('/movies/{id}', tags=['movies'], response_model= list[Movie])
def get_movie(id: int = Path(ge = 1, le = 2000)) -> Movie:
    db = Session()
    result = MovieService(db).get_movie_service(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Query
@movie_router.get('/movies/', tags=['movies'], response_model= list[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length= 15)) -> list[Movie]:
    db = Session()
    result = MovieService(db).get_movies_by_category_service(category=category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(content=jsonable_encoder(result))

@movie_router.post('/movies/', tags=['movies'], response_model= dict, status_code=201)
def create_movies(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie_service(movie)
    return JSONResponse(status_code= 201 ,content= {"message": "Se ha registrado la pelicula"})

@movie_router.put('/movies/{id}', tags=['movies'], response_model= dict, status_code= 200)
def update_movies(id: int, movie: Movie) -> dict:
    db = Session()
    result = MovieService(db).get_movie_service(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).update_movie_service(id, movie)
    return JSONResponse(status_code= 200, content= {"message": "Se ha modificado la pelicula"})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model= dict, status_code= 200)
def delete_movies(id: int) -> dict:
    db = Session()
    result = MovieService(db).get_movie_service(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    MovieService(db).delete_movie_service(id)
    return JSONResponse(status_code= 200, content= {"message": "Se ha eliminado la pelicula"})