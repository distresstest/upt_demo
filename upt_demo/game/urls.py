from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import game_main_view
# from django.views.generic import TemplateView   # CBV Stuff

app_name = 'game'
urlpatterns = [
    #path('<int:id>/', game_main view, name='game_main_view'),
    path('', game_main_view, name='game_main_view'),

]