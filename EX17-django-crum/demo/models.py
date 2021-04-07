from django.db import models

from crum import get_current_request
from crum import get_current_user


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    remote_addr = models.CharField(blank=True, default='', max_length=32)

    def save(self, *args, **kwargs):
        request = get_current_request()
        if request and not self.remote_addr:
            self.remote_addr = request.META['REMOTE_ADDR']
        super(Comment, self).save(*args, **kwargs)


class Thing(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, blank=True, related_name='+')
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        'auth.User', on_delete=models.CASCADE, blank=True, related_name='+')

    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Thing, self).save(*args, **kwargs)
