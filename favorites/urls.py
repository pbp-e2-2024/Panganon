# favorites/urls.py
from django.urls import path
from favorites.views import favorites_view, add_favorite, remove_favorite, add_review, remove_review, show_json, show_xml, show_json_by_id, show_xml_by_id

app_name = 'favorites'

urlpatterns = [
    path('', favorites_view, name='favorites'),
    path('add_favorite/', add_favorite, name='add_favorite'),
    path('remove_favorite/', remove_favorite, name='remove_favorite'),
    path('add_review/str:add_review/', add_review, name='add_review'),
    path('remove_review/', remove_review, name='remove_review'),
    path('json/', show_json, name='show_json'),
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json_by_id, name='show_json_by_id'),
    path('xml/', show_xml_by_id, name='show_xml_by_id'),
]
