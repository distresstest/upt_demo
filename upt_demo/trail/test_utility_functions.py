import unittest
from django.test import TestCase
from .utility_functions import add_events_to_game, get_game_events, get_current_context, get_actions_for_context
from .models import Events, Game, Location, Context, Action


class MyUtilityTestCases(TestCase):
    def setUp(self):
        print("============================================")
        print("Setting up test database...")

        # Create a location
        Location.objects.create(location_name="Test Location", location_description="This is a test location",)
        location_list = Location.objects.all()
        location = location_list[0]
        print('> Created a location, %s' % location.location_name)

        # Create a few events
        Events.objects.create(event_name="EVENT1")  # ----------------------------------------- 1
        Events.objects.create(event_name="EVENT2")  # ----------------------------------------- 2
        Events.objects.create(event_name="EVENT3")  # ----------------------------------------- 3
        action1_event = Events.objects.create(event_name="DONE_ACTION1")  # ------------------- 4
        action2_event = Events.objects.create(event_name="DONE_ACTION2")  # ------------------- 5
        action3_event = Events.objects.create(event_name="DONE_ACTION3")  # ------------------- 6
        context_1_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_1")  # --- 7
        context_2a_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2A")  # - 8
        context_2b_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2B")  # - 9

        # Create a few actions
        # a1c1 = Action.objects.create(action_name="CONTEXT1_ACTION1")
        # a2c1 = Action.objects.create(action_name="CONTEXT1_ACTION2")
        # a1c2 = Action.objects.create(action_name="CONTEXT2_ACTION1")
        # a2c2 = Action.objects.create(action_name="CONTEXT2_ACTION2")
        # a3c2 = Action.objects.create(action_name="CONTEXT2_ACTION3")
        context1_action1 = Action.objects.create(action_name="ACTION1", action_event=action1_event)
        context1_action2 = Action.objects.create(action_name="ACTION2", action_event=action2_event)
        context2_action1 = Action.objects.create(action_name="ACTION3", action_event=action3_event)


        # Create a few contexts for the location created above
        c0 = Context.objects.create(context_index=0, context_text="This is context 0...", context_location=location)
        c1 = Context.objects.create(context_index=1, context_text="This is context 1...", context_location=location)
        c2 = Context.objects.create(context_index=2, context_text="This is context 2...", context_location=location)
        # Add some enable conditions
        c1.context_enable_events.add(context_1_enable)
        c2.context_enable_events.add(context_2a_enable, context_2b_enable)
        # Add some actions
        c1.context_action.add(context1_action1, context1_action2)
        c2.context_action.add(context2_action1)
        # Save the contexts
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

    def test_add_events_to_game(self):
        """Add some events to game and check they are present"""
        # Set up variables
        game_id = 1
        event_list = [1, 2, 3]
        my_event_list = []

        # call function
        add_events_to_game(game_id,event_list)
        # get events in game
        games_list = Game.objects.filter(id=game_id)
        events = Events.objects.distinct().filter(game__in=games_list)

        for event in events:
            my_event_list.append(event.event_name)

        self.assertEqual(my_event_list, ['EVENT1', 'EVENT2', 'EVENT3'])

    def test_get_game_events(self):
        # Set up variables
        game_id = 1
        event_list = [1, 3]
        # Add some events to the database
        add_events_to_game(game_id, event_list)

        # Get event list
        my_event_list = get_game_events(game_id)

        print(my_event_list)
        self.assertEqual(my_event_list, ['EVENT1', 'EVENT3'])

    def test_get_current_context_index_is_zero(self):
        """Check that get_current_context returns 0 when game events don't enable any contexts"""
        game_id = 1
        location_id = 1
        add_events_to_game(game_id, [1])
        context_index = get_current_context(game_id, location_id)

        print('context number = %s' % context_index)
        self.assertEqual(context_index, 0)

    def test_get_current_context_index_is_1(self):
        """Check that get_current_context returns 1 when game event matches with context 1"""
        game_id = 1
        location_id = 1
        add_events_to_game(game_id, [7])
        print(get_game_events(game_id))
        context_index = get_current_context(game_id, location_id)

        print('context number = %s' % context_index)
        self.assertEqual(context_index, 1)

    def test_get_current_context_index_is_2(self):
        """Check that get_current_context returns 2 when game event matches with context 2"""
        game_id = 1
        location_id = 1
        add_events_to_game(game_id, [8,9])
        context_index = get_current_context(game_id, location_id)

        print('context number = %s' % context_index)
        self.assertEqual(context_index, 2)

    def test_get_current_context_returns_2_if_events_for_1_and_2(self):
        """Check that get_current_context returns 2 when game event matches with context 2 and 1"""
        game_id = 1
        location_id = 1
        add_events_to_game(game_id, [7, 8, 9])
        context_index = get_current_context(game_id, location_id)

        print('context number = %s' % context_index)
        self.assertEqual(context_index, 2)

    def test_get_actions_for_context_for_context_1(self):
        """Check that get_actions_for_context returned a list of the correct actions"""
        context_index = 1
        location_id = 1
        game_id = 1

        actions = get_actions_for_context(context_index, location_id, game_id)

        self.assertEqual(actions, ['ACTION1', 'ACTION2'])

    def test_get_actions_for_context_for_context_2(self):
        """Check that get_actions_for_context returned a list of the correct actions"""
        context_index = 2
        location_id = 1
        game_id = 1

        actions = get_actions_for_context(context_index, location_id, game_id)

        self.assertEqual(actions, ['ACTION3'])

    def test_get_actions_returns_no_actions_if_already_done(self):
        """Check that get_actions_for_context returns empty list if actions already done"""
        context_index = 1
        location_id = 1
        game_id = 1
        add_events_to_game(game_id, [4, 5])
        actions = get_actions_for_context(context_index, location_id, game_id)
        print('Actions returned = %s' % actions)

        self.assertEqual(actions, [])

    def test_get_actions_returns_correrct_actions_if_action1_already_done(self):
        """Check that get_actions_for_context returns empty list if actiona already done"""
        context_index = 1
        location_id = 1
        game_id = 1
        add_events_to_game(game_id, [4])
        actions = get_actions_for_context(context_index, location_id, game_id)
        print('Actions returned = %s' % actions)

        self.assertEqual(actions, ['ACTION2'])

    def test_get_actions_returns_correrct_actions_if_action2_already_done(self):
        """Check that get_actions_for_context returns empty list if actiona already done"""
        context_index = 1
        location_id = 1
        game_id = 1
        add_events_to_game(game_id, [5])
        actions = get_actions_for_context(context_index, location_id, game_id)
        print('Actions returned = %s' % actions)

        self.assertEqual(actions, ['ACTION1'])


if __name__ == '__main__':
    unittest.main()
