from fastapi import FastAPI, Request, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from database import get_db, User
import logging

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Configuration des templates
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "Détecteur de Spam",
            "heading": "Votre message est-il un spam ?"
        }
    )

@app.get("/users", response_class=HTMLResponse)
async def get_users(request: Request, db: Session = Depends(get_db)):
    try:
        users = db.query(User).all()
        logger.info(f"Nombre d'utilisateurs trouvés: {len(users)}")
        
        return templates.TemplateResponse(
            "user.html", 
            {
                "request": request, 
                "users": users,
                "title": "Liste des utilisateurs"
            }
        )
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        return templates.TemplateResponse(
            "user.html", 
            {
                "request": request, 
                "users": [],
                "error": "Erreur lors de la récupération des utilisateurs"
            }
        )

@app.post("/resultats", response_class=HTMLResponse)
async def check_message(request: Request, message: str = Form(...)):
    try:
        return templates.TemplateResponse(
            "resultats.html",
            {
                "request": request,
                "message": message,
                "result": "Message reçu (traitement à implémenter)"
            }
        )
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "title": "Erreur",
                "heading": "Une erreur est survenue",
                "error": str(e)
            }
        ) 