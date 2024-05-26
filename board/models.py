from django.db import models

class Product(models.Model):
    """Продукт"""
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.FloatField(default=0.0, verbose_name='Цена')

    def __str__(self):
        """Строковое представление"""
        return f'{self.name } | {str(self.price)}₽'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

class Order(models.Model):
    """Заказ"""
    time_in = models.DateTimeField(auto_now_add=True, verbose_name='Заказ оформлен') # дата и время оформления заказа
    time_out = models.DateTimeField(null=True, verbose_name='Заказ выдан') # дата и время выдачи заказа
    cost = models.FloatField(default=0.0, verbose_name='Стоимость') # общая стоимость заказа
    take_away = models.BooleanField(default=False, verbose_name='Доставка по адресу') # самовывоз - False, доставка - True
    complete = models.BooleanField(default=False, verbose_name='Заказ выполнен') # заказ выполнен - True, заказ не выполнен - False

    products = models.ManyToManyField(Product, through='ProductOrder')

    class Meta:
        ordering = ('-time_in',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.pk}'

class ProductOrder(models.Model):
    """ ~~ Промежуточная таблица ~~ """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_in')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.IntegerField(default=1, db_column='amount') # количество продуктов в заказе
