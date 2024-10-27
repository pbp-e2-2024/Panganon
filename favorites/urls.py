from django.urls import path
from favorites.views import show_fav_restaurant, add_favorite, show_xml, show_json, show_xml_by_id, show_json_by_id

app_name = 'favorites'

urlpatterns = [
    path('', show_fav_restaurant, name ='show_fav_restaurant'),
    # path('show_restaurant_review/', show_restaurant_review, name ='show_restaurant_review'),
    path('add/<str:restaurant_id>/', add_favorite, name='add_favorite'),
    # path('remove_favorite/<str:restaurant_name>/', remove_favorite, name='remove_favorite'),
    # path('add_review/<str:restaurant_name>/', add_review, name='add_review'),
    # path('remove_review/<str:restaurant_name>/', remove_review, name='remove_review')
    # path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]