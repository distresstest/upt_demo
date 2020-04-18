from django.urls import path
from . views import trail_main_view, game_main_view, location_detail_view#, game_finish_view

app_name = 'trail'

urlpatterns = [
    path('trail/<int:id>/', trail_main_view, name='trail_main_view'),  # For when we add more trails!
    #path('', trail_main_view, name='trail_main_view'),
    path('game/', game_main_view, name='game_main_view'),
    #path('game/finish', game_finish_view, name='game_main_view'),
    path('location/<int:id>/', location_detail_view, name='location_detail_view'),
]