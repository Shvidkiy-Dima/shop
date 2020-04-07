from django.db import models


class Slides(models.Model):
    image = models.ImageField(upload_to='desing/slides/')

    @property
    def url(self):
        return self.image.url

    def __str__(self):
        return self.image.name