from app.config.settings import API_PORT
from app.routers import ai
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
import uvicorn

app = FastAPI(title='AI Agent API')
app.include_router(ai.router)

@app.get("/")
def main(request: Request):
    if request.method == "GET":
        return RedirectResponse(url='/docs')


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=API_PORT, reload=True)