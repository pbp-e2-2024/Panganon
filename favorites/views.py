# favorites/views.py
from favorites.models import Restaurant, FavoriteRestaurant, RestaurantReview, FavoriteRestaurant
from django.http import HttpResponse, JsonResponse

from django.core import serializers
from django.contrib.auth.decorators import login_required
from datetime import datetime, timezone
from urllib.parse import unquote
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib import messages
from django.utils.html import strip_tags
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers

from .models import FavoriteRestaurant, RestaurantReview
from authentication.models import User
from daftar_toko.models import Restaurant

# @login_required
# favorites/views.py

def favorites_view(request):
        user_favorites = Restaurant.objects.all()
        return render(request, 'favorites.html', {'user_favorites': user_favorites})

@require_POST
def add_favorite(request, restaurant_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'status': 'error', 'message': 'User not logged in'}, status=401)

    try:
        user = get_object_or_404(User, id=user_id)
        
        # Mendapatkan objek Restaurant
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        # Mengecek apakah restoran sudah ada di favorit user
        favorite, created = FavoriteRestaurant.objects.get_or_create(
            user=user,
            restaurant=restaurant
        )
        
        if created:
            message = f'{restaurant.name} has been added to your favorites!'
            messages.success(request, message)
        else:
            message = f'{restaurant.name} is already in your favorites!'
            messages.info(request, message)
            
        # Menangani respon jika ini adalah permintaan AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'created': created,
                'message': message
            })
            
        # Redirect kembali ke halaman sebelumnya
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('show_fav_restaurant')))
        
    except Restaurant.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Restaurant not found!'}, status=404)
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'User not found!'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'An error occurred: {str(e)}'}, status=500)


# @login_required
def remove_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite = FavoriteRestaurant.objects.filter(user=request.user, restaurant=restaurant).first()
    if favorite:
        favorite.delete()
        messages.success(request, f'{restaurant.name} telah dihapus dari favorit Anda')
    else:
        messages.error(request, f'{restaurant.name} tidak ditemukan di daftar favorit Anda')
    return redirect('favorites:favorites')

# favorites/views.py

@csrf_exempt
def add_review(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)

    # Parsing data from JSON
    data = JsonResponse.loads(request.body)
    review_content = data.get("review")
    rating = data.get("rating")

    if review_content and rating:
        review = RestaurantReview.objects.create(
            user=request.user,
            restaurant=restaurant,
            review=review_content,
            rating=rating
        )
        review.save()
        return JsonResponse({'success': True, 'message': f'Review untuk {restaurant.name} telah ditambahkan.'})
    return JsonResponse({'success': False, 'message': 'Konten review dan rating harus diisi.'})

@csrf_exempt
def remove_review(request, review_id):
    review = get_object_or_404(RestaurantReview, id=review_id, user=request.user)

    review.delete()
    return JsonResponse({'success': True, 'message': 'Restoran review telah dihapus.'})

def show_json(request):
    data = serializers.serialize("json", Restaurant.objects.all())
    return HttpResponse(data, content_type="application/json")

def show_xml(request):
    data = serializers.serialize("xml", Restaurant.objects.all())
    return HttpResponse(data, content_type="application/xml")

def show_json_by_id(request, id):
    data = serializers.serialize("json", Restaurant.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/json")

def show_xml_by_id(request, id):
    data = serializers.serialize("xml", Restaurant.objects.filter(pk=id))
    return HttpResponse(data, content_type="application/xml")
from daftar_toko.models import Restaurant 

def show_fav_restaurant(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    restaurants = Restaurant.objects.all()
    context = {
        'restaurants': restaurants,
    }
    return render(request, "add_fav.html", context)
    

@require_POST
def add_favorite(request, restaurant_id):
    
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    try:
        # Get the restaurant by name
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user_id = request.session.get('user_id')
        user = User.objects.get(id=user_id)
        
        # Check if already favorited
        favorite, created = FavoriteRestaurant.objects.get_or_create(
            user=user,
            restaurant=restaurant
        )
        
        if created:
            messages.success(request, f'{restaurant.name} has been added to your favorites!')
        else:
            messages.info(request, f'{restaurant.name} is already in your favorites!')
            
        # If it's an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'created': created,
                'message': 'Added to favorites' if created else 'Already in favorites'
            })
            
        # Redirect back to the previous page
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', reverse('show_fav_restaurant')))
        
    except Restaurant.DoesNotExist:
        messages.error(request, 'Restaurant not found!')
        return redirect('show_fav_restaurant')
    except User.DoesNotExist:
        messages.error(request, 'User not found!')
        return redirect('login_user')
    except Exception as e:
        messages.error(request, f'An error occurred: {str(e)}')
        return redirect('show_fav_restaurant')
