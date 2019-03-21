import math

infinity = float('inf')

class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class Middle(metaclass=Singleton):
    x_position_left = 370
    x_position_right = 996

    def __init__(self):
        self.player = None
        self.ball = None
        self.side = None

    def update_vals(self, player, ball, side):
        self.player = player
        self.ball = ball
        self.side = side

    def in_front_of_ball(self):
        if self.side == 'left':
            return self.player['x'] > self.ball['x']
        return self.player['x'] < self.ball['x']

    def update(self):
        max_force = self.player['a_max'] * self.player['mass']
        x_position = self.x_position_left
        if self.side == 'right':
            x_position = self.x_position_right
        result = dict()
        if self.in_front_of_ball():
            result['shot_request'] = False
            result['shot_power'] = 0
            result['alpha'] = math.pi
            if self.side == 'right':
                result['alpha'] = 0
            result['force'] = -infinity
        else:
            if self.side == 'left':
                if self.player['x'] >= x_position:
                    result['alpha'] = math.pi
                    result['force'] = max_force
                else:
                    if self.player['y'] > self.ball['y']:
                        result['alpha'] = math.pi * 3 / 2
                        result['force'] = max_force
                    elif self.player['y'] < self.ball['y']:
                        result['alpha'] = math.pi / 2
                        result['force'] = max_force
                    else:
                        result['force'] = 0
                        result['alpha'] = 0
            else:
                if self.player['x'] <= x_position:
                    result['alpha'] = 0
                    result['force'] = max_force
                else:
                    if self.player['y'] > self.ball['y']:
                        result['alpha'] = math.pi * 3 / 2
                        result['force'] = max_force
                    elif self.player['y'] < self.ball['y']:
                        result['alpha'] = math.pi / 2
                        result['force'] = max_force
                    else:
                        result['alpha'] = math.pi
                        result['force'] = 0
            result['shot_power'] = self.player['shot_power_max']
            result['shot_request'] = True
        return result
