from django.urls import path
from favorites.views import show_restaurant, favorites_view, show_restaurant_review, add_favorite, remove_favorite, add_review, remove_review, list_favorites, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'favorites'

urlpatterns = [
    path('', show_restaurant, name ='show_restaurant'),
    path('favorites/', favorites_view, name='favorites'),
    path('show_restaurant_review/', show_restaurant_review, name ='show_restaurant_review'),
    path('add_favorite/', add_favorite, name='add_favorite'),
    path('remove_favorite/', remove_favorite, name='remove_favorite'),
    path('add_review/', add_review, name='add_review'),
    path('remove_review/', remove_review, name='remove_review'),
    path('list_favorites/', list_favorites, name='list_favorites'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]