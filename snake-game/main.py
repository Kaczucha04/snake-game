import tkinter as tk
from tkinter import messagebox
import random

class Snake(tk.Canvas):
    def __init__(self):
        super().__init__(width=600, height=620, background="black", highlightthickness=0)

        self.snake_pos = [(100, 100), (80, 100), (60, 100)]
        self.food_pos = self.set_new_food_position()
        self.direction = 'Right'
        
        self.score = 0
        self.game_over_flag = False

        self.load_assets()
        self.create_objects()

        self.pack()

        self.bind_all("<Key>", self.on_key_press)
        self.after(100, self.perform_actions)

    def load_assets(self):
        self.snake_body_image = '■'
        self.food_image = '☼'

    def create_objects(self):
        self.create_text(
            100, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10
        )
        for x_position, y_position in self.snake_pos:
            self.create_text(
                x_position, y_position, text=self.snake_body_image, tag="snake", fill="white", font=("Helvetica", 20)
            )
        self.create_text(
            *self.food_pos, text=self.food_image, tag="food", fill="#ff0", font=("Helvetica", 20)
        )

    def set_new_food_position(self):
        while True:
            x_position = random.randint(1, 29)*20
            y_position = random.randint(3, 30)*20
            food_position = (x_position, y_position)

            if food_position not in self.snake_pos:
                return food_position

    def on_key_press(self, e):
        if self.game_over_flag:
            return
        
        new_direction = e.keysym

        all_directions = ['Up', 'Down', 'Left', 'Right']
        opposites = [['Up', 'Down'], ['Left', 'Right']]

        if (
            new_direction in all_directions and
            new_direction != self.direction and
            [new_direction, self.direction] not in opposites
        ):
            self.direction = new_direction

    def perform_actions(self):
        if self.game_over_flag:
            return

        if self.check_collisions():
            self.game_over()
            return

        self.check_food_collision()
        self.move_snake()
        self.after(100, self.perform_actions)

    def check_collisions(self):
        head_x_position, head_y_position = self.snake_pos[0]

        return (
            head_x_position in (0, 600)
            or head_y_position in (20, 620)
            or (head_x_position, head_y_position) in self.snake_pos[1:]
        )

    def check_food_collision(self):
        if self.snake_pos[0] == self.food_pos:
            self.score += 1
            self.snake_pos.append(self.snake_pos[-1])

            self.create_text(
                *self.snake_pos[-1], text=self.snake_body_image, tag="snake", fill="white", font=("Helvetica", 20)
            )

            self.delete("food")

            self.food_pos = self.set_new_food_position()
            self.create_text(
                *self.food_pos, text=self.food_image, tag="food", fill="#ff0", font=("Helvetica", 20)
            )

            self.delete("score")
            self.create_text(
                100, 12, text=f"Score: {self.score}", tag="score", fill="#fff", font=10
            )

    def move_snake(self):
        head_x_position, head_y_position = self.snake_pos[0]

        if self.direction == "Left":
            new_head_position = (head_x_position - 20, head_y_position)
        elif self.direction == "Right":
            new_head_position = (head_x_position + 20, head_y_position)
        elif self.direction == "Up":
            new_head_position = (head_x_position, head_y_position - 20)
        else:
            new_head_position = (head_x_position, head_y_position + 20)

        self.snake_pos = [new_head_position] + self.snake_pos[:-1]

        for segment, position in zip(self.find_withtag("snake"), self.snake_pos):
            self.coords(segment, position)

    def game_over(self):
        self.game_over_flag = True
        messagebox.showinfo("Game Over", f"You scored {self.score}!")

        self.restart_game()

    def restart_game(self):
        self.game_over_flag = False
        self.score = 0
        self.snake_pos = [(100, 100), (80, 100), (60, 100)]
        self.food_pos = self.set_new_food_position()
        self.direction = 'Right'

        self.delete(tk.ALL)
        self.create_objects()

        self.perform_actions()

root = tk.Tk()
root.title("Snake")
root.resizable(False, False)

board = Snake()

root.mainloop()
