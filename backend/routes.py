from typing import List

from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder

from models import Fact, FactUpdate

router = APIRouter()


@router.post("/", response_description="Add new fact", status_code=status.HTTP_201_CREATED, response_model=Fact)
def create_fact(request: Request, fact: Fact = Body(...)):
    fact = jsonable_encoder(fact)
    new_fact = request.app.database["facts"].insert_one(fact)
    created_fact = request.app.database["facts"].find_one(
        {"_id": new_fact.inserted_id}
    )

    return created_fact


@router.get("/", response_description="List all known facts", response_model=List[Fact])
def list_facts(request: Request):
    facts = list(request.app.database["facts"].find(limit=100))
    return facts


@router.get("/{id}", response_description="Get a fact by id", response_model=Fact)
def find_fact(id: str, request: Request):
    if (fact := request.app.database["facts"].find_one({"_id": id})) is not None:
        return fact
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


@router.put("/{id}", response_description="Update a fact", response_model=Fact)
def update_fact(id: str, request: Request, fact: FactUpdate = Body(...)):
    fact = {k: v for k, v in fact.dict().items() if v is not None}
    if len(fact) >= 1:
        update_result = request.app.database["facts"].update_one(
            {"_id": id}, {"$set": fact}
        )

        if update_result.modified_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fact with ID {id} not found")

    if (
            existing_fact := request.app.database["facts"].find_one({"_id": id})
    ) is not None:
        return existing_fact

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fact with ID {id} not found")


@router.delete("/{id}", response_description="Delete a fact")
def delete_fact(id: str, request: Request, response: Response):
    delete_result = request.app.database["facts"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Fact with ID {id} not found")
