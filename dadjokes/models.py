from django.db import models

# Create your models here.


class Joke(models.Model):
    '''Text of a joke'''
    text = models.TextField()
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text if self.name else f"Joke {self.id}"

class Picture(models.Model):
    '''Silly image or URL'''
    url = models.URLField(blank=True, null=True)
    name = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url if self.name else f"Picture {self.id}"