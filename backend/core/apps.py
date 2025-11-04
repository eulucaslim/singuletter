from datetime import timedelta
from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.contrib.auth import get_user_model
from setup.settings import USER_ADMIN
import json
import random
class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        post_migrate.connect(create_default_superuser, sender=self)
        post_migrate.connect(create_periodic_tasks, sender=self)
        post_migrate.connect(create_default_data, sender=self)

def create_default_superuser(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(username=USER_ADMIN["username"]).exists():
        User.objects.create_superuser(
            username=USER_ADMIN["username"],
            email=USER_ADMIN["email"],
            password=USER_ADMIN["password"]
        )
        print("Superuser created!")

def create_default_data(sender, **kwargs):
    from core.models import Category, News
    from django.utils import timezone

    if not Category.objects.exists():
        categories = [
            Category(name='Inteligência Artificial'),
            Category(name='Programação'),
            Category(name='Startups'),
            Category(name='Cibersegurança'),
            Category(name='Gadgets'),
        ]
        Category.objects.bulk_create(categories)

    if not News.objects.exists():
        # Create with outher days
        random_days = random.randint(0, 30)
        random_date = timezone.now() - timedelta(days=random_days)
        categories = {cat.name: cat for cat in Category.objects.all()}

        News.objects.bulk_create([
            News(
                title="OpenAI lança novo modelo de IA revolucionário",
                content="A OpenAI apresentou um novo modelo de linguagem capaz de entender e gerar código em múltiplas linguagens de forma mais eficiente.",
                category=categories['Inteligência Artificial'],
                created_at=random_date
            ),
            News(
                title="Python 3.13 traz melhorias de performance impressionantes",
                content="A nova versão do Python apresenta otimizações internas que reduzem o tempo de execução em até 30%.",
                category=categories['Programação'],
                created_at=random_date
            ),
            News(
                title="Startup brasileira recebe investimento milionário em fintech",
                content="A fintech FlowBank recebeu um aporte de R$ 25 milhões para expandir suas operações no mercado latino-americano.",
                category=categories['Startups'],
                created_at=random_date
            ),
            News(
                title="Novo malware se espalha via e-mails falsos de suporte técnico",
                content="Pesquisadores identificaram uma campanha de phishing que utiliza e-mails falsos para roubar credenciais corporativas.",
                category=categories['Cibersegurança'],
                created_at=random_date
            ),
            News(
                title="Google apresenta smartphone com IA embarcada",
                content="O novo Pixel traz recursos de geração de texto, tradução instantânea e edição inteligente de imagens diretamente no dispositivo.",
                category=categories['Gadgets'],
                created_at=timezone.now()
            ),
        ])

def create_periodic_tasks(sender, **kwargs):
    """Create or update periodic Celery Beat tasks after migrations."""
    from django_celery_beat.models import PeriodicTask, CrontabSchedule
    try:
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='*',
            day_of_week='1,2,3,4,5',
            timezone='America/Sao_Paulo',
        )

        PeriodicTask.objects.update_or_create(
            name='save_news_periodic_task',
            defaults={
                'task': 'core.tasks.save_news',
                'crontab': schedule,
                'args': json.dumps([]),
                'enabled': True,
            },
        )

        print("✅ Periodic task 'save_news_periodic_task' created or updated successfully.")
    except Exception as e:
        print(f"⚠️ Could not create periodic task: {e}")