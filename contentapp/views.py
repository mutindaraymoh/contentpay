from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from .models import Article, Video, Purchase, Category

# M-Pesa integration
try:
    from django_daraja.mpesa.core import MpesaClient
    MPESA_AVAILABLE = True
except ImportError:
    MPESA_AVAILABLE = False
    print("WARNING: django_daraja not installed. M-Pesa payments will not work.")

def home(request):
    featured_articles = Article.objects.filter(is_published=True).order_by('-created_at')[:3]
    featured_videos = Video.objects.filter(is_published=True).order_by('-created_at')[:3]
    categories = Category.objects.all()
    
    context = {
        'featured_articles': featured_articles,
        'featured_videos': featured_videos,
        'categories': categories,
        'mpesa_available': MPESA_AVAILABLE,
    }
    return render(request, 'contentapp/home.html', context)

def article_list(request):
    category_slug = request.GET.get('category')
    articles = Article.objects.filter(is_published=True)
    
    if category_slug:
        articles = articles.filter(category__slug=category_slug)
    
    context = {
        'articles': articles,
        'categories': Category.objects.all(),
        'current_category': category_slug
    }
    return render(request, 'contentapp/article_list.html', context)

@login_required
def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    
    # Check if user has purchased this article
    has_purchased = Purchase.objects.filter(
        user=request.user, 
        article=article
    ).exists()
    
    context = {
        'article': article,
        'has_purchased': has_purchased,
        'mpesa_available': MPESA_AVAILABLE,
    }
    return render(request, 'contentapp/article_detail.html', context)

def video_list(request):
    category_slug = request.GET.get('category')
    videos = Video.objects.filter(is_published=True)
    
    if category_slug:
        videos = videos.filter(category__slug=category_slug)
    
    context = {
        'videos': videos,
        'categories': Category.objects.all(),
        'current_category': category_slug
    }
    return render(request, 'contentapp/video_list.html', context)

@login_required
def video_detail(request, slug):
    video = get_object_or_404(Video, slug=slug, is_published=True)
    
    # Check if user has purchased this video
    has_purchased = Purchase.objects.filter(
        user=request.user, 
        video=video
    ).exists()
    
    context = {
        'video': video,
        'has_purchased': has_purchased,
        'mpesa_available': MPESA_AVAILABLE,
    }
    return render(request, 'contentapp/video_detail.html', context)

# ============= M-PESA PAYMENT METHODS =============

@login_required
def mpesa_payment_page(request, content_type, content_id):
    """Display M-Pesa payment page"""
    if content_type == 'article':
        item = get_object_or_404(Article, id=content_id, is_published=True)
    elif content_type == 'video':
        item = get_object_or_404(Video, id=content_id, is_published=True)
    else:
        messages.error(request, 'Invalid content type')
        return redirect('home')
    
    # Check if already purchased
    if content_type == 'article':
        already_purchased = Purchase.objects.filter(
            user=request.user, article=item
        ).exists()
    else:
        already_purchased = Purchase.objects.filter(
            user=request.user, video=item
        ).exists()
    
    if already_purchased:
        messages.info(request, 'You already have access to this content')
        return redirect(item.get_absolute_url())
    
    context = {
        'item': item,
        'content_type': content_type,
    }
    return render(request, 'contentapp/mpesa_payment.html', context)

@login_required
def initiate_mpesa_payment(request):
    """Initiate STK Push for content purchase"""
    if not MPESA_AVAILABLE:
        messages.error(request, 'M-Pesa payment is not configured. Please install django-daraja.')
        return redirect('home')
        
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        phone_number = request.POST.get('phone_number')
        
        # Validate and format phone number
        phone_number = phone_number.strip()
        # Remove any non-digit characters
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Convert to format required by M-Pesa (2547XXXXXXXX)
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('7'):
            phone_number = '254' + phone_number
        elif phone_number.startswith('254'):
            pass  # Already in correct format
        else:
            messages.error(request, 'Please enter a valid phone number (e.g., 0712345678 or 254712345678)')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        # Ensure it's 12 digits
        if len(phone_number) != 12:
            messages.error(request, 'Phone number must be 12 digits (format: 254712345678)')
            return redirect(request.META.get('HTTP_REFERER', 'home'))
        
        # Get the content item
        if content_type == 'article':
            item = get_object_or_404(Article, id=content_id)
        elif content_type == 'video':
            item = get_object_or_404(Video, id=content_id)
        else:
            messages.error(request, 'Invalid content type')
            return redirect('home')
        
        # Check if already purchased
        if content_type == 'article':
            already_purchased = Purchase.objects.filter(
                user=request.user, article=item
            ).exists()
        else:
            already_purchased = Purchase.objects.filter(
                user=request.user, video=item
            ).exists()
        
        if already_purchased:
            messages.info(request, 'You already have access to this content')
            return redirect(item.get_absolute_url())
        
        # Store purchase details in session for callback
        request.session['pending_purchase'] = {
            'user_id': request.user.id,
            'content_type': content_type,
            'content_id': content_id,
            'amount': str(item.price),
            'phone_number': phone_number
        }
        
        # Initialize M-Pesa client
        cl = MpesaClient()
        
        # Set up STK Push parameters
        account_reference = f'{content_type[:3].upper()}{content_id}'
        transaction_desc = f'Purchase of {item.title[:20]}'
        callback_url = request.build_absolute_uri('/mpesa/callback/')
        
        # Convert amount to integer (M-Pesa requires whole numbers)
        amount = int(float(item.price))
        
        # Initiate STK Push
        try:
            response = cl.stk_push(
                phone_number, 
                amount, 
                account_reference,
                transaction_desc, 
                callback_url
            )
            
            # Check response
            response_data = response.json()
            if response_data.get('ResponseCode') == '0':
                messages.success(
                    request, 
                    'STK Push sent! Please check your phone and enter your PIN to complete payment.'
                )
                return redirect('payment_pending')
            else:
                messages.error(
                    request, 
                    f'Payment initiation failed: {response_data.get("ResponseDescription", "Unknown error")}'
                )
                return redirect(item.get_absolute_url())
                
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect(item.get_absolute_url())
    
    return redirect('home')

