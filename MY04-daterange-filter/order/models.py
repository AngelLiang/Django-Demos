from django.db import models
from django.db.models import Sum


class Customer(models.Model):
    name = models.CharField('姓名', max_length=255)
    phone = models.CharField('联系电话', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '客户'
        verbose_name_plural = '客户'


class Product(models.Model):
    name = models.CharField('名称', max_length=255)
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = '产品'
        verbose_name_plural = '产品'


class Order(models.Model):
    code = models.CharField('订单号', max_length=40, default='', blank=True)
    order_date = models.DateField('订单日期')
    title = models.CharField('标题', max_length=255, default='')
    description = models.TextField('描述说明', max_length=10000, default='')
    amount = models.DecimalField('总金额', max_digits=11, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField('创建时间')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name='客户')

    def __str__(self):
        return f'[{self.id}]{self.order_date}'

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'

    def update_amount(self, commit=True):
        self.amount = OrderItem.objects.filter(order=self).aggregate(Sum('amount')).get('amount__sum')
        if commit:
            self.save(update_fields=['amount'])

    def update_code(self, prefix='D', number_width=4, commit=True):
        if self.code is None or len(self.code) == 0:
            fmt = f'%s%0{number_width}d'
            # 生成code，这里需要获取obj的id，所以需要先保存
            code = fmt % (prefix, self.id)
            self.code = code
            if commit:
                self.save(update_fields=['code'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='订单', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='产品')

    quantity = models.PositiveSmallIntegerField('数量')
    price = models.DecimalField('单价', max_digits=11, decimal_places=2)
    amount = models.DecimalField('总价', max_digits=11, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.amount = self.quantity * self.price
        super().save(*args, **kwargs)
        self.order.update_amount()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.order.update_amount()

    class Meta:
        verbose_name = '订单明细'
        verbose_name_plural = '订单明细'
        default_permissions = ()
