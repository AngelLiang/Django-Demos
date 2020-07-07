from django.db import models


class Product(models.Model):
    name = models.CharField("Product name", max_length=255)
    value = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
    date = models.DateField(auto_now_add=True, verbose_name='Data do Cadastro')

    PAYMENT_TYPE = (
        (1, "现金"),
        (2, "信用卡"),
        (3, "银行转账"),
    )

    payment_type = models.PositiveSmallIntegerField(
        '付款类型',
        default=None, choices=PAYMENT_TYPE, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    total_value = models.DecimalField(max_digits=11, decimal_places=2)

    email = models.EmailField(null=True, blank=True)

    GENDER = (
        (0, "男"),
        (1, "女")
    )
    gender = models.NullBooleanField(choices=GENDER, null=True, blank=True, default=None)

    def __str__(self):
        return f'[{self.id}]{self.date}'


class OrderItem(models.Model):
    class Meta:
        verbose_name = "Order Iten"
        verbose_name_plural = "Order Itens"

    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField('数量')
    value = models.DecimalField('单价', max_digits=11, decimal_places=2)
    total = models.DecimalField('总金额', max_digits=11, decimal_places=2, blank=True, default=0)

    def save(self, *args, **kwargs):
        self.total = self.quantity * self.value
        super().save(*args, **kwargs)


class OrderProxy(Order):
    class Meta:
        verbose_name = "Report Order"
        verbose_name_plural = 'Report Orders'
        proxy = True


class ProductProxy(Product):
    class Meta:
        verbose_name = "Report Order Item"
        verbose_name_plural = 'Report Order Items'
        proxy = True
