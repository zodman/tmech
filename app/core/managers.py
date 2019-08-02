from django.db import models


class ServiceManager(models.Manager):
    def count_open(self):
        qs = self.get_queryset()
        return qs.filter(status=self.model.STATUS[0]).count()