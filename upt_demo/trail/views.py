# Other packages
from secrets import token_urlsafe
from datetime import datetime, timezone

# django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# My packages
from .models import Trail, Game, Item, Location
from .forms import TrailForm, LocationForm


# utility functions
def get_users_items(user):
    pass

def get_game_data(user):
    # get game data
    games_list = Game.objects.filter(game_player=user).order_by('-game_start')[:1]
    print(games_list)
    game_data = games_list[0]
    print(game_data)
    print('game_data.id = %s' % game_data.id)
    print('game_data.game_player = %s' % game_data.game_player)
    print('game_data.game_name = %s' % game_data.game_name)
    print('game_data.game_mission = %s' % game_data.game_mission)
    print('game_data.game_start = %s' % game_data.game_start)
    print('game_data.game_inventory = %s' % game_data.game_inventory)
    print('game_data.game_url = %s' % game_data.game_url)
    print('game_data.game_total_items = %s' % game_data.game_total_items)

    return games_list

# Create your views here.
@login_required(login_url='/login/')
def trail_main_view(request, id=1):
    # Get current user
    current_user = request.user
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
    print("------------ game_main_view -----------------")

    # Check if it is a POST from finish button click
    if request.method == 'POST':
        if request.POST.getlist('end_button')[0] == 'Finish':
            return render(request, "game/game_finish.html", {})

    # Work out which items the current player has got in their game
    current_user = request.user
    games_list = get_game_data(current_user)
    game_data = games_list[0]
    items = Item.objects.distinct().filter(game__in=games_list)
    print("You have the following items...")
    for item in items:
        print("> %s : %s" % (item.item_name, item.item_description))

    # Check if all items have been found
    current_items = len(items)
    if current_items == game_data.game_total_items:
        trail_completed = True
    else:
        trail_completed = False

    # Update the current duration
    now = datetime.now(timezone.utc)
    game_duration = now - game_data.game_start

    # Add it all to context dictionary
    context = {
        "items": items,
        "current_items": current_items,
        "object": game_data,
        "duration": game_duration,
        "complete": trail_completed,
        }

    return render(request, "game/game_main.html", context)

@login_required(login_url='/login/')
def location_detail_view(request, id):
    print("------------ location_detail_view -----------------")

    # Get the location data
    location_data = get_object_or_404(Location, id=id)

    # Check if it is a POST
    if request.method == 'POST':
        # Work out which item has been taken
        item_index = request.POST.getlist('item')[0]
        item = Item.objects.filter(id=item_index)
        print('You have picked up a %s' % item[0].item_name)

        #  Add it to game inventory
        current_item = Item(id=item_index)
        games_list = get_game_data(request.user)
        current_game = Game(id=games_list[0].id)
        current_game.game_inventory.add(current_item)

        # redirect to game_main_view
        return HttpResponseRedirect('/game/')

    location_list = Location.objects.filter(id=id)
    location_items = Item.objects.distinct().filter(location__in=location_list)
    print("The location has the following items...")
    for item in location_items:
        print('> %s : "%s", "%s" (%s)' % (item.item_name, item.item_description, item.item_alt, item.item_image))

    # get current game_inventory
    games_list = get_game_data(request.user)
    current_game = Game(id=games_list[0].id)
    game_items = Item.objects.distinct().filter(game__in=games_list)
    print("You have the following items...")
    for item in game_items:
        print("> %s : %s" % (item.item_name, item.item_description))

    location_items_left = location_items.difference(game_items)

    total_items = len(location_items_left)

    # Add it all to the context
    context = {
        "location_data": location_data,
        "location_items_left": location_items_left,
        "total_items": total_items,
    }

    return render(request, "locations/location_detail.html", context)


@login_required(login_url='/login/')
def game_finish_view(request):
    print("------------ game_finish_view -----------------")

    return render(request, "game/game_finish.html", {})

