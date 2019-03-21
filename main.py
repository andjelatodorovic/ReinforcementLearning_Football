from functions import *
import numpy as np
import Arsenal
import Brighton
import United
import City
import time
import random

def render(screen, team_1, team_2, ball, posts, team_1_score, team_2_score, time_to_play, start, half, countdown,
           team_1_name, team_2_name, team_1_color, team_2_color):

    pygame.draw.rect(screen, white, resolution_rect)
    pygame.draw.rect(screen, grass, ground_rect)
    pygame.draw.rect(screen, black, resolution_rect, 2)
    pygame.draw.rect(screen, black, ground_rect, 2)
    pygame.draw.rect(screen, white, playground_rect, 2)
    pygame.draw.rect(screen, white, half_playground_rect, 2)
    pygame.draw.circle(screen, white, center, 100, 2)
    pygame.draw.circle(screen, white, center, 5)

    if half == 1:
        team_left_logo = logos[team_1_name]
        team_right_logo = logos[team_2_name]
        team_left_color = team_1_color
        team_right_color = team_2_color
    else:
        team_left_logo = logos[team_2_name]
        team_right_logo = logos[team_1_name]
        team_left_color = team_2_color
        team_right_color = team_1_color

    screen.blit(team_left_logo, team_left_logo_position)
    screen.blit(team_right_logo, team_right_logo_position)

    pygame.draw.rect(screen, team_left_color, team_left_color_position)
    pygame.draw.rect(screen, team_right_color, team_right_color_position)

    for player in team_1:
        player.draw(screen, team_1_color)
    for player in team_2:
        player.draw(screen, team_2_color)
    ball.draw(screen)
    for post in posts:
        post.draw(screen)

    if countdown:
        myfont = pygame.font.SysFont("monospace", 750)
        short_pause_countdown = "{}".format(short_pause_countdown_time - int(time.time() - start))
        label = myfont.render(short_pause_countdown, 1, (0, 0, 0))
        screen.blit(label, (460, 85))

        myfont = pygame.font.SysFont("monospace", 120)
        message = "{} сек.".format(time_to_play)
        label = myfont.render(message, 1, (0, 0, 0))
        screen.blit(label, (750, 0))
    else:
        myfont = pygame.font.SysFont("monospace", 120)
        time_screen_value = time_to_play - int(time.time() - start)
        if time_screen_value < 0:
            time_screen_value = 0
        message = "{} сек.".format(time_screen_value)
        label = myfont.render(message, 1, (0, 0, 0))
        screen.blit(label, (750, 0))


    myfont = pygame.font.SysFont("monospace", 70)
    if half == 1:
        message = "прво полувреме"
    else:
        message = "второ полувреме"

    label = myfont.render(message, 1, (0, 0, 0))
    screen.blit(label, (730, 85))


    myfont = pygame.font.SysFont("monospace", 150)
    if half == 1:
        message = "{}:{}".format(team_1_score, team_2_score)
    else:
        message = "{}:{}".format(team_2_score, team_1_score)

    label = myfont.render(message, 1, (0, 0, 0))
    screen.blit(label, (215, 0))

    pygame.display.flip()
    pygame.time.Clock().tick(fps)


