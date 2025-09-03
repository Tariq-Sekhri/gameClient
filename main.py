# main.py
import arcade

WIDTH, HEIGHT = 800, 600

class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Circle")
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.radius = 40
        self.step = 10
        self.gravity = 0.4

    def on_draw(self):
        self.clear()
        self.vy+=self.gravity
        self.y -= self.vy
        self.x -= self.vx
        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.AQUA)

    def on_key_press(self, symbol, modifiers):
        if symbol in (arcade.key.LEFT, arcade.key.A):
            self.vx -= self.step
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.vx += self.step
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.vy += self.step
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.vy -= self.step


if __name__ == "__main__":
    MyWindow()
    arcade.run()
