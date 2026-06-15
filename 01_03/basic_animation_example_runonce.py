# Small wrapper of basic animation that runs for a fixed number of steps and exits.
import turtle

# Define program constants
WIDTH = 500
HEIGHT = 500
DELAY = 20
STEPS = 300

print('Starting run-once animation')

step_count = 0

def move_turtle():
    global step_count
    my_turtle.forward(1)
    my_turtle.right(1)
    screen.update()
    step_count += 1
    if step_count >= STEPS:
        print('Reached step limit, closing window')
        turtle.bye()  # Close the turtle window and end the program
    else:
        screen.ontimer(move_turtle, DELAY)

# Create a window where we will do our drawing.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Program Title - runonce")
screen.bgcolor("cyan")
screen.tracer(0)

# Create a turtle to do your bidding
my_turtle = turtle.Turtle()
my_turtle.shape("turtle")
my_turtle.color("red")

# Start animation
move_turtle()

# This will keep the program alive until turtle.bye() is called
try:
    turtle.mainloop()
except Exception:
    pass

print('Program finished')
