import random
import sys
import pygame
import os

print(os.getcwd())

pygame.init()

WIDTH, HEIGHT = 980, 620
FPS = 60
ORDER_TIME = 25

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Purple Cake")
CLOCK = pygame.time.Clock()

BG_TOP = (246, 236, 255)
BG_BOTTOM = (222, 203, 245)
PANEL = (255, 250, 255)
TEXT = (70, 52, 90)
ACCENT = (126, 72, 173)
ACCENT_DARK = (93, 52, 128)
GOOD = (57, 162, 97)
BAD = (195, 76, 76)

FONT = pygame.font.Font("/Users/atika1337/Desktop/игра/assets/minecraft.ttf", 16)
FONT_SMALL = pygame.font.Font("/Users/atika1337/Desktop/игра/assets/minecraft.ttf", 16)
FONT_BIG = pygame.font.Font("/Users/atika1337/Desktop/игра/assets/minecraft.ttf", 22)

SHAPES = ["Круг", "Квадрат", "Сердце"]
COLORS = [
    ("Банановый", (250, 235, 100)),
    ("Клубничный", (255, 192, 203)),
    ("Черничный", (200, 180, 235)),
    ("Шоколадный", (152, 104, 74)),
]
DETAILS = ["Вишенка", "Свечки", "Печеньки", "Ягоды", "Посыпка"]
LAYER_CHOICES = [1, 2, 3]


class Button:
    def __init__(self, rect, text, value, group):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.value = value
        self.group = group

    def draw(self, surface, selected=False):
        fill = ACCENT if selected else (240, 232, 247)
        border = ACCENT_DARK if selected else (204, 183, 224)
        pygame.draw.rect(surface, fill, self.rect, border_radius=12)
        pygame.draw.rect(surface, border, self.rect, 2, border_radius=12)
        text_surface = FONT_SMALL.render(self.text, True, (255, 255, 255) if selected else TEXT)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class Order:
    def __init__(self, level):
        self.shape = random.choice(SHAPES)
        self.color_name, self.color_rgb = random.choice(COLORS)
        self.detail = random.choice(DETAILS)
        self.layers = get_required_layers(level)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient_bg(surface):
    for y in range(HEIGHT):
        t = y / HEIGHT
        pygame.draw.line(surface, lerp_color(BG_TOP, BG_BOTTOM, t), (0, y), (WIDTH, y))


def heart_points(rect):
    x, y, w, h = rect
    return [
        (x + w * 0.50, y + h * 0.96),
        (x + w * 0.36, y + h * 0.82),
        (x + w * 0.22, y + h * 0.68),
        (x + w * 0.12, y + h * 0.54),
        (x + w * 0.08, y + h * 0.40),
        (x + w * 0.11, y + h * 0.27),
        (x + w * 0.20, y + h * 0.17),
        (x + w * 0.31, y + h * 0.12),
        (x + w * 0.42, y + h * 0.14),
        (x + w * 0.50, y + h * 0.24),
        (x + w * 0.58, y + h * 0.14),
        (x + w * 0.69, y + h * 0.12),
        (x + w * 0.80, y + h * 0.17),
        (x + w * 0.89, y + h * 0.27),
        (x + w * 0.92, y + h * 0.40),
        (x + w * 0.88, y + h * 0.54),
        (x + w * 0.78, y + h * 0.68),
        (x + w * 0.64, y + h * 0.82),
    ]


