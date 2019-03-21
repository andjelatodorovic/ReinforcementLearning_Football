import pygame
from constants import *
import numpy as np
import pandas as pd


def collision(circle_1, circle_2):
    return (circle_1.x - circle_2.x)**2 + (circle_1.y - circle_2.y)**2 <= (circle_1.radius + circle_2.radius)**2


class Circle:
    def __init__(self, x=0, y=0, radius=0, mass=1, alpha=0):
        self.x = x
        self.y = y
        self.radius = radius
        self.mass = mass
        self.alpha = alpha
        self.v = 0


class Player(Circle):
    a_fifa = 0.75
    v_fifa = 0.88
    shot_power_fifa = 0.95
    a_max_coeff = 22 # 22 max
    v_max_coeff = 7 # 7 max?
    shot_power_max_coeff = 200
    a_max = a_max_coeff * a_fifa
    v_max = v_max_coeff * v_fifa
    shot_power_max = shot_power_max_coeff * shot_power_fifa
    shot_power = shot_power_max
    shot_request = False

    def __init__(self, number):
        df = pd.read_csv('players.csv', index_col='Index')
        player = df.loc[number]
        self.mass = int(player['Kilograms'])
        self.radius = int(player['Radius'])
        self.a_fifa = int(player['Acceleration'])
        self.v_fifa = int(player['Speed'])
        self.shot_power_fifa = int(player['Shot_power'])
        self.v_max = self.v_max_coeff * self.v_fifa
        self.a_max = self.a_max_coeff * self.a_fifa
        self.shot_power_max = self.shot_power_max_coeff * self.shot_power_fifa

    def move(self, manager_decision):
        force = np.clip(manager_decision['force'], -0.5 * self.a_max * self.mass, self.a_max * self.mass)
        self.alpha = manager_decision['alpha']
        self.shot_power = np.clip(manager_decision['shot_power'], 0, self.shot_power_max)
        self.shot_request = manager_decision['shot_request']
        self.v += force / self.mass * dt
        self.v = np.clip(self.v, 0, self.v_max)
        self.x += np.cos(self.alpha) * self.v * dt
        self.y += np.sin(self.alpha) * self.v * dt

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, [int(self.x), int(self.y)], self.radius)
        new_x = self.x + self.radius * np.cos(self.alpha)
        new_y = self.y + self.radius * np.sin(self.alpha)
        pygame.draw.line(screen, black, [self.x, self.y], [new_x, new_y], cursor_width)

    def data(self):
        player_data = {'x': self.x, 'y': self.y, 'alpha': self.alpha, 'mass': self.mass, 'radius': self.radius,
                       'v_max': self.v_max, 'a_max': self.a_max, 'shot_power': self.shot_power,
                       'shot_power_max': self.shot_power_max, 'shot_power_fifa': self.shot_power_fifa}
        return player_data

    def snelius(self):
        if self.y + self.radius >= ground[3] and np.sin(self.alpha) > 0:
            self.alpha = -self.alpha
            self.v *= np.abs(np.cos(self.alpha))
        if self.y - self.radius <= ground[1] and np.sin(self.alpha) < 0:
            self.alpha = -self.alpha
            self.v *= np.abs(np.cos(self.alpha))
        if self.x + self.radius >= ground[2] and np.cos(self.alpha) > 0:
            self.alpha = np.pi - self.alpha
            self.v *= np.abs(np.sin(self.alpha))
        if self.x - self.radius <= ground[0] and np.cos(self.alpha) < 0:
            self.alpha = -np.pi - self.alpha
            self.v *= np.abs(np.sin(self.alpha))

    def reset(self, initial_position, alpha):
        self.x = initial_position[0]
        self.y = initial_position[1]
        self.alpha = alpha
        self.v = 0

    def clip_velocity(self):
        self.v = np.clip(self.v, 0, self.v_max)


class Ball(Circle):
    v_max = 850
    radius = 15
    mass = 0.5

    def move(self):
        self.x += np.cos(self.alpha) * self.v * dt
        self.y += np.sin(self.alpha) * self.v * dt
        self.v *= 0.99

    def draw(self, screen):
        pygame.draw.circle(screen, black, [int(self.x), int(self.y)], self.radius)
        pygame.draw.circle(screen, white, [int(self.x), int(self.y)], self.radius - 2)

    def snelius(self):
        goal = post_screen_top < self.y < post_screen_bottom
        if self.y + self.radius >= playground[3] and np.sin(self.alpha) > 0:
            self.alpha = -self.alpha
            self.y = playground[3] - self.radius
        if self.y - self.radius <= playground[1] and np.sin(self.alpha) < 0:
            self.alpha = -self.alpha
            self.y = playground[1] + self.radius
        if self.x + self.radius >= playground[2] and np.cos(self.alpha) > 0 and not goal:
            self.alpha = np.pi - self.alpha
            self.x = playground[2] - self.radius
        if self.x - self.radius <= playground[0] and np.cos(self.alpha) < 0 and not goal:
            self.alpha = -np.pi - self.alpha
            self.x = playground[0] + self.radius

    def reset(self):
        self.x = center[0]
        self.y = center[1]
        self.alpha = 0
        self.v = 0

    def data(self):
        ball_data = {'x': self.x, 'y': self.y, 'alpha': self.alpha, 'mass': self.mass, 'radius': self.radius}
        return ball_data

    def clip_velocity(self):
        self.v = np.clip(self.v, 0, self.v_max)


