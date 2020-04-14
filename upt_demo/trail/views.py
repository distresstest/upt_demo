# Other packages
from secrets import token_urlsafe
import datetime


# django packages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

# My packages
from .models import Trail, Game, Item, Location
from .forms import TrailForm, LocationForm
from .utility_functions import get_game_data, get_current_user, get_current_game_duration, format_duration, get_high_scores


# Create your views here.
@login_required(login_url='/login/')
def trail_main_view(request, id=1):
    """
    Trail Main View shows the landing page for a specific trail.
    It gathers trail data from database and monitors for a click on "Start Trail" button.
    On click it creates a new game for the current user in the database and redirected to the "game" page

    :param id: This is the "id" from the url  it equates to the id of the trail table (in models.py)
    :param request: django request object
    :return: django response (either redirect or rendered response)

    """

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
                                game_trail=trail_data,
                                game_progress=0,
                                game_status='In Progress',
                                )

            # Redirect to game.html
            return HttpResponseRedirect('/game/')

    # get top 5 scores
    top_score_games = get_high_scores(5)

    # Add it all to context dictionary
    context = {
        "object": trail_data,
        "top_scores": top_score_games,
        }
    return render(request, "trail/trail_main.html", context)


@login_required(login_url='/login/')
def game_main_view(request): #, id):
    """
    This view generates the latest game view for the current user.
    It lists the current game stats, player's items and calculates game duration.
    It also checks to see if the trail has been completed (i.e. expected number of items found) and
    if so enables the "Finish" button.  If "Finish" button has been clicked then it returns a rendered request
    of the game_finish.html

    :param request: django request object
    :return: django rendered response

    """
    # Work out which items the current player has got in their game
    current_user = get_current_user(request)
    games_list = get_game_data(current_user)
    game_data = games_list[0]

    # Check if it is a POST from finish button click
    if request.method == 'POST':
        if request.POST.getlist('end_button')[0] == 'Finish':

            # Work out duration
            game_duration = get_current_game_duration(game_data.game_start)
            game_data.game_status = 'Completed'
            game_data.game_duration = game_duration
            game_data.save()

            # Get a pretty string format for duration
            game_duration_str = format_duration(game_duration)

            context = {
                "game_duration": game_duration_str,
            }
            return render(request, "game/game_finish.html", context)

    # Work out items
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
    game_duration = get_current_game_duration(game_data.game_start)

    # Get a pretty string format for duration
    game_duration_str = format_duration(game_duration)

    # Add it all to context dictionary
    context = {
        "items": items,
        "current_items": current_items,
        "object": game_data,
        "duration": game_duration_str,
        "complete": trail_completed,
        }

    return render(request, "game/game_main.html", context)


@login_required(login_url='/login/')
def location_detail_view(request, id):
    """
    This view generates a location view based on the "id" .
    It gets the location data for the given "id" from the location table in the database.
    It checks to see if request is a post and if so works out which item was associated with the click.  It then adds
    the new item to the players inventory (in Game table).  If an item has been collected then it will redirect
    to "/game/".  Else it will render the location

    :param request: django request object
    :param id: location id from the url
    :return: django rendered response or redirect

    """

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


# @login_required(login_url='/login/')
# def game_finish_view(request):
#     print("------------ game_finish_view -----------------")
#
#     #return render(request, "game/game_finish.html", {})

