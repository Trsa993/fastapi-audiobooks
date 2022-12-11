from fastapi import HTTPException, Depends, APIRouter, status, BackgroundTasks
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


@router.get("/{id}", response_model=schemas.BookOut)
def get_book(id: int, background_task: BackgroundTasks, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} is not found")
    background_task.add_task(audiobook.read_book, book.path, 0)
    return book


@router.post("/{id}")
def choose_page(page: schemas.BookPage, id: int, background_task: BackgroundTasks, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} is not found")
    background_task(audiobook.read_book, book.path, page.page)
    if page.page > audiobook.num_of_pages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"page {page.page} does not exist")
    return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def play_audiobook(command: schemas.BookCommands, id: int, background_task: BackgroundTasks, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"book with id {id} is not found")
    if command is command.play:
        audiobook.read()
    elif command is command.pause:
        audiobook.pause()
    elif command is command.resume:
        audiobook.unpause()
    elif command is command.stop:
        audiobook.stop()
        background_task.add_task(audiobook.read_book, book.path, 0)
    return HTMLResponse(status_code=status.HTTP_204_NO_CONTENT)