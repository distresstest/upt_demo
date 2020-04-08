from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import trail_main_view

app_name = 'trail'
urlpatterns = [
    #path('<int:id>/', trail_main_view, name='trail_main_view'),
    path('', trail_main_view, name='trail_main_view'),
]