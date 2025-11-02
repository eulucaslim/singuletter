from celery import shared_task
from celery.utils.log import get_task_logger
from core.agent import Agent
from core.models import News, Category
import time

logger = get_task_logger(__name__)

@shared_task
def save_news():
    try:
        agent = Agent() 
        for _ in range(1, 4):
            news_data = agent.get_news()
            category_name = news_data.get("category_name", None)
            
            if not category_name:
                raise Exception("Category not found!")
            
            category, _ = Category.objects.get_or_create(name=category_name)

            news, created = News.objects.get_or_create(
                title=news_data['title'],
                content=news_data['content'],
                category=category
            )
            if created:
                logger.info(f"News created in Database! {news.title}")
            else:
                logger.info(f"News {news.title} already exists!")
            
            # Waiting to create outher news
            time.sleep(5)

        return {"msg": "News Created!!!"}

    except Exception as e:
        raise {"error": f"Error to create a news: {e}"}