def draw_detail(surface, detail, area):
    x, y, w, h = area
    if w <= 6 or h <= 6:
        return

    clip_rect = pygame.Rect(x, y, w, h)
    old_clip = surface.get_clip()
    surface.set_clip(clip_rect)

    rnd = random.Random((x, y, w, h, detail))
    size = min(w, h)

    if detail == "Вишенка":
        radius = max(4, size // 7)
        cx, cy = x + w // 2, y + h // 2
        pygame.draw.circle(surface, (205, 40, 58), (cx, cy), radius)
        pygame.draw.line(surface, (33, 122, 63), (cx, cy - radius), (cx + radius, cy - radius * 2), 2)
    elif detail == "Свечки":
        candle_w = max(4, w // 18)
        candle_h = max(8, h // 3)
        for i in range(3):
            cx = int(x + w * (0.30 + i * 0.20))
            cy = int(y + h * 0.34)
            pygame.draw.rect(surface, (255, 242, 195), (cx, cy, candle_w, candle_h), border_radius=3)
            pygame.draw.circle(surface, (255, 157, 57), (cx + candle_w // 2, cy - 4), max(2, candle_w // 2))
    elif detail == "Печеньки":
        cookie_r = max(4, size // 9)
        points = [
            (0.20, 0.28), (0.50, 0.20), (0.80, 0.30),
            (0.30, 0.50), (0.70, 0.50),
            (0.22, 0.76), (0.78, 0.76),
        ]
        for px, py in points:
            cx = int(x + w * px)
            cy = int(y + h * py)
            pygame.draw.circle(surface, (188, 132, 92), (cx, cy), cookie_r)
            pygame.draw.circle(surface, (129, 84, 55), (cx - cookie_r // 3, cy - cookie_r // 4), max(1, cookie_r // 5))
            pygame.draw.circle(surface, (129, 84, 55), (cx + cookie_r // 4, cy + cookie_r // 3), max(1, cookie_r // 5))
    elif detail == "Ягоды":
        berry_r = max(3, size // 11)
        for _ in range(8):
            bx = rnd.randint(x + berry_r, x + w - berry_r)
            by = rnd.randint(y + berry_r, y + h - berry_r)
            pygame.draw.circle(surface, (72, 84, 188), (bx, by), berry_r)
            pygame.draw.circle(surface, (128, 45, 145), (bx + berry_r // 2, by + berry_r // 2), max(2, berry_r - 1))
    elif detail == "Посыпка":
        sprinkle_colors = [(255, 96, 150), (130, 214, 255), (255, 255, 170), (170, 255, 180)]
        count = max(12, size // 3)
        seg = max(2, size // 26)
        for _ in range(count):
            sx = rnd.randint(x + seg, x + w - seg)
            sy = rnd.randint(y + seg, y + h - seg)
            col = rnd.choice(sprinkle_colors)
            pygame.draw.line(surface, col, (sx - seg, sy - 1), (sx + seg, sy + 1), 2)

    surface.set_clip(old_clip)


def draw_round_tier(surface, color, rect):
    x, y, w, h = rect
    shade = tuple(max(0, c - 30) for c in color)
    side = tuple(max(0, c - 55) for c in color)
    rim = tuple(min(255, c + 20) for c in color)
    highlight = tuple(min(255, c + 45) for c in color)

    cap_h = max(10, h // 3)
    body_y = y + cap_h // 2
    body_h = max(10, h - cap_h)
    body_rect = pygame.Rect(x + 2, body_y, max(8, w - 4), body_h)

    pygame.draw.rect(surface, side, body_rect, border_radius=max(6, body_h // 4))

    bottom_rect = pygame.Rect(x + 2, body_rect.bottom - cap_h // 2, max(8, w - 4), cap_h)
    pygame.draw.ellipse(surface, shade, bottom_rect)

    top_rect = pygame.Rect(x, y, w, cap_h)
    pygame.draw.ellipse(surface, color, top_rect)
    pygame.draw.ellipse(surface, rim, top_rect, 2)

    gloss_rect = pygame.Rect(x + int(w * 0.20), y + int(cap_h * 0.20), int(w * 0.34), int(cap_h * 0.45))
    pygame.draw.ellipse(surface, highlight, gloss_rect)

    seam_rect = pygame.Rect(x + 3, body_y - 1, max(6, w - 6), 3)
    pygame.draw.ellipse(surface, shade, seam_rect)


def draw_square_tier(surface, color, rect):
    x, y, w, h = rect
    shade = tuple(max(0, c - 30) for c in color)
    side = tuple(max(0, c - 55) for c in color)
    rim = tuple(min(255, c + 20) for c in color)
    highlight = tuple(min(255, c + 45) for c in color)

    cap_h = max(10, h // 3)
    body_y = y + cap_h // 2
    body_h = max(10, h - cap_h)

    body_rect = pygame.Rect(x + 4, body_y, max(8, w - 8), body_h)
    pygame.draw.rect(surface, side, body_rect, border_radius=max(7, body_h // 4))
    pygame.draw.rect(surface, shade, body_rect.inflate(-4, -4), border_radius=max(6, body_h // 4))

    top_rect = pygame.Rect(x + 2, y + 1, max(10, w - 4), cap_h)
    pygame.draw.rect(surface, color, top_rect, border_radius=max(7, cap_h // 2))
    pygame.draw.rect(surface, rim, top_rect, 2, border_radius=max(7, cap_h // 2))

    gloss = pygame.Rect(x + int(w * 0.20), y + int(cap_h * 0.22), int(w * 0.34), int(cap_h * 0.42))
    pygame.draw.ellipse(surface, highlight, gloss)

    seam = pygame.Rect(x + 5, body_y - 1, max(8, w - 10), 3)
    pygame.draw.rect(surface, shade, seam, border_radius=2)


def draw_heart_tier(surface, color, rect):
    x, y, w, h = rect
    side = tuple(max(0, c - 45) for c in color)
    rim = tuple(min(255, c + 20) for c in color)
    highlight = tuple(min(255, c + 45) for c in color)

    cap_h = max(13, int(h * 0.48))
    top_rect = pygame.Rect(x, y, w, cap_h + max(8, int(h * 0.16)))
    pts_top = heart_points((top_rect.x + 2, top_rect.y + 1, top_rect.w - 4, top_rect.h - 2))
    depth = max(8, int(h * 0.26))
    pts_side = [(px, py + depth) for px, py in pts_top]

    pygame.draw.polygon(surface, side, pts_side)
    pygame.draw.polygon(surface, color, pts_top)
    pygame.draw.polygon(surface, rim, pts_top, 2)

    seam = [(px, py + max(2, depth // 3)) for px, py in pts_top]
    pygame.draw.polygon(surface, tuple(max(0, c - 30) for c in color), seam, 2)

    pygame.draw.circle(surface, highlight, (int(x + w * 0.38), int(y + cap_h * 0.45)), max(4, int(w * 0.06)))
    pygame.draw.circle(surface, highlight, (int(x + w * 0.62), int(y + cap_h * 0.45)), max(4, int(w * 0.06)))


def draw_single_heart(surface, color, rect):
    x, y, w, h = rect
    rim = tuple(min(255, c + 18) for c in color)
    shadow = tuple(max(0, c - 28) for c in color)
    highlight = tuple(min(255, c + 40) for c in color)

    main_pts = heart_points((x + 2, y + 2, w - 4, h - 4))
    shadow_pts = [(px, py + max(4, h // 10)) for px, py in main_pts]

    pygame.draw.polygon(surface, shadow, shadow_pts)
    pygame.draw.polygon(surface, color, main_pts)
    pygame.draw.polygon(surface, rim, main_pts, 2)
    pygame.draw.circle(surface, highlight, (int(x + w * 0.38), int(y + h * 0.27)), max(5, int(w * 0.06)))
    pygame.draw.circle(surface, highlight, (int(x + w * 0.62), int(y + h * 0.27)), max(5, int(w * 0.06)))


def draw_tier(surface, shape, color, rect):
    if shape == "Круг":
        draw_round_tier(surface, color, rect)
    elif shape == "Квадрат":
        draw_square_tier(surface, color, rect)
    else:
        draw_heart_tier(surface, color, rect)


def draw_cake(surface, shape, color, detail, rect, layers=2):
    x, y, w, h = rect
    layers = max(1, layers)

    # Soft shadow under cake for extra depth.
    shadow_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.ellipse(shadow_surface, (30, 20, 40, 55), (w * 0.10, h * 0.80, w * 0.80, h * 0.16))
    surface.blit(shadow_surface, (x, y))

    if shape == "Сердце" and layers == 1:
        single_rect = pygame.Rect(x + int(w * 0.06), y + int(h * 0.12), int(w * 0.88), int(h * 0.76))
        draw_single_heart(surface, color, single_rect)
        detail_w = max(14, int(single_rect.w * 0.42))
        detail_h = max(14, int(single_rect.h * 0.26))
        detail_x = single_rect.x + (single_rect.w - detail_w) // 2
        detail_y = single_rect.y + int(single_rect.h * 0.24)
        detail_area = (
            detail_x,
            detail_y,
            detail_w,
            detail_h,
        )
        draw_detail(surface, detail, detail_area)
        return

    if shape == "Круг":
        tier_height = max(30, int((h * 0.82) / (layers + 0.30)))
        overlap = max(2, int(tier_height * 0.08))
    elif shape == "Сердце":
        tier_height = max(30, int((h * 0.84) / (layers + 0.22)))
        overlap = max(18, int(tier_height * 0.66))
    else:
        tier_height = max(28, int((h * 0.76) / (layers + 0.26)))
        overlap = max(12, int(tier_height * 0.40))
    base_y = y + h - tier_height - int(h * 0.08)
    tier_rects = []

    for i in range(layers):
        if shape == "Круг":
            if layers <= 2:
                base_scale = 0.93
                step = 0.22
            else:
                base_scale = 0.90
                step = 0.16
            scale = base_scale - i * step
        elif shape == "Сердце":
            if layers <= 2:
                scale = 1.00 - i * 0.15
            else:
                scale = 0.98 - i * 0.11
        else:
            if layers <= 2:
                scale = 0.96 - i * 0.18
            else:
                scale = 0.94 - i * 0.14
        if shape == "Сердце":
            tier_w = max(42, int(w * scale * 1.06))
        else:
            tier_w = max(42, int(w * scale))
        tier_x = x + (w - tier_w) // 2
        tier_y = base_y - i * (tier_height - overlap)
        tier_rects.append(pygame.Rect(tier_x, tier_y, tier_w, tier_height))

    for tier_rect in tier_rects:
        if shape == "Сердце":
            draw_single_heart(surface, color, tier_rect)
        else:
            draw_tier(surface, shape, color, tier_rect)

    top_tier = tier_rects[-1]
    if shape == "Круг":
        pad_x = max(10, top_tier.w // 4)
        top_cap_h = max(10, top_tier.h // 3)
        detail_area = (top_tier.x + pad_x, top_tier.y + 3, max(14, top_tier.w - 2 * pad_x), max(12, top_cap_h - 5))
    elif shape == "Сердце":
        detail_w = max(14, int(top_tier.w * 0.42))
        detail_h = max(12, int(top_tier.h * 0.24))
        detail_x = top_tier.x + (top_tier.w - detail_w) // 2
        detail_y = top_tier.y + max(4, int(top_tier.h * 0.20))
        detail_area = (detail_x, detail_y, detail_w, detail_h)
    else:
        pad_x = max(10, top_tier.w // 5)
        cap_h = max(10, top_tier.h // 3)
        detail_area = (top_tier.x + pad_x, top_tier.y + 3, max(14, top_tier.w - 2 * pad_x), max(12, cap_h - 4))

    draw_detail(surface, detail, detail_area)


def build_buttons():
    buttons = []

    sx = 352

    sy = 124
    shape_w, shape_h = 180, 42
    shape_gap = 18
    for i, shape in enumerate(SHAPES):
        buttons.append(Button((sx + i * (shape_w + shape_gap), sy, shape_w, shape_h), shape, shape, "shape"))

    cy = 250
    color_w, color_h = 134, 42
    color_gap = 14
    for i, (name, _) in enumerate(COLORS):
        row = i // 4
        col = i % 4
        buttons.append(Button((sx + col * (color_w + color_gap), cy + row * (color_h + 10), color_w, color_h), name, name, "color"))

    dy = 380
    detail_w, detail_h = 134, 42
    detail_gap = 14
    for i, detail in enumerate(DETAILS):
        row = i // 3
        col = i % 3
        buttons.append(Button((sx + col * (detail_w + detail_gap), dy + row * (detail_h + 10), detail_w, detail_h), detail, detail, "detail"))

    submit = Button((744, 536, 200, 52), "Подать торт", "submit", "action")
    return buttons, submit


def build_layer_buttons(available_layers):
    buttons = []
    start_x = 52
    y = 510
    w = 116
    h = 34
    gap = 12
    for i, layers in enumerate(available_layers):
        buttons.append(Button((start_x + i * (w + gap), y, w, h), f"{layers} сл.", layers, "layers"))
    return buttons


def find_color_rgb(name):
    for cname, rgb in COLORS:
        if cname == name:
            return rgb
    return COLORS[0][1]


def evaluate(order, selection):
    score = 0
    score += int(order.shape == selection["shape"])
    score += int(order.layers == selection["layers"])
    score += int(order.color_name == selection["color"])
    score += int(order.detail == selection["detail"])
    bonus = 3 if score == 4 else 0
    return score + bonus, score == 4


def get_required_layers(level):
    return get_available_layers(level)[0]


def get_available_layers(level):
    if level <= 1:
        return [1]
    if level == 2:
        return [2]
    return [3]


def get_order_time(level):
    return max(12, ORDER_TIME - (level - 1) * 2)


def get_combo_multiplier(streak):
    if streak >= 9:
        return 4
    if streak >= 6:
        return 3
    if streak >= 3:
        return 2
    return 1


def draw_panel(surface, rect, title):
    pygame.draw.rect(surface, PANEL, rect, border_radius=18)
    pygame.draw.rect(surface, (216, 197, 233), rect, 2, border_radius=18)
    header = FONT.render(title, True, TEXT)
    surface.blit(header, (rect.x + 16, rect.y + 12))


def main():
    buttons, submit_button = build_buttons()

    cakes_served = 0
    level = 1
    order_time_limit = get_order_time(level)
    order = Order(level)
    order_start = pygame.time.get_ticks()
    selection = {
        "shape": SHAPES[0],
        "layers": LAYER_CHOICES[0],
        "color": COLORS[0][0],
        "detail": DETAILS[0],
    }

    score = 0
    streak = 0
    lives = 3
    result_text = ""
    result_color = TEXT
    game_over = False

    while True:
        CLOCK.tick(FPS)
        available_layers = get_available_layers(level)
        layer_buttons = build_layer_buttons(available_layers)
        if selection["layers"] not in available_layers:
            selection["layers"] = available_layers[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if game_over and event.key == pygame.K_r:
                    cakes_served = 0
                    level = 1
                    order_time_limit = get_order_time(level)
                    order = Order(level)
                    order_start = pygame.time.get_ticks()
                    selection = {"shape": SHAPES[0], "layers": LAYER_CHOICES[0], "color": COLORS[0][0], "detail": DETAILS[0]}
                    score = 0
                    streak = 0
                    lives = 3
                    result_text = ""
                    game_over = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                for lb in layer_buttons:
                    if lb.is_clicked(event.pos):
                        selection["layers"] = lb.value
                for b in buttons:
                    if b.is_clicked(event.pos):
                        selection[b.group] = b.value
                if submit_button.is_clicked(event.pos):
                    gain, perfect = evaluate(order, selection)
                    if perfect:
                        streak += 1
                        combo = get_combo_multiplier(streak)
                        final_gain = gain * combo
                        score += final_gain
                        if combo > 1:
                            result_text = f"Идеально! +{final_gain} (x{combo} комбо)"
                        else:
                            result_text = f"Идеально! +{final_gain}"
                        result_color = GOOD
                    else:
                        score += gain
                        streak = 0
                        lives -= 1
                        result_text = f"Не точно (+{gain}), жизнь -1"
                        result_color = BAD

                    cakes_served += 1
                    level = min(3, cakes_served // 10 + 1)
                    order_time_limit = get_order_time(level)
                    order = Order(level)
                    order_start = pygame.time.get_ticks()

                    if lives <= 0:
                        game_over = True

        elapsed = (pygame.time.get_ticks() - order_start) / 1000.0
        left = max(0, order_time_limit - elapsed)
        if left <= 0 and not game_over:
            lives -= 1
            streak = 0
            result_text = "Слишком медленно! жизнь -1"
            result_color = BAD
            if lives <= 0:
                game_over = True
            else:
                order = Order(level)
                order_start = pygame.time.get_ticks()

        draw_gradient_bg(SCREEN)

        left_panel = pygame.Rect(24, 22, 300, 576)
        right_panel = pygame.Rect(338, 22, 618, 576)
        draw_panel(SCREEN, left_panel, "Текущий заказ")
        draw_panel(SCREEN, right_panel, "Собери торт")

        order_shape = order.shape
        order_color = order.color_rgb
        order_detail = order.detail
        order_layers = order.layers

        draw_cake(SCREEN, order_shape, order_color, order_detail, (58, 86, 232, 230), layers=order_layers)

        SCREEN.blit(FONT.render(f"Форма: {order.shape}", True, TEXT), (52, 330))
        SCREEN.blit(FONT.render(f"Слои: {order.layers}", True, TEXT), (52, 362))
        SCREEN.blit(FONT.render(f"Цвет: {order.color_name}", True, TEXT), (52, 394))
        SCREEN.blit(FONT.render(f"Декор: {order.detail}", True, TEXT), (52, 426))
        level_y = 454
        SCREEN.blit(FONT_SMALL.render(f"Уровень сложности: {level}", True, TEXT), (52, level_y))
        SCREEN.blit(FONT_SMALL.render("Выбери слои:", True, TEXT), (52, level_y + 24))
        for lb in layer_buttons:
            selected = selection["layers"] == lb.value
            lb.draw(SCREEN, selected=selected)

        timer_ratio = left / order_time_limit if order_time_limit > 0 else 0
        pygame.draw.rect(SCREEN, (227, 216, 239), (52, 548, 248, 18), border_radius=9)
        pygame.draw.rect(SCREEN, (115, 83, 166), (52, 548, int(248 * timer_ratio), 18), border_radius=9)
        SCREEN.blit(FONT_SMALL.render(f"Осталось времени: {left:0.1f}с", True, TEXT), (52, 570))

        SCREEN.blit(FONT.render("1) Выбери форму", True, TEXT), (352, 90))
        SCREEN.blit(FONT.render("2) Выбери цвет", True, TEXT), (352, 214))
        SCREEN.blit(FONT.render("3) Выбери декор", True, TEXT), (352, 344))

        for b in buttons:
            selected = selection.get(b.group) == b.value
            b.draw(SCREEN, selected=selected)

        pygame.draw.rect(SCREEN, ACCENT, submit_button.rect, border_radius=14)
        pygame.draw.rect(SCREEN, ACCENT_DARK, submit_button.rect, 2, border_radius=14)
        sb_text = FONT.render(submit_button.text, True, (255, 255, 255))
        SCREEN.blit(sb_text, sb_text.get_rect(center=submit_button.rect.center))

        preview_color = find_color_rgb(selection["color"])
        preview_box = pygame.Rect(786, 352, 152, 154)
        pygame.draw.rect(SCREEN, (243, 234, 250), preview_box, border_radius=14)
        pygame.draw.rect(SCREEN, (216, 197, 233), preview_box, 2, border_radius=14)
        draw_cake(SCREEN, selection["shape"], preview_color, selection["detail"], (794, 372, 136, 122), layers=selection["layers"])
        SCREEN.blit(FONT_SMALL.render("Предпросмотр", True, TEXT), (790, 358))

        SCREEN.blit(FONT.render(f"Очки: {score}", True, TEXT), (352, 506))
        SCREEN.blit(FONT.render(f"Жизни: {lives}", True, TEXT), (500, 506))
        SCREEN.blit(FONT.render(f"Серия: {streak}", True, TEXT), (630, 506))
        SCREEN.blit(FONT_SMALL.render(f"Уровень: {level}", True, TEXT), (352, 540))
        SCREEN.blit(FONT_SMALL.render(f"Тортов: {cakes_served}", True, TEXT), (500, 540))
        SCREEN.blit(FONT_SMALL.render(f"Комбо: x{get_combo_multiplier(streak)}", True, TEXT), (630, 540))

        if result_text:
            SCREEN.blit(FONT_SMALL.render(result_text, True, result_color), (352, 570))

        if game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((35, 20, 54, 170))
            SCREEN.blit(overlay, (0, 0))
            msg1 = FONT_BIG.render("Игра окончена", True, (255, 255, 255))
            msg2 = FONT.render(f"Финальные очки: {score}", True, (255, 255, 255))
            msg3 = FONT_SMALL.render("Нажми R для перезапуска или ESC для выхода", True, (255, 255, 255))
            SCREEN.blit(msg1, msg1.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40)))
            SCREEN.blit(msg2, msg2.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 6)))
            SCREEN.blit(msg3, msg3.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 42)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
