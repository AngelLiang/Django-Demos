from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    name = models.CharField('标签名', max_length=32)

    def __str__(self):
        return self.name


class Post(models.Model):
    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#charfield
    title = models.CharField('标题', max_length=128)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#slugfield
    slug = models.SlugField(blank=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#textfield
    content = models.TextField('内容', default='')

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#booleanfield
    is_delete = models.BooleanField('已删除', default=False)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#datefield
    create_date = models.DateField('创建日期', auto_now_add=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#timefield
    # DateField.auto_now_add: Automatically set the field to now when the object is first created.
    create_time = models.TimeField('创建时间', auto_now_add=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#datetimefield
    # DateField.auto_now: Automatically set the field to now every time the object is saved.
    update_datetime = models.DateTimeField('更新时间', auto_now=True)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#integerfield
    view_count = models.IntegerField('浏览次数', default=0)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#decimalfield
    money = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, default=Decimal('0.0')
    )

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#floatfield
    price = models.FloatField(blank=True, default=0.0)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#foreignkey
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # https://docs.djangoproject.com/en/3.0/ref/models/fields/#manytomanyfield
    tags = models.ManyToManyField(Tag)

    DRAFT = 'd'
    PUBLISHED = 'p'
    WITHDRAWN = 'w'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published'),
        (WITHDRAWN, 'Withdrawn'),
    ]
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-update_datetime']
