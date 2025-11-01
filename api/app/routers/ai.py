from app.lib.agent import Agent
from app.models.prompt import Prompt
from app.models.news import News
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

router = APIRouter(tags=['AI Agent'])
ai = Agent()

@router.post("/resume")
def message(prompt: Prompt):
    try:
        response = ai.generate_response(prompt.message)
        return JSONResponse({"data": response}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"msg": str(e)}, status_code=400)

@router.get("/generate-news", response_model=News)
def generate_news(request: Request):
    try:
        if request.method == "GET":
            generated_news = ai.generate_news()
            news_data: News = ai.format_news(generated_news)
            return news_data
    except (Exception, Agent.GenerateError) as e:
        return JSONResponse(content={"msg": str(e)}, status_code=400)