def payment_pending(request):
    """Show payment pending page"""
    return render(request, 'contentapp/payment_pending.html')

@csrf_exempt
def mpesa_callback(request):
    """Handle M-Pesa payment callback"""
    if request.method == 'POST':
        try:
            # Get callback data
            callback_data = json.loads(request.body)
            print(f"M-Pesa Callback received: {json.dumps(callback_data, indent=2)}")
            
            # Extract transaction details
            body = callback_data.get('Body', {})
            stk_callback = body.get('stkCallback', {})
            result_code = stk_callback.get('ResultCode')
            result_desc = stk_callback.get('ResultDesc')
            checkout_request_id = stk_callback.get('CheckoutRequestID')
            
            # Check if payment was successful (ResultCode 0 means success)
            if result_code == 0:
                # Get metadata from callback
                metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
                
                # Extract transaction details
                transaction_details = {}
                for item in metadata:
                    name = item.get('Name')
                    value = item.get('Value')
                    transaction_details[name] = value
                
                print(f"Payment successful: {transaction_details}")
                
                # Here you would typically:
                # 1. Find the pending transaction by checkout_request_id
                # 2. Create Purchase record
                # 3. Grant access to content
                
                # For now, just return success to M-Pesa
                return JsonResponse({"ResultCode": 0, "ResultDesc": "Success"})
            else:
                # Payment failed
                print(f"Payment failed: {result_desc}")
                return JsonResponse({"ResultCode": result_code, "ResultDesc": result_desc})
                
        except Exception as e:
            print(f"Callback error: {str(e)}")
            return JsonResponse({"ResultCode": 1, "ResultDesc": "Error processing callback"})
    
    return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"})

# ============= USER REGISTRATION =============

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')

        # Example: fetch the video or article price
        if content_type == 'video':
            from .models import Video
            item = Video.objects.get(id=content_id)
        else:
            from .models import Article
            item = Article.objects.get(id=content_id)

        stripe.api_key = settings.STRIPE_SECRET_KEY

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'kes',
                    'product_data': {
                        'name': item.title,
                    },
                    'unit_amount': int(item.price * 100),  # price in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri('/success/'),
            cancel_url=request.build_absolute_uri('/cancel/'),
        )

        return redirect(session.url, code=303)
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from .models import Article, Video, Purchase

@login_required
def initiate_mpesa_payment(request):
    """Initiate STK Push for content purchase using settings.py values"""
    if request.method == 'POST':
        content_type = request.POST.get('content_type')
        content_id = request.POST.get('content_id')
        phone_number = request.POST.get('phone_number').strip()

        # Format phone number
        phone_number = ''.join(filter(str.isdigit, phone_number))
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('7'):
            phone_number = '254' + phone_number
        elif not phone_number.startswith('254'):
            messages.error(request, 'Invalid phone number format. Use 07XXXXXXXX or 2547XXXXXXXX')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        if len(phone_number) != 12:
            messages.error(request, 'Phone number must be 12 digits (format: 254712345678)')
            return redirect(request.META.get('HTTP_REFERER', 'home'))

        # Get the content item
        if content_type == 'article':
            item = get_object_or_404(Article, id=content_id)
            already_purchased = Purchase.objects.filter(user=request.user, article=item).exists()
        elif content_type == 'video':
            item = get_object_or_404(Video, id=content_id)
            already_purchased = Purchase.objects.filter(user=request.user, video=item).exists()
        else:
            messages.error(request, 'Invalid content type')
            return redirect('home')

        if already_purchased:
            messages.info(request, 'You already have access to this content')
            return redirect(item.get_absolute_url())

        # Initialize M-Pesa client
        cl = MpesaClient()

        account_reference = f'{content_type[:3].upper()}{content_id}'
        transaction_desc = f'Purchase of {item.title[:20]}'
        callback_url = settings.MPESA_SANDBOX_CALLBACK_URL
        amount = int(float(item.price))  # M-Pesa requires whole numbers

        try:
            response = cl.stk_push(
                phone_number,
                amount,
                account_reference,
                transaction_desc,
                callback_url,
               
            )
            response_data = response.json()
            if response_data.get('ResponseCode') == '0':
                messages.success(request, 'STK Push sent! Check your phone to complete payment.')
                return redirect('payment_pending')
            else:
                messages.error(request, f'Payment failed: {response_data.get("ResponseDescription", "Unknown error")}')
                return redirect(item.get_absolute_url())
        except Exception as e:
            messages.error(request, f'Payment error: {str(e)}')
            return redirect(item.get_absolute_url())

    return redirect('home')
