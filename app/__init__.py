from fastapi import FastAPI, Form, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from app import database
from app import models

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates('templates')


def get_db(request: Request) -> database.Session:
    request.state.db: database.Session
    return request.state.db


def get_note(db: database.Session, note_id: str) -> models.Note:
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail='Note not found')
    return note


@app.get('/')
async def home(request: Request):
    return templates.TemplateResponse('note_create.html', context={'request': request})


@app.post('/note')
async def note_create(*,
                      title: str = Form(None),
                      body: str = Form(...),
                      db: database.Session = Depends(get_db)):
    note = models.Note(title=title, body=body)
    db.add(note)
    db.commit()
    return RedirectResponse(f'/note/{note.id}')


@app.get('/note/{note_id}')
async def note_view(request: Request, note_id: str, db: database.Session = Depends(get_db)):
    note = get_note(db, note_id)
    return templates.TemplateResponse('note_view.html', context={
        'request': request,
        'note': note,
    })


@app.get('/note/{note_id}/edit')
async def note_edit(request: Request, note_id: str, db: database.Session = Depends(get_db)):
    note = get_note(db, note_id)
    return templates.TemplateResponse('note_create.html', context={'request': request, 'note': note})


@app.post('/note/{note_id}')
async def note_update(note_id: str,
                      title: str = Form(None),
                      body: str = Form(...),
                      db: database.Session = Depends(get_db)):
    note = get_note(db, note_id)
    note.title = title
    note.body = body
    db.add(note)
    db.commit()
    return RedirectResponse(f'/note/{note_id}')


@app.post('/note/{note_id}/delete')
async def note_delete(note_id: str, db: database.Session = Depends(get_db)):
    note = get_note(db, note_id)
    db.delete(note)
    db.commit()
    return RedirectResponse('/')


@app.middleware('http')
async def db_session_middleware(request: Request, call_next: callable):
    response = Response('Internal server error', status_code=500)
    try:
        request.state.db = database.SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
