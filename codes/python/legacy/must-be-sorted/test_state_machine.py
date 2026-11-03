import unittest
from state_machine import StateMachine 

class TestStateMachine(unittest.TestCase):
    def setUp(self):
        self.sm = StateMachine()

    def test_initial_state(self):
        """Test that the initial state is correctly set."""
        self.assertEqual(self.sm.get_state(), 'initial')

    def test_valid_transitions(self):
        """Test valid transitions."""
        self.sm.trigger('start')
        self.assertEqual(self.sm.get_state(), 'running')

        self.sm.trigger('pause')
        self.assertEqual(self.sm.get_state(), 'paused')

        self.sm.trigger('resume')
        self.assertEqual(self.sm.get_state(), 'running')

        self.sm.trigger('stop')
        self.assertEqual(self.sm.get_state(), 'stopped')

    def test_invalid_transition(self):
        """Test that invalid transitions raise an error."""
        with self.assertRaises(ValueError):
            self.sm.trigger('stop')  # Invalid event in 'initial' state

    def test_no_transition_from_stopped(self):
        """Test that no transitions are allowed from the 'stopped' state."""
        self.sm.trigger('start')
        self.sm.trigger('stop')
        with self.assertRaises(ValueError):
            self.sm.trigger('resume')  # Invalid event in 'stopped' state

if __name__ == '__main__':
    unittest.main()
