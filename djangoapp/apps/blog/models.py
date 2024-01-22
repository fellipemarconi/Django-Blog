from django.db import models
from utils.rands import new_slugify

# Create your models here.
class Tag(models.Model):
    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(
        unique=True, default=None, null=True, blank=True,
        max_length=100
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = new_slugify(self.name, 4)
        return super().save(*args, **kwargs)