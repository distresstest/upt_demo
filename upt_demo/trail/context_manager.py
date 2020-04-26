# import django
# from django.conf import settings
# from upt_demo.trail import trail_defaults
#
# settings.configure(default_settings=trail_defaults, DEBUG=True)
# django.setup()

from .models import Game, Item, Event, Location, Context


class ContextManager(object):
    """Context Manager"""

    def __init__(self, game_id, location_id):
        """
        :param game_id: Id of the current game
        :param location_id: Id of the current location

        """

        self.current_context_number = 0
        self.current_context = None
        self.location_id = location_id

        # Get game data based on id specified
        self.games_list = Game.objects.filter(id=game_id)
        self.current_game = self.games_list[0]
        print('Game Id = %s' % self.current_game.id)
        print('Game Name = %s' % self.current_game.game_name)
        print('Game Mission = %s' % self.current_game.game_mission)

        # Get location data based on id specified
        self.location_list = Location.objects.filter(id=self.location_id)
        self.location = Location.objects.get(id=location_id)
        print('Current location = %s' % self.location)

        # Work out current events
        event_list = []
        self.game_events = Event.objects.distinct().filter(game__in=self.games_list)
        print("self.game_events = %s" % self.game_events)

        # Get contexts for current location
        self.context_list = Context.objects.filter(context_location=self.location)
        print('self.context_list = %s' % self.context_list)

    def get_current_items(self):
        """
        Work out which items are currently at the location for the given context

        :return: context_inventory: List of item record that are still present at location
        """

        # Get items in location inventory
        location_items = Item.objects.distinct().filter(location__in=self.location_list)
        print('> Location items = %s' % location_items)

        # Loop through items in self.game_events
        print(location_items)
        context_inventory = []
        for local_item in location_items:
            #print('location_item = %s' % local_item.item_name)
            item_event = "TOOK_" + local_item.item_name.replace(" ", "_").upper()
            #print('item_event = %s' % item_event)

            # Check if local_item is in self.game_events
            #print(self.game_events)
            found = False
            for game_event in self.game_events:
                if item_event == game_event.event_name:
                    print("Item has already been taken.  Not Appending!")
                    found = True

            if not found:
                print("Item has NOT been taken!  Appending %s" % item_event)
                context_inventory.append(local_item)

        return context_inventory

    def get_current_context(self):
        """
        Work out the current context in a location for a given game
        Get contexts for the location provided
        Get events for game provided and check against each context enable requirements
        Return the highest context index where enable requirements match

        :return current_context: current context record

        """

        # Loop through each context and find the a match based on game events
        self.current_context_number = 0
        for context in self.context_list:
            context_enable_events_list = []
            context_enable_events = (context.context_enable_events.all())
            if context_enable_events:
                for context_enable_event in context_enable_events:
                    print("Appending context_enable_event = %s" % context_enable_event)
                    context_enable_events_list.append(context_enable_event)
            else:
                print('This context requires no enable events')

            # Check if context enable events are in game events
            print("Checking if self.game_events (%s) are in context_enable_events_list (%s)..." % (self.game_events, context_enable_events_list))
            if set(context_enable_events_list).issubset(self.game_events):
                self.current_context_number = context.context_index
                self.current_context = context

        return self.current_context

    def concatenate_context(self, context_index):
        """
        Takes the context index and concatenates all of contexts together and returns the story so far

        :param context_index:
        :return: story_so_far: str
        """

        location_context_so_far = Context.objects.filter(context_location=self.location_id, context_index__lte=context_index)
        context_text = list(location_context_so_far.values_list('context_text', flat=True))
        context_text_section = '\n'.join(context_text)

        return context_text_section


if __name__ == '__main__':
    pass
