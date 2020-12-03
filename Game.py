 #!/usr/bin/python
import tkinter as tk
import random
import CONS

class Snake():
    def __init__(self):
        self.body = []
        self.on_crack = False
        self.length = 1
        self.speed = self.snake_on_crack(self.on_crack)
        self.color = CONS.COL_SNAKE_1
        self.outline = CONS.COL_SNAKE_2
        self.x = CONS.GRID_WIDTH / 2
        self.y = CONS.GRID_HEIGHT / 2
        self.x_new = 0
        self.y_new = 0
        
        # TODO: self.dir = (whatever direction was last pressed)
        # self.prev_dir

    def snake_on_crack(self, bool):
        if self.on_crack == True:
            return 96
        else:
            return 10

    def add_length(self):
        self.length += 1

    def add_speed(self):
        if self.speed < CONS.MAX_SPEED:
            self.speed += 2
        else:
            pass

    def eat(self, food):
        self.add_speed()
        self.add_length()
        food.respawn()
    

class Food():
    def __init__(self):
        self.color = self.random_color()
        self.x = self.get_rand_loc(CONS.GRID_WIDTH, CONS.CELL_WIDTH)
        self.y = self.get_rand_loc(CONS.GRID_HEIGHT, CONS.CELL_HEIGHT)

    def random_color(self):
        color = "#" + "%06x" % random.randint(0, 0xFFFFFF)
        return color

    def respawn(self):
        self.color = self.random_color()
        self.x = self.get_rand_loc(CONS.GRID_WIDTH, CONS.CELL_WIDTH)
        self.y = self.get_rand_loc(CONS.GRID_HEIGHT, CONS.CELL_HEIGHT)

    def get_rand_loc(self, m, u):
        return random.randrange(0, m, u)
       
class Game(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.snake = Snake()
        self.snake2 = Snake()
        self.won = False
        self.lost = False
        self.last_pressed = ""
        self.previous_last_pressed = ""
        self.width = CONS.GRID_WIDTH / 2
        self.height = CONS.GRID_HEIGHT / 2
        self.food = Food()
        self.score = self.snake.length - 1;

        self.focus_set()
        self.configure(bg=CONS.COL_BG)
        self.title("Amar's Snake")

        # Keypress event binding
        self.bind('<KeyPress-w>', self.on_press)
        self.bind('<KeyPress-s>', self.on_press)
        self.bind('<KeyPress-a>', self.on_press)
        self.bind('<KeyPress-d>', self.on_press)

        self.bind('<Up>', self.on_press)
        self.bind('<Down>', self.on_press)
        self.bind('<Left>', self.on_press)
        self.bind('<Right>', self.on_press)
        
        self.bind('<Escape>', self.stop_game)

        self.geometry(CONS.WINDOW_SIZE)

        self.can = tk.Canvas(self, width=CONS.GRID_WIDTH, height=CONS.GRID_HEIGHT, bg=CONS.COL_BG)
        self.can.pack()

        self.game_loop()

    def restart(self):
        pass

    def stop_game(self, event):
        exit()
    
    def draw(self, canvas, snake_list, food_list, score):
        canvas.create_rectangle(self.food.x, self.food.y, self.food.x + CONS.CELL_WIDTH, self.food.y + CONS.CELL_HEIGHT, fill=self.food.color)
        for i in snake_list:
            canvas.create_rectangle(i[0], i[1], i[0] + CONS.CELL_WIDTH, i[1] + CONS.CELL_HEIGHT, fill=self.snake.color, outline=self.snake.outline)

    def check_collision(self):

        # Prevent snake from going 180 degrees by checking which last 2 directions the snake was going in
        # Might get removed when actual collision detection is implemented
        illegal_moves = [["up", "down"], ["left", "right"],["down", "up"], ["right", "left"]]
        for i in illegal_moves:
            if self.last_pressed == i[0] and self.previous_last_pressed == i[1] and self.snake.length > 1:
                #self.lost = True
                pass

        # If snake goes out of frame, snake comes back form the other side
        # Needs improvement, otherwise snake sticks out of frame
        if self.snake.x >= CONS.GRID_WIDTH:
            self.snake.x = 0 - CONS.CELL_WIDTH
        elif self.snake.x < 0:
            self.snake.x = CONS.GRID_WIDTH
        elif self.snake.y >= CONS.GRID_HEIGHT:
            self.snake.y = 0 - CONS.CELL_HEIGHT
        elif self.snake.y < 0:
            self.snake.y = CONS.GRID_HEIGHT

        # Collision detection
        for i in self.snake.body:
            if self.snake.body[len(self.snake.body)-1][0] == self.food.x and self.snake.body[len(self.snake.body)-1][1] == self.food.y:
                self.snake.eat(self.food)

            if self.snake.body[len(self.snake.body)-1] in self.snake.body[0:len(self.snake.body)-2]:
                self.lost = True
    def check_lose(self):
        if self.lost == True:
            self.destroy()
            new_game = Game()
            new_game.mainloop()

    # Move snake in different direction depending on the last pressed key
    def move(self, last_pressed, posx, posy):
        if last_pressed == "up":
            self.snake.x_new = 0
            self.snake.y_new = -1 * CONS.CELL_WIDTH
        elif last_pressed == "down":
            self.snake.x_new = 0
            self.snake.y_new = CONS.CELL_HEIGHT
        elif last_pressed == "left":
            self.snake.x_new = -1 * CONS.CELL_WIDTH
            self.snake.y_new = 0
        elif last_pressed == "right":
            self.snake.x_new = CONS.CELL_WIDTH
            self.snake.y_new = 0
        self.snake.x += self.snake.x_new
        self.snake.y += self.snake.y_new
        self.snake.x_new = 0
        self.snake.y_new = 0
        snake_head = []
        snake_head.append(self.snake.x)
        snake_head.append(self.snake.y)
        self.snake.body.append(snake_head)

        if len(self.snake.body) > self.snake.length:
            del self.snake.body[0]

    # Catch keypress events
    # TODO: Change self.last_pressed -> self.snake.prev_dir and etc.
    def on_press(self, event):
        key = event.char
        self.previous_last_pressed = self.last_pressed
        if key == "w" or key == "up":
            self.last_pressed = "up"
        elif key == "s" or key == "down":
            self.last_pressed = "down"
        elif key == "a" or key == "left":
            self.last_pressed = "left"
        elif key == "d" or key == "right":
            self.last_pressed = "right"

    # Game loop
    def game_loop(self):
        self.check_collision()
        self.check_lose()
        self.move(self.last_pressed, self.snake.x, self.snake.y)
        self.can.delete("all")
        self.draw(self.can, self.snake.body, self.food, self.score)
        self.after(100 - self.snake.speed, self.game_loop)

if __name__ == "__main__":
    game = Game()
    game.mainloop()
