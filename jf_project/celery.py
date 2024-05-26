from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jf_project.settings') # связь настройки Django с настройками Celery через переменную окружения

app = Celery('jf_project') # файл конфигурации для экземпляра
app.config_from_object('django.conf:settings', namespace='CELERY') # указываем пространство имён, \
# чтобы Celery сам находил все необходимые настройки в общем конфигурационном файле settings.py \
# поиск будет осуществляться по шаблону CELERY_***

app.autodiscover_tasks() # указываем Celery авторматически искать задания в файлах tasks.py \
# каждого приложения проекта.

# выполнение периодической задачи по удалению неактуальных заказов каждую минуту
app.conf.beat_schedule = {
    'clear_board_every_minute': {
        'task': 'board.tasks.clear_old',
        'schedule': crontab(),
    },
}