from secrets import token_urlsafe

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from django.contrib.auth.models import User
from .models import Trail, Game, Item
from .forms import TrailForm

# Create your views here.

@login_required(login_url='/login/')
def trail_main_view(request, id=1):
    # Get current user
    current_user = request.user

    print("-----------------------------------")
    print('Hello "%s"' % current_user)

    # get trail data
    trail_data = get_object_or_404(Trail, id=id)


    # Check if it is a POST
    if request.method == 'POST':
        print('Hello! Button has been pressed')
        form = TrailForm(request.POST)
        # Check if data is valid
        if form.is_valid():
            print("Form is valid!")

        # Now create a new game for the current user
        my_url = token_urlsafe(16)
        print(my_url)

        Game.objects.create(game_name='The Gem Game',
                            game_description='Find the gems.',
                            game_player=request.user,
                            game_url=my_url,
                            )

        # Redirect to game.html
        return HttpResponseRedirect('/game/')

    else:
        form = TrailForm()#initial={'post':"My data"})

    # Add it all to context dictionary
    context = {
        "form": form,
        "object": trail_data,
        }
    return render(request, "trail/trail_main.html", context)





@login_required(login_url='/login/')
def game_main_view(request): #, id):
    current_user = request.user

    # get game data
    gameslist = Game.objects.filter(game_player=current_user)
    print(gameslist)

    items = Item.objects.distinct().filter(game__in=gameslist)
    print("You have the following items...")
    for item in items:
        print("> %s : %s" % (item.item_name, item.item_description))

    return render(request, "game/game_main.html", {})
















#### Class Based Views Stuff -  Will look at later in more detail!
# from .forms import TrailForm
# from django.utils.decorators import method_decorator
# from django.views.generic import TemplateView
#
# class TrailMainView(TemplateView):
#     template_name = 'trail_main.html'
#
#     def get(self, request):
#         form = TrailForm()
#         print("hello fro the view!")
#         print(form)
#         return render(request, self.template_name, {'form': form})
#
#     # @method_decorator(login_required)
#     # def dispatch(self, *args, **kwargs):
#     #     return super().dispatch(*args, **kwargs)



