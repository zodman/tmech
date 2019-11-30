from django.db import models


class ServiceQuerySet(models.QuerySet):
    def paid(self):
        return self.filter(status='p')
    def suma(self):
        ds = self
        l = []
        for i in ds:
            l.append(i.total())
        return sum(l)

    def completed(self):
        return self.filter(status='c')
    def open(self):
        return self.filter(status='o')