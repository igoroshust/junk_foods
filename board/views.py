from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView, CreateView
from .tasks import complete_order, clear_old
from .models import Order
from datetime import datetime
from django.utils import timezone

class IndexView(TemplateView):
    """Главная страница - таблица заказов"""
    template_name = 'board/index.html'

    def get_context_data(self, **kwargs):
        """Передача информации в шаблон (заполнение словаря)"""
        context = super().get_context_data(**kwargs)
        context['orders'] = Order.objects.all()
        return context

class NewOrderView(CreateView):
    """Форма нового заказа"""
    model = Order
    fields = ['products'] # единственное поле
    template_name = 'board/new.html'

    def form_valid(self, form):
        """Валидация формы"""
        order = form.save() # сохраняем объект
        order.cost = sum([prod.price for prod in order.products.all()]) # считаем его общую стоимость
        order.save()
        complete_order.apply_async([order.pk], countdown=60) # завершаем заказ через минуту после вызова
        return redirect('/')

def take_order(request, oid):
    """Кнопка 'забрать заказ'"""
    order = Order.objects.get(pk=oid)
    order.time_out = timezone.now()
    order.save()
    return redirect('/')
