from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(max_length=500)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles')
    thumbnail = models.ImageField(upload_to='articles/thumbnails/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=9.99)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('article_detail', args=[self.slug])

class Video(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    video_url = models.URLField()  # YouTube/Vimeo URL or video file path
    thumbnail = models.ImageField(upload_to='videos/thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='videos')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=14.99)
    duration = models.CharField(max_length=20, help_text="e.g., 10:30")
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('video_detail', args=[self.slug])

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, null=True, blank=True)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=255)
    purchased_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [
            ['user', 'article'],
            ['user', 'video']
        ]
    
    def __str__(self):
        item = self.article or self.video
        return f"{self.user.username} - {item.title}"
# Create your models here.
