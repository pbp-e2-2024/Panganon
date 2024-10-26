from django.shortcuts import render, redirect, reverse
from django.shortcuts import render, get_object_or_404, redirect
from favorites.models import Restaurant, FavoriteRestaurant, RestaurantReview
from django.http import HttpResponse,  HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags



# Create your views here.

#@login_required(login_url='/login')

def show_restaurant(request):

    return render(request, "add_fav.html")

def show_fav_restaurant(request):
    favorite_restaurants = FavoriteRestaurant.objects.filter(user=request.user)
    
    context = {
        'favorite_restaurants': favorite_restaurants,
    }
    return render(request, "add_fav.html", context)

def show_restaurant_review(request):
    ...

def add_favorite(request,restaurant_id):
    #add code
    restaurant = get_object_or_404(Restaurant, id= restaurant_id)
    favorite, created = FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)

    if created:
        messages.success(request, f'{Restaurant.name} telah ditambahkan ke favorti anda')
    else:
        messages.success(request, f'{Restaurant.name} sudah ditambahkan kedalam favorit anda')

    return redirect('restaurant_detail', restaurant_id=restaurant.id)

def remove_favorite(request,restaurant_id):
    #add code
    restaurant = get_object_or_404(Restaurant, id= restaurant_id)
    favorite= FavoriteRestaurant.objects.get_or_create(user=request.user, restaurant=restaurant)

    if favorite.exist():
        favorite.delete()
        messages.success(request, f'{Restaurant.name} telah dihapus dari favorti anda')
    else:
        messages.success(request, f'{Restaurant.name} tidak ditemukan di favorit anda')

    return redirect('restaurant_detail', restaurant_id=restaurant.id)

def add_review(request, review_id):
    #add code
    restaurant = get_object_or_404(Restaurant, id=review_id)

    if request.method == "POST":
        review_content = request.POST.get("review")
        rating = request.POST.get("rating")

        if review_content and rating:
            # Create and save the review
            review = RestaurantReview.objects.create(
                user=request.user, 
                restaurant=restaurant, 
                review_text=review_content, 
                rating=rating
            )
            review.save()
            messages.success(request, f'Review for {restaurant.name} has been added.')
        else:
            messages.error(request, 'Review content and rating are required.')

    return redirect('restaurant_detail', restaurant_id=restaurant.id)


@csrf_exempt
@require_POST
def add_review_by_AJAX(request, review_id):
    #add code
    restaurant = get_object_or_404(Restaurant, id=review_id)

    review_content = strip_tags(request.POST.get("review"))
    rating = strip_tags(request.POST.get("rating"))


    try:
        rating = float(rating)
    except(ValueError, TypeError):
        messages.error(request, 'Rating harus bilangan.')
        return redirect('restaurant_detail', restaurant_id=restaurant.id)

       
            
    if review_content and 1 <= rating <=5:
        review = RestaurantReview.objects.create(
            user=request.user, 
            restaurant=restaurant, 
            review_text=review_content, 
            rating=rating
        )
        review.save()

    return redirect(b'review was added', restaurant_id=restaurant.id)


    
def remove_review(request, review_id):
    #add code
    review = get_object_or_404(RestaurantReview, id=review_id, user=request.user)
    
    if request.method == "POST":
        review.delete()
        messages.success(request, f'Review for {review.restaurant.name} has been removed.')
    else:
        messages.error(request, 'Failed to remove review.')

    return redirect('restaurant_detail', restaurant_id=review.restaurant.id)
def list_favorites(request):
    #add code
    favorites = FavoriteRestaurant.objects.filter(user=request.user)
    
    return render(request, 'add_fav.html', {'favorites': favorites})

def show_xml(request):
    dataRestaurant = Restaurant.objects.filter(user=request.user)
    dataReview = RestaurantReview.objects.filter(user=request.user)

    serializer_Restaurant = serializers.serialize("xml", dataRestaurant)
    serializer_Review = serializers.serialize("xml", dataReview)

    combined_seliarizers = serializer_Restaurant + serializer_Review

    return HttpResponse(combined_seliarizers, content_type="application/xml")



def show_json(request):
    dataRestaurant = Restaurant.objects.filter(user=request.user)
    dataReview = RestaurantReview.objects.filter(user=request.user)

    serializer_Restaurant = serializers.serialize("json", dataRestaurant)
    serializer_Review = serializers.serialize("json", dataReview)

    combined_seliarizers = serializer_Restaurant + serializer_Review

    return HttpResponse(combined_seliarizers, content_type="application/json")

def show_xml_by_id(request, id):
    dataRestaurant = Restaurant.objects.filter(pk=id)
    dataReview = RestaurantReview.objects.filter(pk=id)

    serializer_Restaurant = serializers.serialize("xml", dataRestaurant)
    serializer_Review = serializers.serialize("xml", dataReview)

    combined_seliarizers = serializer_Restaurant + serializer_Review

    return HttpResponse(combined_seliarizers, content_type="application/xml")

def show_json_by_id(request, id):
    dataRestaurant = Restaurant.objects.filter(pk=id)
    dataReview = RestaurantReview.objects.filter(pk=id)

    serializer_Restaurant = serializers.serialize("json", dataRestaurant)
    serializer_Review = serializers.serialize("json", dataReview)

    combined_seliarizers = serializer_Restaurant + serializer_Review

    return HttpResponse(combined_seliarizers, content_type="application/json")
