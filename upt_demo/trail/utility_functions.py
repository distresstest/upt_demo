"""Utility functions required to get data for views"""
from datetime import datetime, timezone
import re

from .models import Game

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
    games_list = Game.objects.order_by('-game_duration')[:number]
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
