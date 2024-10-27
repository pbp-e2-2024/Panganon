# favorites/views.py
from favorites.models import Restaurant, FavoriteRestaurant, RestaurantReview, FavoriteRestaurant
from django.http import HttpResponse, JsonResponse

from django.core import serializers
from django.contrib.auth.decorators import login_required
from datetime import timezone
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



# @login_required
def add_favorite(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)
    if created:
        messages.success(request, f'{restaurant.name} telah ditambahkan ke favorit Anda')
    else:
        messages.info(request, f'{restaurant.name} sudah ada di daftar favorit Anda')
    return redirect('favorites:favorites')

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

# @login_required
# @require_POST
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
    

# def remove_favorite(request, restaurant_id):
#     if 'user_id' not in request.session:
#         return redirect('login_user')

#     restaurant = get_object_or_404(Restaurant, id=restaurant_id)
#     favorite = FavoriteRestaurant.objects.filter(user=request.user, restaurant=restaurant)

#     if favorite.exists():
#         favorite.delete()
#         messages.success(request, f'{restaurant.name} telah dihapus dari favorit anda')
#     else:
#         messages.success(request, f'{restaurant.name} tidak ditemukan di favorit anda')

#     return redirect('restaurant_detail', restaurant_id=restaurant.id)

# def add_review(request, review_id):
#     if 'user_id' not in request.session:
#         return redirect('login_user')
    
#     restaurant = get_object_or_404(Restaurant, id=review_id)

#     if request.method == "POST":
#         review_content = request.POST.get("review")
#         rating = request.POST.get("rating")

#         if review_content and rating:
#             review = RestaurantReview.objects.create(
#                 user=request.user, 
#                 restaurant=restaurant, 
#                 review_text=review_content, 
#                 rating=rating
#             )
#             review.save()
#             messages.success(request, f'Review for {restaurant.name} has been added.')
#         else:
#             messages.error(request, 'Review content and rating are required.')

#     return redirect('restaurant_detail', restaurant_id=restaurant.id)

# @csrf_exempt
# @require_POST
# def add_review_by_AJAX(request, review_id):
#     restaurant = get_object_or_404(Restaurant, id=review_id)

#     review_content = strip_tags(request.POST.get("review"))
#     rating = strip_tags(request.POST.get("rating"))

#     try:
#         rating = float(rating)
#     except (ValueError, TypeError):
#         messages.error(request, 'Rating harus bilangan.')
#         return redirect('restaurant_detail', restaurant_id=restaurant.id)
            
#     if review_content and 1 <= rating <= 5:
#         review = RestaurantReview.objects.create(
#             user=request.user, 
#             restaurant=restaurant, 
#             review_text=review_content, 
#             rating=rating
#         )
#         review.save()

#     return HttpResponseRedirect('review was added')

# def remove_review(request, review_id):
#     review = get_object_or_404(RestaurantReview, id=review_id, user=request.user)
    
#     if request.method == "POST":
#         restaurant_id = review.restaurant.id
#         review.delete()
#         messages.success(request, f'Review for {review.restaurant.name} has been removed.')
#     else:
#         messages.error(request, 'Failed to remove review.')

#     return redirect('restaurant_detail', restaurant_id=restaurant_id)

# def list_favorites(request):
#     favorites = FavoriteRestaurant.objects.filter(user=request.user)
#     return render(request, 'add_fav.html', {'favorites': favorites})

def show_xml(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    data_review = RestaurantReview.objects.filter(user=user)
    return HttpResponse(serializers.serialize("xml", data_review), content_type="application/xml")

def show_json(request):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    data_review = RestaurantReview.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data_review), content_type="application/json")

def show_xml_by_id(request, id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    data_review = RestaurantReview.objects.filter(user=user)
    return HttpResponse(serializers.serialize("xml", data_review), content_type="application/xml")

def show_json_by_id(request, id):
    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)
    data_review = RestaurantReview.objects.filter(user=user)
    return HttpResponse(serializers.serialize("json", data_review), content_type="application/json")
