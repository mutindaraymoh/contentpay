from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    path('videos/', views.video_list, name='video_list'),
    path('video/<slug:slug>/', views.video_detail, name='video_detail'),
    path('create-checkout-session/', views.create_checkout_session, name='create_checkout_session'),
    
    # M-Pesa URLs
    path('mpesa/payment/<str:content_type>/<int:content_id>/', views.mpesa_payment_page, name='mpesa_payment_page'),
    path('mpesa/initiate/', views.initiate_mpesa_payment, name='initiate_mpesa_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    path('payment/pending/', views.payment_pending, name='payment_pending'),
    
    # Registration
    path('register/', views.register, name='register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)