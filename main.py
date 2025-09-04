import arcade
import websockets
import asyncio
import json
import uuid
import threading

WIDTH, HEIGHT = 800, 600
x = WIDTH // 2
y = HEIGHT // 2
user_id = str(uuid.uuid4())

GRAVITY = 1.5
GROUND_RESISTANCE = 0.98
BOUNCE_DAMPING = 0.90
WALL_DAMPING = 0.90
CEILING_DAMPING = 0.90

other_positions = {}  # userId -> {"x": ..., "y": ...}


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, "Multiplayer Balls")
        self.vx = 0
        self.vy = 0
        self.radius = 20
        self.xchange = 1.5
        self.ychange = 2.0
        self.held_keys = set()

    def on_draw(self):
        self.clear()
        arcade.draw_circle_filled(x, y, self.radius, arcade.color.AQUA)
        for uid, pos in other_positions.items():
            if uid != user_id:
                arcade.draw_circle_filled(pos["x"], pos["y"], self.radius, arcade.color.RED)

    def on_update(self, delta_time):
        global x, y
        if arcade.key.LEFT in self.held_keys or arcade.key.A in self.held_keys:
            self.vx += self.xchange
        if arcade.key.RIGHT in self.held_keys or arcade.key.D in self.held_keys:
            self.vx -= self.xchange
        if arcade.key.UP in self.held_keys or arcade.key.W in self.held_keys:
            self.vy -= self.ychange
        if arcade.key.DOWN in self.held_keys or arcade.key.S in self.held_keys:
            self.vy += self.ychange

        self.vy += GRAVITY
        y -= self.vy
        x -= self.vx

        # Boundaries
        if y - self.radius <= 0:
            y = self.radius
            self.vx *= GROUND_RESISTANCE
            self.vy *= -BOUNCE_DAMPING
        if y + self.radius >= HEIGHT:
            y = HEIGHT - self.radius
            self.vy *= -CEILING_DAMPING
        if x - self.radius <= 0:
            x = self.radius
            self.vx *= -WALL_DAMPING
        if x + self.radius >= WIDTH:
            x = WIDTH - self.radius
            self.vx *= -WALL_DAMPING

    def on_key_press(self, symbol, modifiers):
        self.held_keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        self.held_keys.remove(symbol)


async def websocket_loop():
    global x, y
    uri = "ws://localhost:8765"
    try:
        async with websockets.connect(uri) as ws:
            print(f"[CLIENT {user_id}] Connected")

            async def send_loop():
                while True:
                    await ws.send(json.dumps({"userId": user_id, "x": x, "y": y}))
                    await asyncio.sleep(0.03)

            async def recv_loop():
                while True:
                    msg = await ws.recv()
                    positions = json.loads(msg)
                    other_positions.clear()
                    other_positions.update(positions)

            await asyncio.gather(send_loop(), recv_loop())

    except Exception as e:
        print(f"[CLIENT {user_id}] Connection failed: {e}")


def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_loop())


if __name__ == "__main__":
    threading.Thread(target=start_async_loop, daemon=True).start()
    window = MyWindow()
    arcade.run()
