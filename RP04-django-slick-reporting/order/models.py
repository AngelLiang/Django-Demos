from django.db import models


class Product(models.Model):
    name = models.CharField('名称', max_length=255)
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_date = models.DateField('订单日期', auto_now_add=True)
    title = models.CharField('标题', max_length=255, default='')
    amount = models.DecimalField('总金额', max_digits=11, decimal_places=2, blank=True, default=0)


class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')

    quantity = models.PositiveSmallIntegerField('数量')
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)
    total = models.DecimalField('总价', max_digits=11, decimal_places=2, blank=True, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.price
        super().save(*args, **kwargs)
