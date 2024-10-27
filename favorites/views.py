# favorites/views.py
from django.shortcuts import render, get_object_or_404, redirect
from favorites.models import Restaurant, FavoriteRestaurant, RestaurantReview, FavoriteRestaurant
from django.http import HttpResponse, JsonResponse

from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from django.contrib import messages
from django.utils.html import strip_tags

# @login_required
# favorites/views.py

def favorites_view(request):

        user_favorites = FavoriteRestaurant.objects.all()
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
