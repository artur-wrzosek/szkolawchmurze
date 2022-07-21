from django.db import models


class ShortURL(models.Model):
    short = models.SlugField(primary_key=True, max_length=50, editable=True)
    target_url = models.URLField()
