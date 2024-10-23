from django.shortcuts import render
from .models import Makanan

def makanan_list(request):
    name = request.GET.get('name')
    min_rating = request.GET.get('min_rating')
    max_rating = request.GET.get('max_rating')
    address = request.GET.get('address')
    rating_amount = request.GET.get('rating_count') 

    queryset = Makanan.objects.all()

    if name:
        queryset = queryset.filter(name__icontains=name)

    if min_rating:
        try:
            min_rating = float(min_rating)
            queryset = queryset.filter(rating__gte=min_rating)
        except ValueError:
            pass 

    if max_rating:
        try:
            max_rating = float(max_rating)
            queryset = queryset.filter(rating__lte=max_rating)
        except ValueError:
            pass  

    if address:
        queryset = queryset.filter(address__icontains=address)

    if rating_amount:
        try:
            rating_amount = int(rating_amount)
            if rating_amount == 25:
                queryset = queryset.filter(rating_amount__gte=1, rating_amount__lte=25).exclude(rating_amount__isnull=True)
            elif rating_amount == 50:
                queryset = queryset.filter(rating_amount__gte=26, rating_amount__lte=50).exclude(rating_amount__isnull=True)
            elif rating_amount == 100:
                queryset = queryset.filter(rating_amount__gte=51, rating_amount__lte=100).exclude(rating_amount__isnull=True)
            elif rating_amount == 200:
                queryset = queryset.filter(rating_amount__gte=101, rating_amount__lte=1000).exclude(rating_amount__isnull=True)

        except ValueError:
            pass

    ordering = request.GET.get('ordering')
    if ordering == 'rating_low':
        queryset = queryset.order_by('rating')
    elif ordering == 'rating_high':
        queryset = queryset.order_by('-rating')
    elif ordering == 'name_asc':
        queryset = queryset.order_by('name')
    elif ordering == 'name_desc':
        queryset = queryset.order_by('-name')

    context = {
        'makanan': queryset, 
    }

    return render(request, 'makanan_list.html', context)
