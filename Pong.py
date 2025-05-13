import turtle
import random
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 100
BALL_SIZE = 20
BALL_SPEED = 4.5  # Increased ball speed for a faster game
COMPUTER_SPEED = 4  # Increased computer speed for more thrill

# Game state
player_score = 0
computer_score = 0
player_lives = 3
game_over = False

# Initialize the screen and objects
def initialize_game():
    global wn, pen, paddle_a, paddle_b, ball

    # Create the game window
    wn = turtle.Screen()
    wn.title("Pong Game")
    wn.bgcolor("black")
    wn.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    wn.tracer(0)  # Stops auto updates for better control over screen refresh

    # Create score display
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("white")
    pen.penup()
    pen.hideturtle()
    pen.goto(0, SCREEN_HEIGHT // 2 - 50)
    update_scoreboard()

    # Create player paddle (left side)
    paddle_a = turtle.Turtle()
    paddle_a.speed(0)
    paddle_a.shape("square")
    paddle_a.color("white")
    paddle_a.shapesize(stretch_wid=PADDLE_HEIGHT / 20, stretch_len=PADDLE_WIDTH / 20)
    paddle_a.penup()
    paddle_a.goto(-SCREEN_WIDTH // 2 + PADDLE_WIDTH, 0)

    # Create computer paddle (right side)
    paddle_b = turtle.Turtle()
    paddle_b.speed(0)
    paddle_b.shape("square")
    paddle_b.color("white")
    paddle_b.shapesize(stretch_wid=PADDLE_HEIGHT / 20, stretch_len=PADDLE_WIDTH / 20)
    paddle_b.penup()
    paddle_b.goto(SCREEN_WIDTH // 2 - PADDLE_WIDTH, 0)

    # Create ball
    ball = turtle.Turtle()
    ball.speed(1)
    ball.shape("circle")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = BALL_SPEED * random.choice([-1, 1])  # Random initial direction for x
    ball.dy = BALL_SPEED * random.choice([-1, 1])  # Random initial direction for y

# Update the scoreboard with current score and lives
def update_scoreboard():
    pen.clear()
    pen.write(f"Player: {player_score}  Computer: {computer_score}  Lives: {player_lives}", 
              align="center", font=("Courier", 24, "normal"))

# Move the player paddle up
def paddle_a_up():
    if paddle_a.ycor() < SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2:
        paddle_a.sety(paddle_a.ycor() + 40)

# Move the player paddle down
def paddle_a_down():
    if paddle_a.ycor() > -SCREEN_HEIGHT // 2 + PADDLE_HEIGHT // 2:
        paddle_a.sety(paddle_a.ycor() - 40)

# Game over screen
def game_over_screen():
    global game_over
    pen.clear()
    pen.hideturtle()
    paddle_a.hideturtle()
    paddle_b.hideturtle()
    ball.hideturtle()

    game_over_pen = turtle.Turtle()  # Create a separate turtle for the game-over message
    game_over_pen.hideturtle()       # Hide the turtle shape
    game_over_pen.penup()            # Make sure it doesn't draw any line
    game_over_pen.color("black")
    pen.goto(0, 0)
    pen.write(f"GAME OVER! Final Score: Player - {player_score} v/s Computer - {computer_score}", 
              align="center", font=("Courier", 18, "normal"))
    game_over = True
    wn.update()  
    time.sleep(8)  
    wn.bye()  # Close the game window after the delay

# Game loop
def game_loop():
    global game_over, player_score, computer_score, player_lives, ball

    while not game_over:
        wn.update()

        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Ball collision with top and bottom borders
        if ball.ycor() >= SCREEN_HEIGHT // 2 - BALL_SIZE:
            ball.sety(SCREEN_HEIGHT // 2 - BALL_SIZE)
            ball.dy *= -1

        if ball.ycor() <= -SCREEN_HEIGHT // 2 + BALL_SIZE:
            ball.sety(-SCREEN_HEIGHT // 2 + BALL_SIZE)
            ball.dy *= -1

        # Ball collision with player paddle (left)
        if (ball.xcor() < -SCREEN_WIDTH // 2 + PADDLE_WIDTH + BALL_SIZE) and \
           (paddle_a.ycor() - PADDLE_HEIGHT // 2 < ball.ycor() < paddle_a.ycor() + PADDLE_HEIGHT // 2):
            ball.setx(-SCREEN_WIDTH // 2 + PADDLE_WIDTH + BALL_SIZE)
            ball.dx *= -1

        # Ball collision with computer paddle (right)
        if (ball.xcor() > SCREEN_WIDTH // 2 - PADDLE_WIDTH - BALL_SIZE) and \
           (paddle_b.ycor() - PADDLE_HEIGHT // 2 < ball.ycor() < paddle_b.ycor() + PADDLE_HEIGHT // 2):
            ball.setx(SCREEN_WIDTH // 2 - PADDLE_WIDTH - BALL_SIZE)
            ball.dx *= -1

        # Scoring: Ball goes off the left side (Computer scores)
        if ball.xcor() < -SCREEN_WIDTH // 2:
            computer_score += 1
            player_lives -= 1
            reset_ball()
            update_scoreboard()

            # End game if player loses all lives
            if player_lives == 0:
                game_over_screen()
                return  # Exit the game loop to prevent further execution

        # Scoring: Ball goes off the right side (Player scores)
        if ball.xcor() > SCREEN_WIDTH // 2:
            player_score += 1
            reset_ball()
            update_scoreboard()

        # Move the computer paddle to track the ball (increased speed)
        if paddle_b.ycor() < ball.ycor() - 10:
            paddle_b.sety(paddle_b.ycor() + COMPUTER_SPEED)
        elif paddle_b.ycor() > ball.ycor() + 10:
            paddle_b.sety(paddle_b.ycor() - COMPUTER_SPEED)

        # Control the game frame rate (decrease time.sleep for faster speed)
        time.sleep(0.005)  # Reduced sleep time to increase game speed

# Reset the ball to the center and randomly choose a new direction
def reset_ball():
    ball.goto(0, 0)
    ball.dx = BALL_SPEED * random.choice([-1, 1])
    ball.dy = BALL_SPEED * random.choice([-1, 1])

# Main function
def main():
    initialize_game()

    # Keyboard bindings for player paddle
    wn.listen()
    wn.onkeypress(paddle_a_up, "Up")
    wn.onkeypress(paddle_a_down, "Down")

    game_loop()

if __name__ == "__main__":
    main()
