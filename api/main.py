from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI Agent API")

@app.get("/")
def read_root():
    return {"message": "API activa"}

# Incluimos las rutas de query
app.include_router(router)