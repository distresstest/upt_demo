"""Utility functions required to get data for views"""
from datetime import datetime, timezone
import re

from .models import Game, Events, Location, Context

def get_game_data(user):
    """
    Get game data

    :param user: django user object
    :return: queryset containing all the games for the user provided

    """
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


def get_high_scores(number):
    """
    Get the top n scores where n = number

    :param number: integer of the number of scores required
    :return: queryset containing top n games

    """
    games_list = Game.objects.order_by('game_duration')[:number]
    print(games_list)
    game_data = games_list[0]
    print(game_data)
    for game in games_list:
        print('*** %s  -  %s ***' % (game.game_player, game.game_duration))

    return games_list


def get_current_user(request):
    """
    Just return the current user

    :param request: django request packet
    :return: django user object

    """

    current_user = request.user
    print('Current User = %s' % current_user)
    return current_user


def get_current_game_duration(start_time):
    """
    Just return the current game duration

    :param start_time: start datetime object
    :return: game_duration datetime timedelta object

    """
    now = datetime.now(timezone.utc)
    game_duration = now - start_time
    return game_duration


def format_duration(time_delta):
    """
    Just return pretty format od a timedelta object

    :param time_delta: time_delta object (e.g. duration)
    :return: game_duration_str:  duration string

    """
    # Process for neat printing to screen
    td = str(time_delta).split('.')[0]
    h,m,s = re.split(':', td)
    game_duration_str = ('%s Hours, %s Minutes & %s Seconds' % (h, m, s))

    return game_duration_str



def get_actions(game_id):


    games_list = Game.objects.filter(id=game_id)

    return games_list


def get_game_events(game_id):
    """
    Get events from a game instance

    :param game_id: integer, id of game record
    :return event_list: list events (by name)

    """
    event_list = []
    # get events in game
    games_list = Game.objects.filter(id=game_id)
    events = Events.objects.distinct().filter(game__in=games_list)

    #print("The following events are in game_events...")
    for event in events:
        #print("> %s : %s" % (event.id, event.event_name))
        event_list.append(event.event_name)

    return event_list


def add_events_to_game(game_id, event_ids):
    """
    Add events to game instance

    :param game_id: integer, id of game record
    :param event_ids: list, of event ids to be added

    """
    for event_id in event_ids:
        current_event = Events(id=event_id)
        current_game = Game(id=game_id)
        current_game.game_event_list.add(current_event)


def get_current_context(game_id, location_id):
    """
    Work out the current context in a location for a given game
    Get contexts for the location provided
    Get events for game provided and check against each context enable requirements
    Return the highest context index where enable requirements match

    :param game_id: integer, id of game record
    :param location_id: integer, id of location record
    :return current_context: integer,  id of the context record

    """

    # Get events in game
    current_game_events = get_game_events(game_id)
    print("Events in current game are... %s" % current_game_events)

    # Get location data
    location_list = Location.objects.filter(id=location_id)
    current_location = location_list[0]
    print("Current location = %s" % current_location.location_name)

    # Get contexts for current location
    context_list = Context.objects.filter(context_location=current_location)
    print('context_list = %s' % context_list)

    # Loop through contexts and find the a match based on game events
    current_context_number = 0
    for context in context_list:
        context_enable_list = []
        context_enables = (context.context_enable.all())
        if context_enables:
            for context_enable in context_enables:
                context_enable_list.append(context_enable.event_name)
        else:
            print('This context requires no enable events')

        print('context_enable_list = %s' % context_enable_list)

        # Check if context enable events are in game events
        if set(context_enable_list).issubset(current_game_events):
            current_context_number = context.context_index

    return current_context_number


def get_actions_for_context(context_index, location_id):
    """
    Return actions for the given context_id

    :param context_id: integer, id of game record
    :param location_id: integer, id of location record
    :return context_actions: integer,  list of enabled actions id for the context of a location

    """


    # Get location data
    location_list = Location.objects.filter(id=location_id)
    current_location = location_list[0]
    print("Current location = %s" % current_location.location_name)

    # Get contexts for current location
    context_list = Context.objects.filter(context_index=context_index, context_location=current_location)
    print('context_list = %s' % context_list)
    return context_list
