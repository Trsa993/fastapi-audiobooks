# **Audiobooks**

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

### _This is FastAPI project for audiobooks._

<br>

## Project description

---

In this project, API is connected to the Postgresql database where data about created users and books is stored. In the Books table, there is a column named path which represents the link to the book PDF. PDFs can be stored for example in some cloud-based storage like Google Drive. File [audiobook.py](app/audiobook.py) is the main one for PDF processing and playing audiobooks.

For PDF processing, module [PyMuPDF](https://pymupdf.readthedocs.io/en/latest/intro.html) is used and for text to speech conversion [pyttsx3](https://pyttsx3.readthedocs.io/en/latest/).

There are four options for audiobook:

- Play - Read book aloud
- Pause - Pause reading
- Resume - Unpause reading
- Stop - Completely stop reading, return to first page of the book

## Requirements

These [requirements](requirements.txt) are meant for Windows development. When using something different like Linux or Mac there are some slight changes.

## How to use

Run project on localhost using _uvicorn app.main:app_ (with optional --reload).
When the project is succesfully started go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Every path operation is dependent on database connection.

To be able to use audiobook functions there must be a user created in the database. User must also be logged in.

After logging in, use get request with an ID of desired book stored in the database and then from put method use the same ID and choose play from the dropdown list.

## Next steps

This project will work on development, but for it to work on production server it is best to use some frontend framework that will process text to speech. For example, FastAPI will process PDF and then React will use that text to create text to speech conversion.
