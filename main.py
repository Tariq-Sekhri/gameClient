# main.py
import arcade

WIDTH, HEIGHT = 1920, 1080

class MyWindow(arcade.Window):

    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Arcade Circle")
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.vx = 0
        self.vy = 0
        self.radius = 40
        self.xchange = 6
        self.ychange = 6
        self.gravity = 0.4


    def on_draw(self):
        self.clear()
        self.vy+=self.gravity
        self.y -= self.vy
        self.x -= self.vx
        if(self.y-self.radius<= 7):
            self.vy*=-0.90
        if(self.y-self.radius<= 0):
            self.y =0+self.radius
            self.vx*=0.99

        if self.x - self.radius <= 7:
            self.vx *= -0.90
        if self.x - self.radius <= 0:
            self.x = 0 + self.radius

        # Right wall
        if self.x + self.radius >= WIDTH - 7:
            self.vx *= -0.90
        if self.x + self.radius >= WIDTH:
            self.x = WIDTH - self.radius

        arcade.draw_circle_filled(self.x, self.y, self.radius, arcade.color.AQUA)

    def on_key_press(self, symbol, modifiers):
        if symbol in (arcade.key.LEFT, arcade.key.A):
            self.vx += self.xchange
        elif symbol in (arcade.key.RIGHT, arcade.key.D):
            self.vx -= self.xchange
        elif symbol in (arcade.key.UP, arcade.key.W):
            self.vy -= self.ychange
        elif symbol in (arcade.key.DOWN, arcade.key.S):
            self.vy += self.ychange


if __name__ == "__main__":
    MyWindow()
    arcade.run()
