import unittest
from django.test import TestCase
from .utility_functions import add_events_to_game, get_game_events, get_current_context, get_actions_for_context
from .models import Events, Game, Location, Context, Action


class MyUtilityTestCases(TestCase):
    def setUp(self):
        print("============================================")
        print("Setting up test database...")
        # Create a few events
        Events.objects.create(event_name="EVENT1")
        Events.objects.create(event_name="EVENT2")
        Events.objects.create(event_name="EVENT3")


        # Create a few actions
        a1c1 = Action.objects.create(action_name="CONTEXT1_ACTION1)")
        a2c1 = Action.objects.create(action_name="CONTEXT1_ACTION2)")
        a1c2 = Action.objects.create(action_name="CONTEXT2_ACTION1)")
        a2c2 = Action.objects.create(action_name="CONTEXT2_ACTION2)")
        a3c2 = Action.objects.create(action_name="CONTEXT2_ACTION3)")

        context_1_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_1")
        context_2a_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2A")
        context_2b_enable = Events.objects.create(event_name="EVENT_TO_ENABLE_CONTEXT_2B")

        # Create a location
        Location.objects.create(location_name="Test Location",
                                location_description="This is a test location",
                                )
        location_list = Location.objects.all()
        print('> Total locations =  %s' % len(location_list))
        location = location_list[0]
        print('> Location name = %s' % location.location_name)

        # Create a few contexts for the location created above
        c0 = Context.objects.create(context_index=0, context_text="This is context 0...", context_location=location)
        c1 = Context.objects.create(context_index=1, context_text="This is context 1...", context_location=location)
        c2 = Context.objects.create(context_index=2, context_text="This is context 2...", context_location=location)
        # Add some enable conditions
        c1.context_enable.add(context_1_enable)
        c2.context_enable.add(context_2a_enable, context_2b_enable)
        # Add some actions
        c1.context_action.add(a1c1, a2c1)
        c2.context_action.add(a1c2, a2c2, a3c2)
        # Save the contexts
        c0.save()
        c1.save()
        c2.save()


        # Create a few more events
        Events.objects.create(event_name="EVENT1")
        Events.objects.create(event_name="EVENT2")
        Events.objects.create(event_name="EVENT3")

        # Create a game
        Game.objects.create(game_name="Test Game",
                            game_mission="This is a test mission!",
                            #game_player = "Me",
                            game_url = "test url",
                            #game_trail = "Test Trail",
                            game_status = "In Progress",
                            #game_event_list
                            )

        print("Test database is setup!")
        print("============================================")

    # def test_add_events_to_game(self):
    #     """Add some events to game and check they are present"""
    #     # Set up variables
    #     game_id = 1
    #     event_list = [1, 2, 3]
    #     my_event_list = []
    #
    #     # call function
    #     add_events_to_game(game_id,event_list)
    #     # get events in game
    #     games_list = Game.objects.filter(id=game_id)
    #     events = Events.objects.distinct().filter(game__in=games_list)
    #
    #     for event in events:
    #         my_event_list.append(event.event_name)
    #
    #     self.assertEqual(my_event_list, ['EVENT1', 'EVENT2', 'EVENT3'])
    #
    # def test_get_game_events(self):
    #     # Set up variables
    #     game_id = 1
    #     event_list = [1, 3]
    #     # Add some events to the database
    #     add_events_to_game(game_id, event_list)
    #
    #     # Get event list
    #     my_event_list = get_game_events(game_id)
    #
    #     print(my_event_list)
    #     self.assertEqual(my_event_list, ['EVENT1', 'EVENT3'])
    #
    # def test_get_current_context_index_is_zero(self):
    #     """Check that get_current_context returns 0 when game events don't enable any contexts"""
    #     game_id = 1
    #     location_id = 1
    #     add_events_to_game(game_id, [1])
    #     context_index = get_current_context(game_id, location_id)
    #
    #     print('context number = %s' % context_index)
    #     self.assertEqual(context_index, 0)
    #
    # def test_get_current_context_index_is_1(self):
    #     """Check that get_current_context returns 1 when game event matches with context 1"""
    #     game_id = 1
    #     location_id = 1
    #     add_events_to_game(game_id, [4])
    #     context_index = get_current_context(game_id, location_id)
    #
    #     print('context number = %s' % context_index)
    #     self.assertEqual(context_index, 1)
    #
    # def test_get_current_context_index_is_2(self):
    #     """Check that get_current_context returns 2 when game event matches with context 2"""
    #     game_id = 1
    #     location_id = 1
    #     add_events_to_game(game_id, [5,6])
    #     context_index = get_current_context(game_id, location_id)
    #
    #     print('context number = %s' % context_index)
    #     self.assertEqual(context_index, 2)
    #
    # def test_get_current_context_returns_2_if_events_for_1_and_2(self):
    #     """Check that get_current_context returns 2 when game event matches with context 2 and 1"""
    #     game_id = 1
    #     location_id = 1
    #     add_events_to_game(game_id, [4, 5, 6])
    #     context_index = get_current_context(game_id, location_id)
    #
    #     print('context number = %s' % context_index)
    #     self.assertEqual(context_index, 2)

    def test_get_actions_for_context(self):
        context_index = 1
        location_id = 1

        actions = get_actions_for_context(context_index, location_id)

        print('actions = %s' % actions)


if __name__ == '__main__':
    unittest.main()
