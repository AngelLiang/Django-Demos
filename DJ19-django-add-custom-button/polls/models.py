from django.db import models

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    DRAFT = 'D'
    PUBLISHED = 'P'
    STATUS = (
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
    )
    status = models.CharField(max_length=1, default=DRAFT, choices=STATUS)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
