import secrets

from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone


# Create your models here.
class PostModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    author = models.CharField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=16, blank=True, unique=True)


# Create slug
@receiver(pre_save, sender=PostModel)
def create_slug(sender, instance, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)[:8]
        random_part = secrets.token_urlsafe(8)[:8]
        new_slug = f"{base_slug}-{random_part}"

        while PostModel.objects.filter(slug=new_slug).exists():
            random_part = secrets.token_urlsafe(8)[:8]
            new_slug = f"{base_slug}-{random_part}"

        instance.slug = new_slug


pre_save.connect(create_slug, sender=PostModel)
