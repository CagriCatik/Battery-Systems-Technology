class StateMachine:
    def __init__(self):
        self.state = 'initial'
        self.transitions = {
            'initial': {'start': 'running'},
            'running': {'pause': 'paused', 'stop': 'stopped'},
            'paused': {'resume': 'running', 'stop': 'stopped'},
            'stopped': {}
        }

    def trigger(self, event):
        """Trigger a transition based on the current state and event."""
        if event in self.transitions[self.state]:
            self.state = self.transitions[self.state][event]
            print(f"Transitioned to {self.state}")
        else:
            raise ValueError(f"Invalid event '{event}' for state '{self.state}'")

    def get_state(self):
        """Get the current state of the state machine."""
        return self.state


if __name__ == '__main__':
    sm = StateMachine()
    print(f"Initial State: {sm.get_state()}")
    sm.trigger('start')
    print(f"Current State: {sm.get_state()}")
