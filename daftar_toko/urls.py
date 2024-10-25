from django.urls import path
from daftar_toko.views import restaurant_list, show_xml, show_json, show_xml_by_id, show_json_by_id

urlpatterns = [
    path('', restaurant_list, name='restaurant_list'),  # Root URL
    path('xml/', show_xml, name='show_xml'),
    path('json/', show_json, name='show_json'),
    path('xml/<str:id>/', show_xml_by_id, name='show_xml_by_id'),
    path('json/<str:id>/', show_json_by_id, name='show_json_by_id'),
]