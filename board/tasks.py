from datetime import datetime, timedelta
from django.utils import timezone
from celery import shared_task
import time
from .models import Order

@shared_task
def complete_order(oid):
    """Заказ завершён (флаг True)"""
    order = Order.objects.get(pk=oid)
    order.complete = True
    order.save()

@shared_task
def clear_old():
    """Удаление неактуальных заказов"""
    old_orders = Order.objects.all().exclude(time_in__gt=timezone.now() - timedelta(minutes=5))
    old_orders.delete()