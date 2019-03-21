import math

class Singleton(type):
    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

class Forward(metaclass=Singleton):
    def __init__(self):
        self.player = None
        self.ball = None
        self.side = None

    def update_vals(self, player, ball, side):
        self.player = player
        self.ball = ball
        self.side = side

    def update(self):
        result = dict()
        if not self.behind_the_ball():
            result = self.get_behind_the_ball()
        else:
            if self.in_posession():
                result = self.shoot()
            else:
                result = self.get_posession()
        return result

    def behind_the_ball(self):
        if self.side == 'left':
            return self.player['x'] + self.player['radius'] < self.ball['x'] - self.ball['radius']
        return self.player['x'] - self.player['radius'] > self.ball['x'] + self.ball['radius']

    def get_behind_the_ball(self):
        result = dict()
        result['alpha'] = math.pi
        if self.side == 'right':
            result['alpha'] = 0
        result['force'] = self.player['mass'] * self.player['a_max']
        result['shot_power'] = 0
        result['shot_request'] = False
        return result


    def in_posession(self):
        return (self.player['x'] - self.ball['x'])**2 + (self.player['y'] - self.ball['y'])**2 - (self.player['radius'] + self.ball['radius'])**2 < 100

    def get_posession(self):
        result = dict()
        result['force'] = self.player['mass'] * self.player['a_max']
        result['alpha'] = math.atan((self.player['y'] - self.ball['y']) / (self.player['x'] - self.ball['x']))
        if self.side == 'right':
            result['alpha'] = math.atan((self.player['y'] - self.ball['y']) / (self.player['x'] - self.ball['x'])) - math.pi
        result['shot_power'] = 100
        result['shot_request'] = True
        return result

    def shoot(self):
        result = dict()
        result['force'] = self.player['mass'] * self.player['a_max']
        result['alpha'] = math.atan((self.player['y'] - 460) / (self.player['x'] - 1316))
        if self.side == 'right':
            result['alpha'] = math.atan((self.player['y'] - 460) / (self.player['x'] - 50))
        result['shot_request'] = False
        result['shot_power'] = 0
        return result