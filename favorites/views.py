from favorites.models import FavoriteRestaurant
from django.http import HttpResponse, JsonResponse


from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from daftar_toko.models import Restaurant
from django.shortcuts import render

from authentication.models import User

from django.http import JsonResponse


# Tampilkan restoran favorit
def favorites_view(request):
    # Ambil daftar favorit pengguna
    user_id = request.session.get('user_id')
    user_favorites = FavoriteRestaurant.objects.filter(user=user_id).select_related('restaurant')

    # user_favorites = FavoriteRestaurant.objects.all()
    return render(request, 'favorites.html', {'user_favorites': user_favorites})

@csrf_exempt
def remove_favorite(request, restaurant_id):
    user_id = request.session.get('user_id')
   
    favorite, created = FavoriteRestaurant.objects.get_or_create(user=user_id, restaurant=restaurant)
    if request.method == 'POST':
        if not user_id.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        favorite = FavoriteRestaurant.objects.filter(user=user_id, restaurant=restaurant).first()
        if favorite:
            favorite.delete()
            return JsonResponse({'message': 'Favorite removed successfully', 'success': True})

        return JsonResponse({'error': 'Favorite not found', 'success': False})
    return JsonResponse({'error': 'Invalid request method'}, status=405)
