import unittest
from django.test import TestCase
from .context_manager import ContextManager
from .models import Game, Item, Event, Context, Location
from .utility_functions import add_events_to_game


class ContextManagerTests(TestCase):

    def setUp(self):
        print("============================================")
        print("Setting up test database...")

        # Create some items
        item1 = Item.objects.create(item_name="ITEM1", item_description="This is Item 1")
        item2 = Item.objects.create(item_name="ITEM2", item_description="This is Item 2")
        item3 = Item.objects.create(item_name="ITEM3", item_description="This is Item 3")
        item4 = Item.objects.create(item_name="ITEM4", item_description="This is Item 4")
        item5 = Item.objects.create(item_name="ITEM5", item_description="This is Item 5")

        # Create a location
        location1 = Location.objects.create(location_name="Test Location", location_description="This is a test location", )
        location_list = Location.objects.all()
        location = location_list[0]
        print('> Created a location, %s' % location.location_name)

        # Add items to location
        location1.location_inventory.add(item1)
        location1.location_inventory.add(item2)
        location1.location_inventory.add(item3)

        # Create a few events
        Event.objects.create(event_name="EVENT1")  # ----------------------------------------- 1
        Event.objects.create(event_name="EVENT2")  # ----------------------------------------- 2
        Event.objects.create(event_name="EVENT3")  # ----------------------------------------- 3
        context_1_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_1")  # --- 4
        context_2a_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2A")  # - 5
        context_2b_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2B")  # - 6
        Event.objects.create(event_name="TOOK_ITEM1")  # --------------------------------------7
        Event.objects.create(event_name="TOOK_ITEM2")  # --------------------------------------8
        Event.objects.create(event_name="TOOK_ITEM3")  # --------------------------------------9

        # Create a few contexts for the location created above
        c0 = Context.objects.create(context_index=0, context_text="This is context 0...", context_location=location)
        c1 = Context.objects.create(context_index=1, context_text="This is context 1...", context_location=location)
        c2 = Context.objects.create(context_index=2, context_text="This is context 2...", context_location=location)

        # Add some enable conditions
        c1.context_enable_events.add(context_1_enable)
        c2.context_enable_events.add(context_2a_enable, context_2b_enable)
        c0.save()
        c1.save()
        c2.save()

        # Create a basic game
        Game.objects.create(game_name="Test Game",
                            game_mission="This is a test mission!",
                            game_url="test url",
                            game_status="In Progress",
                            )

        print("Test database is setup!")
        print("============================================")

    def test_get_current_context_index_is_zero(self):
        """Check that get_current_context returns 0 when game events don't enable any contexts"""
        game_id = 1
        location_id = 1
        # add_events_to_game(game_id, [1])
        # context_index = get_current_context(game_id, location_id)

        cm = ContextManager(game_id, location_id)
        my_context = cm.get_current_context()

        print('context number = %s' % my_context)
        self.assertEqual(my_context.context_index, 0)

    def test_get_current_context_index_is_1(self):
        """Check that get_current_context returns 1 when game event matches with context 1"""
        game_id = 1
        location_id = 1

        add_events_to_game(game_id, [4])

        cm = ContextManager(game_id, location_id)
        my_context = cm.get_current_context()

        self.assertEqual(my_context.context_index, 1)

    def test_get_current_context_index_is_2(self):
        """Check that get_current_context returns 2 when game event matches with context 2"""
        game_id = 1
        location_id = 1

        add_events_to_game(game_id, [5, 6])

        cm = ContextManager(game_id, location_id)
        my_context = cm.get_current_context()

        self.assertEqual(my_context.context_index, 2)

    def test_get_current_items_returns_all_items(self):
        """Check that get_get_current_items returns all items if none have been taken"""
        game_id = 1
        location_id = 1

        add_events_to_game(game_id, [5, 6])

        cm = ContextManager(game_id, location_id)
        my_items = cm.get_current_items()

        self.assertQuerysetEqual(my_items, ['<Item: ITEM1>', '<Item: ITEM2>', '<Item: ITEM3>'])

    def test_get_current_items_returns_item2_and_item3(self):
        """Check that get_get_current_items returns item 2 & 3 items if item 1 has been taken"""
        game_id = 1
        location_id = 1

        add_events_to_game(game_id, [5, 6, 7])

        cm = ContextManager(game_id, location_id)
        my_items = cm.get_current_items()

        self.assertQuerysetEqual(my_items, ['<Item: ITEM2>', '<Item: ITEM3>'])


if __name__ == '__main__':
    unittest.main()