def play(screen, team_1, team_2, ball, posts, time_to_play, team_1_score, team_2_score, half, team_1_name, team_2_name,
         team_1_color, team_2_color, team_1_script, team_2_script):

    start = time.time()
    while time.time() - start < 3:
        render(screen, team_1, team_2, ball, posts, team_1_score, team_2_score, time_to_play, start, half, True,
               team_1_name, team_2_name, team_1_color, team_2_color)

    start = time.time()
    velocity_step = 10000
    angle_step = 0.1
    angle_change = 0
    velocity_change = 0

    circles = [team_1[0], team_1[1], team_1[2], team_2[0], team_2[1], team_2[2], ball, posts[0], posts[1], posts[2],
               posts[3]]
    goal = False
    game_exit = False
    manager_1_last_decision = {}
    manager_2_last_decision = {}
    while not game_exit:
        if time.time() - start >= time_to_play:
            if ball.v <= 50:
                return False, 0, team_1_score, team_2_score

            if ball.x <= center[0] and np.cos(ball.alpha) >= 0:
                return False, 0, team_1_score, team_2_score

            if ball.x >= center[0] and np.cos(ball.alpha) <= 0:
                return False, 0, team_1_score, team_2_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    angle_change = -angle_step
                if event.key == pygame.K_RIGHT:
                    angle_change = angle_step
                if event.key == pygame.K_UP:
                    velocity_change = velocity_step
                if event.key == pygame.K_DOWN:
                    velocity_change = -velocity_step
                if event.key == pygame.K_ESCAPE:
                    game_exit = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    angle_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    angle_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    velocity_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    velocity_change = 0

        if not goal:
            try:
                manager_1_decision = team_1_script.decision(
                    our_team=[team_1[0].data(), team_1[1].data(), team_1[2].data()],
                    their_team=[team_2[0].data(), team_2[1].data(), team_2[2].data()],
                    ball=ball.data(),
                    your_side='left' if half == 1 else 'right',
                    half=half,
                    time_left=time_to_play - int(time.time() - start),
                    our_score=team_1_score,
                    their_score=team_2_score)
            except:
                manager_1_decision = manager_1_last_decision
            manager_1_last_decision = manager_1_decision

            try:
                manager_2_decision = team_2_script.decision(
                    our_team=[team_2[0].data(), team_2[1].data(), team_2[2].data()],
                    their_team=[team_1[0].data(), team_1[1].data(), team_1[2].data()],
                    ball=ball.data(),
                    your_side='right' if half == 1 else 'left',
                    half=half,
                    time_left=time_to_play - int(time.time() - start),
                    our_score=team_2_score,
                    their_score=team_1_score)
            except:
                manager_2_decision = manager_2_last_decision
            manager_2_last_decision = manager_2_decision

        manager_decision = [manager_1_decision[0], manager_1_decision[1], manager_1_decision[2],
                            manager_2_decision[0], manager_2_decision[1], manager_2_decision[2]]

        manager_decision[0]['alpha'] += angle_change
        manager_decision[0]['force'] += velocity_change

        for i, player in enumerate(circles[:6]):
            player.move(manager_decision[i])
        ball.move()

        if not goal:
            goal_team_right = post_screen_top < ball.y < post_screen_bottom and ball.x < post_screen_left
            goal_team_left = post_screen_top < ball.y < post_screen_bottom and ball.x > post_screen_right
            if goal_team_left:
                if half == 1:
                    team_1_score += 1
                else:
                    team_2_score += 1
            if goal_team_right:
                if half == 1:
                    team_2_score += 1
                else:
                    team_1_score += 1
            goal = goal_team_left or goal_team_right
        else:
            return True, time_to_play - int(time.time() - start), team_1_score, team_2_score

        if not goal:
            for i in range(len(circles[:-4])):
                circles[i].snelius()
                for j in range(i + 1, len(circles)):
                    if collision(circles[i], circles[j]):
                        circles[i], circles[j] = resolve_collision(circles[i], circles[j])

        render(screen, team_1, team_2, ball, posts, team_1_score, team_2_score, time_to_play, start, half, False,
               team_1_name, team_2_name, team_1_color, team_2_color)


def game(team_1, team_2, ball, posts, team_1_name, team_2_name, team_1_color, team_2_color, team_1_script,
         team_2_script):
    pygame.init()
    screen = pygame.display.set_mode(resolution, pygame.FULLSCREEN)
    pygame.display.set_caption(game_name)
    team_1_score, team_2_score = 0, 0

    pygame.mixer.init(22050, -16, 2, 2048)
    crowd = pygame.mixer.music.load('football_crowd.ogg')
    pygame.mixer.music.play(10, 14)

    time_to_play = half_time_duration
    while time_to_play:
        for i, player in enumerate(team_1):
            player.reset(initial_positions_team_left[i], 0)
        for i, player in enumerate(team_2):
                player.reset(initial_positions_team_right[i], np.pi)
        ball.reset()
        goal, time_to_play, team_1_score, team_2_score = \
            play(screen, team_1, team_2, ball, posts, time_to_play, team_1_score, team_2_score, 1, team_1_name,
                 team_2_name, team_1_color, team_2_color, team_1_script, team_2_script)
        qqq()

    time_to_play = half_time_duration
    while time_to_play:
        for i, player in enumerate(team_2):
            player.reset(initial_positions_team_left[i], 0)
        for i, player in enumerate(team_1):
                player.reset(initial_positions_team_right[i], np.pi)
        ball.reset()
        goal, time_to_play, team_1_score, team_2_score = \
            play(screen, team_1, team_2, ball, posts, time_to_play, team_1_score, team_2_score, 2, team_1_name,
                 team_2_name, team_1_color, team_2_color, team_1_script, team_2_script)
        qqq()

    print (team_1_name, team_2_name, team_1_score, team_2_score)

    time.sleep(6)
    pygame.quit()


