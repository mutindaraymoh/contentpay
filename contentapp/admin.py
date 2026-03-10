from django.contrib import admin
from django.contrib import admin
from .models import Category, Article, Video, Purchase

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'slug']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'price', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'content']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'category', 'price', 'duration', 'created_at', 'is_published']
    list_filter = ['category', 'is_published', 'created_at']
    search_fields = ['title', 'description']

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_item', 'amount_paid', 'purchased_at']
    list_filter = ['purchased_at']
    
    def get_item(self, obj):
        return obj.article or obj.video
    get_item.short_description = 'Item'
# Register your models here.
