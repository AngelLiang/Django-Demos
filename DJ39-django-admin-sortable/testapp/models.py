from django.db import models

from adminsortable.models import SortableMixin
from adminsortable.fields import SortableForeignKey


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    title = models.CharField(max_length=50)
    ...


class Project(SortableMixin):
    class Meta:
        ordering = ['project_order']

    category = SortableForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)

    # ordering field
    project_order = models.PositiveIntegerField(
        default=0, editable=False, db_index=True)

    def __unicode__(self):
        return self.title