def qqq():
    global initial_positions_team_left, initial_positions_team_right
    rrr = random.randint(0, 10)
    player_1_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - rrr, post_screen_top]
    player_2_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - rrr, center[1]]
    player_3_initial_position = [int((center[0] - playground[0]) / 2) + playground[0] - rrr, post_screen_bottom]
    player_4_initial_position = [player_1_initial_position[0] + half_playground_rect[2] + rrr, post_screen_top]
    player_5_initial_position = [player_2_initial_position[0] + half_playground_rect[2] + rrr, center[1]]
    player_6_initial_position = [player_3_initial_position[0] + half_playground_rect[2] + rrr, post_screen_bottom]

    initial_positions_team_left = [player_1_initial_position, player_2_initial_position, player_3_initial_position]
    initial_positions_team_right = [player_4_initial_position, player_5_initial_position, player_6_initial_position]


if __name__ == "__main__":
    brighton = [Player(414), Player(196), Player(500)]
    arsenal = [Player(2), Player(90), Player(113)]
    united = [Player(102), Player(74), Player(18)]
    city = [Player(72), Player(47), Player(71)]
    the_ball = Ball(420, 250, 15, 0.5)
    the_posts = [Post(post_screen_left, post_screen_top, post_radius, post_mass),
                 Post(post_screen_left, post_screen_bottom, post_radius, post_mass),
                 Post(post_screen_right, post_screen_top, post_radius, post_mass),
                 Post(post_screen_right, post_screen_bottom, post_radius, post_mass)]

    # terrain = pygame.image.load('ground.png')
    arsenal_logo = pygame.image.load('arsenal_logo.png')
    brighton_logo = pygame.image.load('brighton_logo.png')
    united_logo = pygame.image.load('united_logo.png')
    city_logo = pygame.image.load('city_logo.png')
    logos = {'arsenal': arsenal_logo, 'brighton': brighton_logo, 'united': united_logo, 'city': city_logo}

    game(brighton, arsenal, the_ball, the_posts, 'brighton', 'arsenal', brighton_home, arsenal_home, Brighton, Arsenal)
    game(united, city, the_ball, the_posts, 'united', 'city', united_home, city_home, United, City)
    game(city, brighton, the_ball, the_posts, 'city', 'brighton', city_home, brighton_home, City, Brighton)
    game(arsenal, united, the_ball, the_posts, 'arsenal', 'united', arsenal_home, united_away, Arsenal, United)
    game(united, brighton, the_ball, the_posts, 'united', 'brighton', united_home, brighton_home, United, Brighton)
    game(city, united, the_ball, the_posts, 'city', 'united', city_home, united_home, City, United)
    game(arsenal, brighton, the_ball, the_posts, 'arsenal', 'brighton', arsenal_home, brighton_home, Arsenal, Brighton)
    game(city, arsenal, the_ball, the_posts, 'city', 'arsenal', city_home, arsenal_home, City, Arsenal)
    game(brighton, city, the_ball, the_posts, 'brighton', 'city', brighton_home, city_home, Brighton, City)
    game(united, arsenal, the_ball, the_posts, 'united', 'arsenal', united_home, arsenal_away, United, Arsenal)
    game(brighton, united, the_ball, the_posts, 'brighton', 'united', brighton_home, united_home, Brighton, United)
    game(arsenal, city, the_ball, the_posts, 'arsenal', 'city', arsenal_home, city_home, Arsenal, City)
