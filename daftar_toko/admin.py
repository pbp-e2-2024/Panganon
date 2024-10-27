from django.contrib import admin
from django.urls import path
from django.core.management import call_command
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Restaurant

class MyModelAdmin(admin.ModelAdmin):

    change_list_template = "change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('load-dataset/', self.admin_site.admin_view(self.load_dataset), name='load-dataset'),
        ]
        return custom_urls + urls

    def load_dataset(self, request):
        try:
            call_command('load_makanan', 'dataset/Bika_Ambon_Medan.json', 'dataset/Durian_Medan.json', 
                         'dataset/Kari_Medan.json', 'dataset/Lontong_Medan.json', 
                         'dataset/Nasi_Lemak_Medan.json', 'dataset/Sate_Medan.json', 
                         'dataset/Soto_Medan.json')
            self.message_user(request, "Datasets loaded successfully", messages.SUCCESS)
        except Exception as e:
            self.message_user(request, f"Error loading datasets: {e}", messages.ERROR)
        return HttpResponseRedirect("../")

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['custom_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Restaurant, MyModelAdmin)