import unittest
from django.test import TestCase
from .action_manager import ActionManager
from .context_manager import ContextManager
from .models import Game, Item, Event, Location
from .utility_functions import add_events_to_game

class ActionManagerTests(TestCase):

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
        Event.objects.create(event_name="TOOK_ITEM1")  # ----------------------------------------- 1
        Event.objects.create(event_name="TOOK_ITEM2")  # ----------------------------------------- 2
        Event.objects.create(event_name="TOOK_ITEM3")  # ----------------------------------------- 3
        Event.objects.create(event_name="USED_ITEM1")   # ----------------------------------------- 4
        Event.objects.create(event_name="USED_ITEM2")   # ----------------------------------------- 5
        Event.objects.create(event_name="USED_ITEM3")   # ----------------------------------------- 6

        # Create a basic game
        Game.objects.create(game_name="Test Game",
                            game_mission="This is a test mission!",
                            game_url = "test url",
                            game_status = "In Progress",
                            )

        print("Test database is setup!")
        print("============================================")

    def test_take_item_1 (self):
        """Test that the id on the item provided is added to the games event list"""

        game_id = 1
        item_id = 1
        am = ActionManager(game_id)
        item_event = am.take_item(item_id)

        self.assertEqual(item_event.event_name, "TOOK_ITEM1")

    def test_take_item_2 (self):
        """Test that the id on the item provided is added to the games event list"""

        game_id = 1
        item_id = 2
        am = ActionManager(game_id)
        item_event = am.take_item(item_id)

        self.assertEqual(item_event.event_name, "TOOK_ITEM2")

    def test_use_item_2(self):
        """Test that the id on the item provided is used if not in games event list"""

        game_id = 1
        item_id = 2
        am = ActionManager(game_id)
        item_event = am.take_item(item_id)

        item_event = am.use_item(item_id)

        self.assertEqual(item_event.event_name, "USED_ITEM2")


    def test_use_item_2_if_not_in_game_inventory_returns_false(self):
        """Test that the id on the item provided is not used if not in games event list"""

        game_id = 1
        item_id = 2
        am = ActionManager(game_id)
        item_event = am.take_item(item_id)

        item_event = am.use_item(1)

        self.assertEqual(item_event, False)

    def test_take_item_updates_items_list(self):
        """Test that..."""

        game_id = 1
        item_id = 1
        am = ActionManager(game_id)
        am.take_item(item_id)

        self.assertQuerysetEqual(am.items, ['<Item: ITEM1>'])

    def test_work_out_current_actions_no_items(self):
        """Test that..."""

        game_id = 1
        location_id = 1
        am = ActionManager(game_id)
        cm = ContextManager(game_id, location_id)

        current_items = cm.get_current_items()
        print(current_items)

        current_actions = am.work_out_current_actions(current_items)

        self.assertEqual(current_actions, [{'action': 'Take "ITEM1"', 'item_id': 1, 'item_name': 'ITEM1'},
                                           {'action': 'Take "ITEM2"', 'item_id': 2, 'item_name': 'ITEM2'},
                                           {'action': 'Take "ITEM3"', 'item_id': 3, 'item_name': 'ITEM3'}]

)

    def test_work_out_current_actions_1_item(self):
        """Test that..."""

        game_id = 1
        location_id = 1
        item_id = 1
        am = ActionManager(game_id)
        cm = ContextManager(game_id, location_id)

        am.take_item(item_id)

        current_items = cm.get_current_items()
        print(current_items)

        current_actions = am.work_out_current_actions(current_items)

        self.assertEqual(current_actions,   [{'action': 'Take "ITEM2"', 'item_id': 2, 'item_name': 'ITEM2'},
                                             {'action': 'Take "ITEM3"', 'item_id': 3, 'item_name': 'ITEM3'},
                                             {'action': 'Use "ITEM1"', 'item_id': 1, 'item_name': 'ITEM1'}])




if __name__ == '__main__':
    unittest.main()
