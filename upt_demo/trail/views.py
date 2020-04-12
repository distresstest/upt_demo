# Other packages
from secrets import token_urlsafe

# django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# My packages
from .models import Trail, Game, Item, Location
from .forms import TrailForm, LocationForm

# Create your views here.
@login_required(login_url='/login/')
def trail_main_view(request, id=1):
    # Get current user
    current_user = request.user
    print('Hello "%s"' % current_user)

    # get trail data
    trail_data = get_object_or_404(Trail, id=id)

    print('trail_data.trail_name = %s' % trail_data.trail_name)
    print('trail_data.trail_description = %s' % trail_data.trail_description)
    print('trail_data.trail_mission = %s' % trail_data.trail_mission)
    print('trail_data.trail_total_items %s' % trail_data.trail_total_items)

   # Check if it is a POST
    if request.method == 'POST':
        print('Hello! Button has been pressed')
        form = TrailForm(request.POST)
        # Check if data is valid
        if form.is_valid():
            print("Form is valid!")

            # Now create a new game for the current user
            my_url = token_urlsafe(16)
            Game.objects.create(game_name=trail_data.trail_name,
                                game_mission=trail_data.trail_mission,
                                game_player=request.user,
                                game_url=my_url,
                                game_total_items=trail_data.trail_total_items,
                                )

            # Redirect to game.html
            return HttpResponseRedirect('/game/')

    else:
        form = TrailForm()  #initial={'post':"My data"})

    # Add it all to context dictionary
    context = {
        "form": form,
        "object": trail_data,
        }
    return render(request, "trail/trail_main.html", context)





@login_required(login_url='/login/')
def game_main_view(request): #, id):
    print("-------------------------------")
    print("In game_main_view...")
    current_user = request.user

    # get game data
    gameslist = Game.objects.filter(game_player=current_user).order_by('-game_start')[:1]
    print(gameslist)
    game_data = gameslist[0]
    print(game_data)
    print('game_data.id = %s' % game_data.id)
    print('game_data.game_player = %s' % game_data.game_player)
    print('game_data.game_name = %s' % game_data.game_name)
    print('game_data.game_mission = %s' % game_data.game_mission)
    print('game_data.game_start = %s' % game_data.game_start)
    print('game_data.game_inventory = %s' % game_data.game_inventory)
    print('game_data.game_url = %s' % game_data.game_url)
    print('game_data.game_total_items = %s' % game_data.game_total_items)

    items = Item.objects.distinct().filter(game__in=gameslist)
    print("You have the following items...")
    for item in items:
        print("> %s : %s" % (item.item_name, item.item_description))

    current_items = len(items)

    if current_user == game_data.game_total_items:
        trail_completed = True
    else:
        trail_completed = False

    # Add it all to context dictionary
    context = {
        "items": items,
        "current_items": current_items,
        "object": game_data,
        "complete": trail_completed,
        }

    return render(request, "game/game_main.html", context)



def location_detail_view(request, id):

    # Get the location data
    location_data = get_object_or_404(Location, id=id)

    # Print out the data
    print('location_data.id = %s' % location_data.id)
    print('location_data.location_name = %s' % location_data.location_name)
    print('location_data.location_description = %s' % location_data.location_description)

    # Check if it is a POST
    if request.method == 'POST':
        print('Hello! Button has been pressed')

        request.POST.getlist('item')
        form = LocationForm(request.POST)
        print(form)
        print(request.POST)
        for n in request.POST:
            print(n)

        item = Item.objects.filter(id=1)
        print('You have picked up item %s' % item[0].item_name)


    locationlist = Location.objects.filter(id=id)

    location_items = Item.objects.distinct().filter(location__in=locationlist)
    print("The location has the following items...")
    for item in location_items:
        print('> %s : "%s", "%s" (%s)' % (item.item_name, item.item_description, item.item_alt, item.item_image))

    total_items = len(location_items)

    context = {
        "location_data": location_data,
        "location_items": location_items,
        "total_items": total_items,
    }

    print(context)

    return render(request, "locations/location_detail.html", context)












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



