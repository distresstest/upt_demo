from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . views import trail_main_view, game_main_view, location_detail_view
# from django.views.generic import TemplateView   # CBV Stuff

app_name = 'trail'
urlpatterns = [
    path('<int:id>/', trail_main_view, name='trail_main_view'),
    path('', trail_main_view, name='trail_main_view'),
    path('game/', game_main_view, name='game_main_view'),
    path('location/<int:id>/', location_detail_view, name='location_detail_view'),
    # path('', TemplateView.as_view(template_name="trail/trail_main.html")) # CBV stuff

]