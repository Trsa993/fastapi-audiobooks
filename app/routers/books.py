from fastapi import HTTPException, Depends, APIRouter, status
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db
from typing import Optional, List
from .. import audiobook


router = APIRouter(
    prefix="/books",
    tags=["Books"]
)

@router.get("/", response_model=List[schemas.BookOut])
def get_books(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    books = db.query(models.Book).filter(models.Book.name.contains(search)).limit(limit).offset(skip).all()
    formated_books = []
    for row in books:
        formated_books.append(
            schemas.BookOut(id=row.id, name=row.name, author=row.author)
        )
    return formated_books


@router.get("/{id}", response_class=HTMLResponse)
def get_book(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} is not found")
    audiobook.read_book(book.path, 0)
    return book


@router.put("/{id}")
def get_book(to_do: schemas.BookPlay, id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} is not found")
    if to_do.play == 0:
        audiobook.read()
    elif to_do.play == 1:
        audiobook.pause()
    elif to_do.play == 2:
        audiobook.unpause()
    elif to_do.play == 3:
        audiobook.stop()
    return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)