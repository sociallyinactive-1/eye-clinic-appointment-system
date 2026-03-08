from django.db import models
from django.contrib.auth import  get_user_model
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.conf import settings

user = get_user_model()

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})


    def __str__(self):
        return self.title
 
