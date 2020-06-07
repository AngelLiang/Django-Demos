from django.db import models
from django.dispatch import receiver
from django.db.models.signals import (
    post_save, post_delete,
    pre_save, pre_delete,
)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


@receiver(pre_save, sender=Question)
def question_pre_save(sender, instance, **kwargs):
    print('pre_save')
    if instance.id:
        print(instance.id)


@receiver(pre_delete, sender=Question)
def question_pre_delete(sender, instance, **kwargs):
    print('pre_delete')


@receiver(post_save, sender=Question)
def question_post_save(sender, instance, **kwargs):
    print('post_save')
    if instance.id:
        print(instance.id)


@receiver(post_delete, sender=Question)
def question_post_delete(sender, instance, **kwargs):
    print('post_delete')
