from .base import BaseManager


class WorkOrderManager(BaseManager):

    def filter_by_creator(self, user):
        return self.filter(created_by=user.username)

    def filter_by_related(self, user):
        return self.filter(created_by=user.username)
