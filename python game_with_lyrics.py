import pygame, sys, random

def play_lyrics():
    import tkinter as tk
    import math, random, time, threading

    lyrics = [
        "If I could, then I would",
        "I'll go wherever you will go",
        "Way up high or down low",
        "I'll go wherever you will go"
    ]
    typing_speeds = [0.11, 0.11, 0.13, 0.12]
    line_pauses = [1.3, 1.3, 1.3, 1.3]

    letters = []
    frame = 0
    normal_size = 28
    big_size = 38
    shrink_speed = 0.4

    window_width = 900
    window_height = 500
    star_count = 150
    north_star_count = 7
    stars = []
    north_stars = []

    root = tk.Tk()
    root.title("Whenever You Will Go")
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    canvas = tk.Canvas(root, width=window_width, height=window_height,
                       bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    canvas.create_text(10, 10, text="@Arjinomoto", anchor="nw",
                       font=("Courier", 12, "italic"), fill="white")

    def rotate_point(cx, cy, x, y, angle):
        s = math.sin(angle)
        c = math.cos(angle)
        x -= cx; y -= cy
        xnew = x * c - y * s
        ynew = x * s + y * c
        return xnew + cx, ynew + cy

    def update_star_shape(star_id, cx, cy, size, angle):
        w = size
        h = size * 0.6
        top = rotate_point(cx, cy, cx, cy - h / 2, angle)
        right = rotate_point(cx, cy, cx + w / 2, cy, angle)
        bottom = rotate_point(cx, cy, cx, cy + h / 2, angle)
        left = rotate_point(cx, cy, cx - w / 2, cy, angle)
        points = [top[0], top[1], right[0], right[1],
                  bottom[0], bottom[1], left[0], left[1]]
        canvas.coords(star_id, *points)

    def create_north_star(cx, cy, size):
        half = size / 2
        v_line = canvas.create_line(cx, cy - half, cx, cy + half, fill="white", width=2)
        h_line = canvas.create_line(cx - half, cy, cx + half, cy, fill="white", width=2)
        return v_line, h_line

    def update_north_star_shape(v_line, h_line, cx, cy, size, angle):
        half = size / 2
        x1, y1 = rotate_point(cx, cy, cx, cy - half, angle)
        x2, y2 = rotate_point(cx, cy, cx, cy + half, angle)
        canvas.coords(v_line, x1, y1, x2, y2)
        x3, y3 = rotate_point(cx, cy, cx - half, cy, angle)
        x4, y4 = rotate_point(cx, cy, cx + half, cy, angle)
        canvas.coords(h_line, x3, y3, x4, y4)

    for _ in range(star_count):
        cx = random.randint(0, window_width)
        cy = random.randint(0, window_height)
        size = random.choice([2, 3, 4])
        angle = random.uniform(0, 2 * math.pi)
        speed_up = random.uniform(0.2, 0.5)
        speed_rot = random.uniform(0.002, 0.008)
        star_id = canvas.create_polygon(0, 0, 0, 0, 0, 0, 0, 0,
                                        fill="white", outline="")
        stars.append([star_id, cx, cy, size, angle, speed_up,
                      speed_rot, random.uniform(0, 2 * math.pi)])

    for _ in range(north_star_count):
        cx = random.randint(20, window_width - 20)
        cy = random.randint(20, window_height - 20)
        size = random.randint(8, 12)
        angle = random.uniform(0, 2 * math.pi)
        speed_up = random.uniform(0.1, 0.3)
        speed_rot = random.uniform(0.005, 0.015)
        v_line, h_line = create_north_star(cx, cy, size)
        north_stars.append([[v_line, h_line], cx, cy, size, angle,
                            speed_up, speed_rot, random.uniform(0, 2 * math.pi)])

    def animate_letters():
        nonlocal frame, letters
        frame += 1
        for i, (item, bx, by, wave_offset, size) in enumerate(letters):
            offset_y = math.sin((frame / 40) + wave_offset) * 3
            offset_x = math.sin((frame / 25) + wave_offset) * 2
            canvas.coords(item, bx + offset_x, by + offset_y)
            if size > normal_size:
                size = max(normal_size, size - shrink_speed)
                canvas.itemconfig(item, font=("Arial", int(size), "bold"))
                letters[i] = (item, bx, by, wave_offset, size)

        for star in stars:
            star_id, cx, cy, size, angle, speed_up, speed_rot, phase = star
            cy -= speed_up; angle += speed_rot
            if cy < -10:
                cy = window_height + 10
                cx = random.randint(0, window_width)
                size = random.choice([2, 3, 4])
                speed_up = random.uniform(0.2, 0.5)
                speed_rot = random.uniform(0.002, 0.008)
            star[1], star[2], star[3], star[4], star[5] = cx, cy, size, angle, speed_up
            update_star_shape(star_id, cx, cy, size, angle)

        for star in north_stars:
            (v_line, h_line), cx, cy, size, angle, speed_up, speed_rot, phase = star
            cy -= speed_up; angle += speed_rot
            if cy < -20:
                cy = window_height + 20
                cx = random.randint(20, window_width - 20)
                size = random.randint(8, 12)
                speed_up = random.uniform(0.1, 0.3)
                speed_rot = random.uniform(0.005, 0.015)
            star[1], star[2], star[3], star[4], star[5] = cx, cy, size, angle, speed_up
            glow = (math.sin(frame / 15 + phase) + 1) / 2
            brightness = int(180 + 75 * glow)
            color = f"#{brightness:02x}{brightness:02x}{brightness:02x}"
            width = 1 + glow * 2
            canvas.itemconfig(v_line, fill=color, width=width)
            canvas.itemconfig(h_line, fill=color, width=width)
            update_north_star_shape(v_line, h_line, cx, cy, size, angle)

        root.after(16, animate_letters)

    def type_line(line, speed):
        nonlocal letters
        for item, *_ in letters:
            canvas.delete(item)
        letters = []
        start_x = window_width // 2 - (len(line) * (normal_size // 2))
        y = window_height // 2
        for i, char in enumerate(line):
            x = start_x + i * (normal_size + 2)
            item = canvas.create_text(x, y, text=char, fill="white",
                                      font=("Arial", big_size, "bold"))
            letters.append((item, x, y, i * 0.3, big_size))
            time.sleep(speed)

    def type_lyrics():
        for i, line in enumerate(lyrics):
            type_line(line, typing_speeds[i])
            time.sleep(line_pauses[i])

    def start_typing():
        threading.Thread(target=type_lyrics, daemon=True).start()

    animate_letters()
    start_typing()
    root.mainloop()

def play_game():
    pygame.init()
    w, h = 500, 700
    screen = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    car = pygame.Rect(w//2 - 20, h - 100, 40, 80)
    road_lines = [pygame.Rect(w//2 - 5, i, 10, 40) for i in range(0, h, 100)]
    pygame.display.set_caption("Car Dodge")
    enemy_cars = []
    speed = 3
    distance = 0
    score = 0
    font = pygame.font.SysFont("Courier", 30, bold=True)
    small_font = pygame.font.SysFont("Courier", 18, italic=True)
    game_over = False
    running = True
    lanes = [80, 160, 240, 320, 400]
    while running:
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (20, 20, 20), (50, 0, 400, h))
        for line in road_lines:
            pygame.draw.rect(screen, (180, 180, 180), line)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and car.left > 60:
                car.x -= 7
            if keys[pygame.K_RIGHT] and car.right < 440:
                car.x += 7
            distance += speed / 10
            score = int(distance)
            speed = 3 + distance / 150
            if random.randint(1, 40) == 1:
                lane = random.choice(lanes)
                enemy_cars.append(pygame.Rect(lane, -100, 40, 80))
            new_enemies = []
            for enemy in enemy_cars:
                enemy.y += speed
                if enemy.y < h:
                    new_enemies.append(enemy)
            enemy_cars = new_enemies
            for enemy in enemy_cars:
                pygame.draw.rect(screen, (150, 150, 0), enemy)
                if enemy.colliderect(car):
                    game_over = True
                    pygame.quit()
                    play_lyrics()
                    return
            pygame.draw.rect(screen, (0, 200, 150), car)
            for line in road_lines:
                line.y += speed
                if line.y > h:
                    line.y = -100
            score_text = font.render(f"SCORE: {score}", True, (255, 255, 0))
            watermark = small_font.render("@Arjinomoto", True, (200, 200, 200))
            screen.blit(score_text, (10, 10))
            screen.blit(watermark, (10, 40))
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    play_game()
