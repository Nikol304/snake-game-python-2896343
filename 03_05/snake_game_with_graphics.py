# Import the Turtle Graphics and random modules
import turtle
import random
import os

# Assets directory (absolute) so running from different cwd/debuggers still works
ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")

# Define program constants
WIDTH = 800
HEIGHT = 600
DELAY = 75  # Milliseconds
FOOD_SIZE = 32
SNAKE_SIZE = 20

offsets = {
    "up": (0, SNAKE_SIZE),
    "down": (0, -SNAKE_SIZE),
    "left": (-SNAKE_SIZE, 0),
    "right": (SNAKE_SIZE, 0)
}

# High score
high_score = 0

# Load the high score if it exists
try:
    with open("high_score.txt", "r") as file:
        high_score = int(file.read())
except FileNotFoundError:
    pass

# Game state
game_running = False
score = 0
snake = []
snake_direction = "up"
food_pos = (0, 0)

# Body colours for snake segments (will repeat)
BODY_COLORS = [
   
    "#009ef1",
    "#ffeb3b",
    "#e91e63",
    "#ff9800",
    "#00c853"
    
]


def update_high_score():
    global high_score

    if score > high_score:
        high_score = score
        with open("high_score.txt", "w") as file:
            file.write(str(high_score))


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up")
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")


def set_snake_direction(direction):
    global snake_direction

    if not game_running:
        return

    if direction == "up":
        if snake_direction != "down":
            snake_direction = "up"
    elif direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
    elif direction == "left":
        if snake_direction != "right":
            snake_direction = "left"
    elif direction == "right":
        if snake_direction != "left":
            snake_direction = "right"


def draw_button(text):
    button.clear()
    button.penup()
    button.goto(-100, -60)
    button.pendown()
    button.fillcolor("#009ef1")
    button.begin_fill()

    for _ in range(2):
        button.forward(200)
        button.left(90)
        button.forward(60)
        button.left(90)

    button.end_fill()
    button.penup()

    button.goto(0, -45)
    button.color("white")
    button.write(text, align="center", font=("Arial", 22, "bold"))

    button.color("black")


def clear_button():
    button.clear()


def show_start_screen():
    global game_running

    game_running = False

    stamper.clearstamps()
    food.hideturtle()
    clear_button()

    message.clear()
    message.goto(0, 80)
    message.write("Snake Game", align="center", font=("Arial", 40, "bold"))

    message.goto(0, 30)
    message.write("Click the button to start", align="center", font=("Arial", 18, "normal"))

    draw_button("START")

    screen.title(f"Snake Game. High Score: {high_score}")
    screen.update()


def show_game_over():
    global game_running

    game_running = False

    update_high_score()

    stamper.clearstamps()
    food.hideturtle()
    clear_button()

    message.clear()
    message.goto(0, 100)
    message.write("GAME OVER", align="center", font=("Arial", 40, "bold"))

    message.goto(0, 50)
    message.write(
        f"Score: {score}   High Score: {high_score}",
        align="center",
        font=("Arial", 20, "normal")
    )

    draw_button("PLAY AGAIN")

    screen.title(f"Game Over. Score: {score} High Score: {high_score}")
    screen.update()


def start_game():
    global game_running, score, snake, snake_direction, food_pos

    game_running = True

    message.clear()
    clear_button()
    stamper.clearstamps()

    score = 0

    snake = [
        [0, 0],
        [SNAKE_SIZE, 0],
        [SNAKE_SIZE * 2, 0],
        [SNAKE_SIZE * 3, 0]
    ]

    snake_direction = "up"

    food_pos = get_random_food_pos()
    food.goto(food_pos)
    food.showturtle()

    game_loop()


def mouse_click(x, y):
    # Button area:
    # x between -100 and 100
    # y between -60 and 0
    if -100 <= x <= 100 and -60 <= y <= 0:
        if not game_running:
            start_game()


def game_loop():
    global game_running

    if not game_running:
        return

    stamper.clearstamps()

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check collisions
    if (
        new_head in snake
        or new_head[0] < -WIDTH / 2
        or new_head[0] > WIDTH / 2
        or new_head[1] < -HEIGHT / 2
        or new_head[1] > HEIGHT / 2
    ):
        show_game_over()
        return

    # Add new head to snake body
    snake.append(new_head)

    # Check food collision
    if not food_collision():
        snake.pop(0)

    # Draw snake head
    stamper.shape(os.path.join(ASSETS_DIR, "snake-head-20x20.gif"))
    stamper.goto(snake[-1][0], snake[-1][1])
    stamper.stamp()

    # Draw snake body with changing colours
    stamper.shape("circle")

    for index, segment in enumerate(snake[:-1]):
        color = BODY_COLORS[index % len(BODY_COLORS)]

        stamper.color(color)
        stamper.goto(segment[0], segment[1])
        stamper.stamp()

    # Refresh screen
    screen.title(f"Snake Game. Score: {score} High Score: {high_score}")
    screen.update()

    # Repeat game loop
    turtle.ontimer(game_loop, DELAY)


def food_collision():
    global food_pos, score

    if get_distance(snake[-1], food_pos) < 20:
        score += 1
        update_high_score()

        food_pos = get_random_food_pos()
        food.goto(food_pos)

        return True

    return False


def get_random_food_pos():
    x = random.randint(
        int(-WIDTH / 2 + FOOD_SIZE),
        int(WIDTH / 2 - FOOD_SIZE)
    )

    y = random.randint(
        int(-HEIGHT / 2 + FOOD_SIZE),
        int(HEIGHT / 2 - FOOD_SIZE)
    )

    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2

    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance


# Create a window where we will do our drawing
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake")
screen.bgpic(os.path.join(ASSETS_DIR, "bg2.gif"))
screen.register_shape(os.path.join(ASSETS_DIR, "snake-food-32x32.gif"))
screen.register_shape(os.path.join(ASSETS_DIR, "snake-head-20x20.gif"))

screen.tracer(0)

# Event handlers
screen.listen()
bind_direction_keys()
screen.onclick(mouse_click)

# Turtle for drawing the snake
stamper = turtle.Turtle()
stamper.shape("circle")
stamper.color("#009ef1")
stamper.penup()
stamper.hideturtle()

# Food
food = turtle.Turtle()
food.shape(os.path.join(ASSETS_DIR, "snake-food-32x32.gif"))
food.shapesize(FOOD_SIZE / 20)
food.penup()
food.hideturtle()

# Message turtle
message = turtle.Turtle()
message.hideturtle()
message.penup()
message.color("black")

# Button turtle
button = turtle.Turtle()
button.hideturtle()
button.speed(0)

# Show start screen first and run; wrap in try/except to surface errors in debuggers
try:
    show_start_screen()
    # Finish nicely
    turtle.done()
except Exception:
    # Print full traceback to the console (useful when running under a debugger)
    import traceback, sys

    traceback.print_exc()
    # Re-raise so the process exit code remains non-zero for the debugger
    raise