class Post(Circle):
    def draw(self, screen):
        pygame.draw.circle(screen, white, [int(self.x), int(self.y)], self.radius)


def resolve_collision(circle_1, circle_2):
    collision_angle = np.arctan2(circle_2.y - circle_1.y, circle_2.x - circle_1.x)

    new_x_speed_1 = circle_1.v * np.cos(circle_1.alpha - collision_angle)
    new_y_speed_1 = circle_1.v * np.sin(circle_1.alpha - collision_angle)
    new_x_speed_2 = circle_2.v * np.cos(circle_2.alpha - collision_angle)
    new_y_speed_2 = circle_2.v * np.sin(circle_2.alpha - collision_angle)

    final_x_speed_1 = ((circle_1.mass - circle_2.mass) * new_x_speed_1
                       + (circle_2.mass + circle_2.mass) * new_x_speed_2) / (circle_1.mass + circle_2.mass)
    final_x_speed_2 = ((circle_1.mass + circle_1.mass) * new_x_speed_1
                       + (circle_2.mass - circle_1.mass) * new_x_speed_2) / (circle_1.mass + circle_2.mass)
    final_y_speed_1 = new_y_speed_1
    final_y_speed_2 = new_y_speed_2

    cos_gamma = np.cos(collision_angle)
    sin_gamma = np.sin(collision_angle)
    circle_1.v_x = cos_gamma * final_x_speed_1 - sin_gamma * final_y_speed_1
    circle_1.v_y = sin_gamma * final_x_speed_1 + cos_gamma * final_y_speed_1
    circle_2.v_x = cos_gamma * final_x_speed_2 - sin_gamma * final_y_speed_2
    circle_2.v_y = sin_gamma * final_x_speed_2 + cos_gamma * final_y_speed_2

    x_difference = circle_1.x - circle_2.x
    y_difference = circle_1.y - circle_2.y
    d = np.linalg.norm([x_difference, y_difference])

    # minimum translation distance to push balls apart after intersecting
    mtd_x = x_difference * (((circle_1.radius + circle_2.radius) - d) / d)
    mtd_y = y_difference * (((circle_1.radius + circle_2.radius) - d) / d)
    im1 = 1 / circle_1.mass if circle_1.mass > 0 else 0
    im2 = 1 / circle_2.mass if circle_2.mass > 0 else 0

    # push-pull them apart based off their mass
    circle_1.x += mtd_x * (im1 / (im1 + im2))
    circle_1.y += mtd_y * (im1 / (im1 + im2))
    circle_2.x -= mtd_x * (im2 / (im1 + im2))
    circle_2.y -= mtd_y * (im2 / (im1 + im2))

    if isinstance(circle_1, Player) and isinstance(circle_2, Player):
        circle_1.v = player_player_restitution * np.sqrt(circle_1.v_x**2 + circle_1.v_y**2)
        circle_2.v = player_player_restitution * np.sqrt(circle_2.v_x**2 + circle_2.v_y**2)
    if isinstance(circle_1, Player) and isinstance(circle_2, Ball):
        circle_1.v = np.sqrt(circle_1.v_x**2 + circle_1.v_y**2)
        if circle_1.shot_request:
            circle_2.v = np.sqrt(circle_2.v_x**2 + circle_2.v_y**2)
            circle_2.v = circle_1.shot_power * circle_1.mass / (circle_1.mass + circle_2.mass) * (1 + ball_restitution)
        else:
            circle_2.v = ball_restitution_under_player_control * np.sqrt(circle_2.v_x**2 + circle_2.v_y**2)
    if isinstance(circle_1, Player) and isinstance(circle_2, Post):
        circle_1.v = player_post_restitution * np.sqrt(circle_1.v_x**2 + circle_1.v_y**2)
        circle_2.v = 0
    if isinstance(circle_1, Ball) and isinstance(circle_2, Post):
        circle_1.v = np.sqrt(circle_1.v_x**2 + circle_1.v_y**2)
        circle_2.v = 0

    circle_1.alpha = np.arctan2(circle_1.v_y, circle_1.v_x)
    circle_2.alpha = np.arctan2(circle_2.v_y, circle_2.v_x)

    for circle in [circle_1, circle_2]:
        if isinstance(circle, Player) or isinstance(circle, Ball):
            circle.clip_velocity()
            circle.snelius()

    return circle_1, circle_2
