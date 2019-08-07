from django.db import models


class ServiceQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status='p')
    def completed(self):
        return self.filter(status='c')
    def open(self):
        return self.filter(status='o')