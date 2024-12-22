from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.core import serializers
from .models import Restaurant
from django.views.decorators.csrf import csrf_exempt

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core import serializers
from .models import Restaurant

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from .models import Restaurant
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from favorites.models import FavoriteRestaurant
from authentication.models import User



# Add to favorites
# @login_required(login_url='/auth/login')
@csrf_exempt
def addfavorite(request, restaurant_id):
    if 'user_id' not in request.session:
        messages.error(request, "Anda harus login terlebih dahulu.")
        return redirect('login_user')
    if request.method == 'POST':
        
        user_id = request.session.get('user_id')
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        user = User.objects.get(id=user_id)
        favorite, created = FavoriteRestaurant.objects.get_or_create(user=user, restaurant=restaurant )


        if created:
       
            return JsonResponse({'success': True, 'message': f'{restaurant.name} added to favorites.'})
        else:
            return JsonResponse({'success': False, 'message': f'{restaurant.name} is already in your favorites.'})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)

# Daftar restoran
@csrf_exempt
def restaurant_list(request):
    if 'user_id' not in request.session:
        return redirect('login_user')
    
    queryset = Restaurant.objects.all()

    # Apply filters
    if name := request.GET.get('name'):
        queryset = queryset.filter(name__icontains=name)

    if min_rating := request.GET.get('min_rating'):
        try:
            queryset = queryset.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    if max_rating := request.GET.get('max_rating'):
        try:
            queryset = queryset.filter(rating__lte=float(max_rating))
        except ValueError:
            pass

    if address := request.GET.get('address'):
        queryset = queryset.filter(address__icontains=address)

    if rating_count := request.GET.get('rating_count'):
        try:
            rating_count = int(rating_count)
            ranges = {
                25: (1, 25),
                50: (26, 50),
                100: (51, 100),
                200: (101, 1000)
            }
            if rating_count in ranges:
                min_count, max_count = ranges[rating_count]
                queryset = queryset.filter(
                    rating_amount__gte=min_count,
                    rating_amount__lte=max_count
                ).exclude(rating_amount__isnull=True)
        except ValueError:
            pass

    if ordering := request.GET.get('ordering'):
        order_mapping = {
            'rating_low': 'rating',
            'rating_high': '-rating',
            'name_asc': 'name',
            'name_desc': '-name'
        }
        if ordering in order_mapping:
            queryset = queryset.order_by(order_mapping[ordering])

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = list(queryset.values('name', 'rating', 'address'))
        return JsonResponse(data, safe=False)

    return render(request, 'daftar_toko.html', {'toko': queryset})

@csrf_exempt
def show_xml(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
def show_json(request):
    data = Restaurant.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def show_xml_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

@csrf_exempt
def show_json_by_id(request, id):
    data = Restaurant.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")



