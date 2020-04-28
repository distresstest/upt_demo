import unittest
from django.test import TestCase
from .action_manager import ActionManager
from .context_manager import ContextManager
from .models import Game, Item, Event, Location, Context, Action
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
        context_1_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_1")  # --- 7
        context_2a_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2A")  # - 8
        context_2b_enable = Event.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2B")  # - 9
        action1_event = Event.objects.create(event_name="DONE_ACTION1")  # ------------------- 10
        action2_event = Event.objects.create(event_name="DONE_ACTION2")  # ------------------- 11
        action3_event = Event.objects.create(event_name="DONE_ACTION3")  # ------------------- 12

        # Create a few actions
        context1_action1 = Action.objects.create(action_name="ACTION1", action_event=action1_event)
        context1_action2 = Action.objects.create(action_name="ACTION2", action_event=action2_event)
        context2_action1 = Action.objects.create(action_name="ACTION3", action_event=action3_event)

        # Create a few contexts for the location created above
        c0 = Context.objects.create(context_index=0, context_text="This is context 0...", context_location=location)
        c1 = Context.objects.create(context_index=1, context_text="This is context 1...", context_location=location)
        c2 = Context.objects.create(context_index=2, context_text="This is context 2...", context_location=location)

        # Add some enable conditions
        c1.context_enable_events.add(context_1_enable)
        c1.context_action.add()
        c2.context_enable_events.add(context_2a_enable, context_2b_enable)

        # Add some actions
        c1.context_action.add(context1_action1, context1_action2)
        c2.context_action.add(context2_action1)

        c0.save()
        c1.save()
        c2.save()

        # Create a basic game
        Game.objects.create(game_name="Test Game",
                            game_mission="This is a test mission!",
                            game_url = "test url",
                            game_status = "In Progress",
                            )

        print("Test database is setup!")
        print("============================================")

#     def test_take_item_1 (self):
#         """Test that the id on the item provided is added to the games event list"""
#
#         game_id = 1
#         item_id = 1
#         am = ActionManager(game_id)
#         item_event = am.take_item(item_id)
#
#         self.assertEqual(item_event.event_name, "TOOK_ITEM1")
#
#     def test_take_item_2 (self):
#         """Test that the id on the item provided is added to the games event list"""
#
#         game_id = 1
#         item_id = 2
#         am = ActionManager(game_id)
#         item_event = am.take_item(item_id)
#
#         self.assertEqual(item_event.event_name, "TOOK_ITEM2")
#
#     def test_use_item_2(self):
#         """Test that the id on the item provided is used if not in games event list"""
#
#         game_id = 1
#         item_id = 2
#         am = ActionManager(game_id)
#         item_event = am.take_item(item_id)
#
#         item_event = am.use_item(item_id)
#
#         self.assertEqual(item_event.event_name, "USED_ITEM2")
#
#
#     def test_use_item_2_if_not_in_game_inventory_returns_false(self):
#         """Test that the id on the item provided is not used if not in games event list"""
#
#         game_id = 1
#         item_id = 2
#         am = ActionManager(game_id)
#         item_event = am.take_item(item_id)
#
#         item_event = am.use_item(1)
#
#         self.assertEqual(item_event, False)
#
#     def test_take_item_updates_items_list(self):
#         """Test that..."""
#
#         game_id = 1
#         item_id = 1
#         am = ActionManager(game_id)
#         am.take_item(item_id)
#
#         self.assertQuerysetEqual(am.items, ['<Item: ITEM1>'])
#
#     def test_work_out_current_actions_no_items(self):
#         """Test that..."""
#
#         game_id = 1
#         location_id = 1
#         am = ActionManager(game_id)
#         cm = ContextManager(game_id, location_id)
#
#         current_items = cm.get_current_items()
#         print(current_items)
#
#         current_actions = am.work_out_current_actions(current_items)
#
#         self.assertEqual(current_actions, [{'action': 'Take "ITEM1"', 'item_id': 1, 'item_name': 'ITEM1'},
#                                            {'action': 'Take "ITEM2"', 'item_id': 2, 'item_name': 'ITEM2'},
#                                            {'action': 'Take "ITEM3"', 'item_id': 3, 'item_name': 'ITEM3'}]
#
# )
#
    # def test_work_out_current_actions_1_item(self):
    #     """Test that..."""
    #
    #     game_id = 1
    #     location_id = 1
    #     item_id = 1
    #     am = ActionManager(game_id)
    #     cm = ContextManager(game_id, location_id)
    #
    #     am.take_item(item_id)
    #
    #     current_items = cm.get_current_items()
    #     print(current_items)
    #
    #     current_actions = am.work_out_current_actions(current_items)
    #
    #     self.assertEqual(current_actions,   [{'action': 'Take "ITEM2"', 'item_id': 2, 'item_name': 'ITEM2'},
    #                                          {'action': 'Take "ITEM3"', 'item_id': 3, 'item_name': 'ITEM3'},
    #                                          {'action': 'Use "ITEM1"', 'item_id': 1, 'item_name': 'ITEM1'}])



    # def test_test(self):
    #
    #     game_id = 1
    #     location_id = 1
    #     item_id = 1
    #     am = ActionManager(game_id)
    #     cm = ContextManager(game_id, location_id)
    #
    #     add_events_to_game(game_id, [7])  # Enable context 1
    #
    #     my_current_context = cm.get_current_context()
    #     # my_current_context_list = Context.objects.all()
    #     # my_current_context = my_current_context_list[1]
    #
    #     #my_current_context.context_action.add(my_current_context)
    #
    #     my_current_context_actions = my_current_context.context_action.all()
    #     print('Current actions are ... %s' % my_current_context_actions)
    #
    #     #
    #     my_actions = am.work_out_current_actions(my_current_context)
    #     # for action in my_actions:
    #     #print(my_current_context_actions)

    def test_perform_action(self):
        """Test perform action"""

        game_id = 1
        location_id = 1
        item_id = 1
        am = ActionManager(game_id)
        cm = ContextManager(game_id, location_id)

        add_events_to_game(game_id, [7])  # Enable context 1

        my_current_context = cm.get_current_context()
        # my_current_context_list = Context.objects.all()
        # my_current_context = my_current_context_list[1]

        #my_current_context.context_action.add(my_current_context)

        my_current_context_actions = my_current_context.context_action.all()
        print('Current actions are ... %s' % my_current_context_actions)

        #
        my_actions = am.work_out_current_actions(my_current_context)
        action =  my_actions[1]
        am.perform_action(action)



if __name__ == '__main__':
    unittest.main()
