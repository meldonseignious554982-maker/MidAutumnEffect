import pygame
import random
import math
import sys
import os

# ==============================================================================
#                      【用户自定义参数配置区】
# ==============================================================================

# 1. 窗口基础与路径
WIDTH, HEIGHT = 1000, 720
FPS = 60

FONT_FILENAME = 'ty.ttf'
FONT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), FONT_FILENAME)
MUSIC_FILENAME = 'bgm.flac'  
MUSIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MUSIC_FILENAME)


# ------------------ 【A. 背景代码雨独立配置】 ------------------
FONT_SIZE_MATRIX = 20          # 代码雨字号
MATRIX_COL_SPACING = 3        # 列间距（越小越密集）
MATRIX_SPEED_MIN = 0.3         # 下落最小速度
MATRIX_SPEED_MAX = 1.0         # 下落最大速度
FADE_TRAIL_ALPHA = 25          # 拖影长度（越小拖影越长）
MATRIX_CHARS = "中秋快乐皆如所愿阖家团圆岁岁平安月圆人圆"

# 代码雨独立颜色组
HEX_COLORS_RAIN = [
    "#6e9dad",  # 雾霾蓝
    "#b36879",  # 柔粉
    "#ad9a50",  # 暖金
    "#afaaaa"   # 纯白
]


# ------------------ 【B. 爱心与爆发火花独立配置】 ------------------
HEX_COLOR_HEART       = "#f688a7"   # 爱心本体颜色
HEX_COLOR_CENTER_TEXT = "#FFF066"   # 爱心中文字“中秋快乐”颜色

HEX_COLORS_SPARKS = [
    "#6e9dad",  # 蓝火花
    "#FF85A1",  # 粉火花
    "#FFE066",  # 金火花
    "#FFFFFF"   # 白火花
]

MINI_HEART_SIZE   = 7          # 爱心本体的小粒子大小
HEART_SCALE       = 15         # 爱心大小
HEART_THICKNESS   = 3          # 爱心厚度
HEART_BURST_COUNT = 15         # 每帧向外爆发的火花爱心数量
HEART_BURST_SPEED = 2.0        # 爆发初速度

HEART_SWAY_AMP_X  = 17.0       # 左右晃动幅度
HEART_SWAY_AMP_Y  = 11.0       # 上下晃动幅度
HEART_SWAY_SPEED  = 0.020      # 漂浮速度


# ------------------ 【C. 前景文字独立配置】 ------------------
FONT_SIZE_LARGE   = 190        # 倒计时、祝福语字号
FONT_SIZE_CENTER  = 60         # 爱心内部“中秋快乐”字号

HEX_COLORS_TEXT = [
    "#FFFFFF",  # 3
    "#FFFFFF",  # 2
    "#FFFFFF",  # 1
    "#FFFFFF",  # 亲爱的
    "#FFFFFF",  # 祝你
    "#FFFFFF",  # 中秋快乐
    "#FFFFFF",  # 岁岁无忧
]


# ------------------ 【D. 结束画面逐字渐显独立配置】 ------------------
ENDING_TEXT           = "此生风月愿同携\n岁岁晨昏共执蹄"   # 结束寄语（支持 \n 换行）
FONT_SIZE_ENDING      = 54                         # 矢量高清字号
HEX_COLOR_ENDING_TEXT = "#FFFFFF"                  # 结束字体颜色
CHAR_APPEAR_INTERVAL  = 10                         # 每一个字出现的间隔帧数（约0.16秒一个字，自然流畅）
ENDING_DURATION       = 312                        # 结束画面总时长（帧数，约5.2秒）


# ------------------ 【各状态停留时长（帧数）】 ------------------
STATE_DURATIONS = [65, 65, 65, 90, 90, 110, 110, 3720, ENDING_DURATION]


# ==============================================================================
#                     【辅助工具与渲染核心】
# ==============================================================================

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

RAIN_COLORS       = [hex_to_rgb(c) for c in HEX_COLORS_RAIN]
SPARK_COLORS      = [hex_to_rgb(c) for c in HEX_COLORS_SPARKS]
COLOR_HEART       = hex_to_rgb(HEX_COLOR_HEART)
COLOR_CENTER_TEXT = hex_to_rgb(HEX_COLOR_CENTER_TEXT)
COLORS_TEXT       = [hex_to_rgb(c) for c in HEX_COLORS_TEXT]
COLOR_ENDING_TEXT = hex_to_rgb(HEX_COLOR_ENDING_TEXT)

pygame.init()
pygame.mixer.init()

def restart_music():
    if os.path.exists(MUSIC_PATH):
        try:
            pygame.mixer.music.load(MUSIC_PATH)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"音频加载失败: {e}")

restart_music()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("中秋代码雨 & 爱心爆发粒子")
clock = pygame.time.Clock()

if not os.path.exists(FONT_PATH):
    print(f"【错误提示】未在当前目录找到字体文件：{FONT_PATH}")
    sys.exit()

font_matrix = pygame.font.Font(FONT_PATH, FONT_SIZE_MATRIX)
font_large  = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
font_center = pygame.font.Font(FONT_PATH, FONT_SIZE_CENTER)
font_ending = pygame.font.Font(FONT_PATH, FONT_SIZE_ENDING)

def create_heart_texture(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r = size / 4.0
    pygame.draw.circle(surf, color, (int(r), int(r)), int(r))
    pygame.draw.circle(surf, color, (int(3 * r), int(r)), int(r))
    points = [(0, int(r * 1.2)), (size, int(r * 1.2)), (size / 2, size)]
    pygame.draw.polygon(surf, color, points)
    return surf

heart_texture_cache = {
    'heart': create_heart_texture(MINI_HEART_SIZE, COLOR_HEART),
    'text': create_heart_texture(MINI_HEART_SIZE - 2, COLOR_CENTER_TEXT)
}


# ================= 背景代码雨 =================
class MatrixRain:
    def __init__(self):
        self.cols = WIDTH // MATRIX_COL_SPACING
        self.drops = [random.randint(-40, 0) for _ in range(self.cols)]
        self.speeds = [random.uniform(MATRIX_SPEED_MIN, MATRIX_SPEED_MAX) for _ in range(self.cols)]
        self.col_colors = [random.choice(RAIN_COLORS) for _ in range(self.cols)]
        self.trail_surface = pygame.Surface((WIDTH, HEIGHT))
        self.trail_surface.fill((0, 0, 0))

    def update_and_draw(self, surface):
        self.trail_surface.set_alpha(FADE_TRAIL_ALPHA)
        surface.blit(self.trail_surface, (0, 0))

        for i in range(self.cols):
            char = random.choice(MATRIX_CHARS)
            base_col = self.col_colors[i]
            shade = random.randint(0, 50)
            color = (max(0, base_col[0] - shade), max(0, base_col[1] - shade), max(0, base_col[2] - shade))
            txt = font_matrix.render(char, True, color)
            
            x = i * MATRIX_COL_SPACING
            y = self.drops[i] * FONT_SIZE_MATRIX
            surface.blit(txt, (x, y))

            if y > HEIGHT and random.random() > 0.96:
                self.drops[i] = 0
                self.col_colors[i] = random.choice(RAIN_COLORS)
                
            self.drops[i] += self.speeds[i] * 0.18


# ================= 爱心爆发火花 =================
class BurstHeartSpark:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        spd = random.uniform(1.2, HEART_BURST_SPEED)
        self.vx = math.cos(angle) * spd + random.uniform(-0.4, 0.4)
        self.vy = math.sin(angle) * spd + random.uniform(-0.4, 0.4)
        self.life = 40
        self.max_life = 40
        self.color = random.choice(SPARK_COLORS)
        self.size = random.randint(5, 9)
        self.texture = create_heart_texture(self.size, self.color)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= 1

    def draw(self, surface):
        if self.life > 0:
            alpha = int(255 * (self.life / self.max_life))
            self.texture.set_alpha(alpha)
            surface.blit(self.texture, (int(self.x - self.size // 2), int(self.y - self.size // 2)))


# ================= 粒子采样辅助 =================
def sample_text_to_particles(text, font, step=5):
    surf = font.render(text, True, (255, 255, 255))
    w, h = surf.get_size()
    points = []
    for x in range(0, w, step):
        for y in range(0, h, step):
            if surf.get_at((x, y))[3] > 120:
                points.append((WIDTH // 2 - w // 2 + x, HEIGHT // 2 - h // 2 + y))
    return points

def get_heart_curve_point(t, scale):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    return WIDTH // 2 + x * scale, HEIGHT // 2 + y * scale - 25


# ================= 主粒子系统 =================
class SuperParticleSystem:
    def __init__(self):
        self.particles = []
        self.sparks = []
        self.color = COLORS_TEXT[0]
        self.is_heart_mode = False
        self.is_ending_mode = False
        self.heart_border_points = []
        self.heart_pulse = 0.0
        self.sway_timer = 0.0
        
        # 结束画面专属控制变量
        self.ending_timer = 0
        self.ending_char_data = []

    def prepare_ending_text(self):
        self.ending_timer = 0
        self.ending_char_data = []
        lines = ENDING_TEXT.split('\n')
        line_spacing = 26
        
        total_h = len(lines) * FONT_SIZE_ENDING + (len(lines) - 1) * line_spacing
        cur_y = HEIGHT // 2 - total_h // 2

        global_char_idx = 0
        for line_idx, line in enumerate(lines):
            line_w = sum(font_ending.size(ch)[0] for ch in line)
            cur_x = WIDTH // 2 - line_w // 2
            
            pause_between_lines = 15 if line_idx > 0 else 0

            for ch in line:
                cw, ch_h = font_ending.size(ch)
                start_frame = global_char_idx * CHAR_APPEAR_INTERVAL + pause_between_lines
                self.ending_char_data.append({
                    'char': ch,
                    'x': cur_x,
                    'y': cur_y,
                    'w': cw,
                    'h': ch_h,
                    'start_frame': start_frame
                })
                cur_x += cw
                global_char_idx += 1

            cur_y += FONT_SIZE_ENDING + line_spacing

    def set_target(self, state_idx):
        targets = []
        self.is_heart_mode = (state_idx == 7)
        self.is_ending_mode = (state_idx == 8)

        if self.is_heart_mode:
            self.heart_border_points = []
            num_heart_particles = 1300
            for _ in range(num_heart_particles):
                t = random.uniform(0, math.pi * 2)
                scale_offset = random.gauss(0, HEART_THICKNESS * 0.45)
                s = HEART_SCALE + scale_offset
                px, py = get_heart_curve_point(t, s)
                targets.append((px, py, 'heart'))
                
                if abs(scale_offset) < 0.8:
                    self.heart_border_points.append((px, py, t))

            center_pts = sample_text_to_particles("中秋快乐", font_center, step=4)
            for pt in center_pts:
                targets.append((pt[0], pt[1] + 0, 'text'))

        elif self.is_ending_mode:
            # 1. 音乐 2.5 秒平滑渐隐淡出（修改为2500毫秒）
            pygame.mixer.music.fadeout(2500)
            
            # 2. 初始化逐字排版数据
            self.prepare_ending_text()
            
            # 3. 爱心粒子化为星光消散
            cx, cy = WIDTH // 2, HEIGHT // 2 - 25
            for p in self.particles:
                angle = math.atan2(p['y'] - cy, p['x'] - cx) + random.uniform(-0.4, 0.4)
                spd = random.uniform(1.5, 5.0)
                p['vx'] = math.cos(angle) * spd
                p['vy'] = math.sin(angle) * spd
                p['type'] = 'stardust'
                p['alpha'] = 255.0
                p['decay'] = random.uniform(1.2, 2.8)
                p['size'] = random.choice([1, 2, 2, 3])
                p['color'] = random.choice(SPARK_COLORS)
            return

        else:
            self.color = COLORS_TEXT[min(state_idx, len(COLORS_TEXT)-1)]
            seq = ["3", "2", "1", "亲爱的", "祝 你", "中秋快乐", "岁岁无忧"]
            raw_pts = sample_text_to_particles(seq[state_idx], font_large, step=6)
            for pt in raw_pts:
                targets.append((pt[0], pt[1], 'normal'))

        random.shuffle(targets)

        while len(self.particles) < len(targets):
            self.particles.append({'x': random.randint(0, WIDTH), 'y': random.randint(0, HEIGHT), 'type': 'normal'})
        if len(self.particles) > len(targets):
            self.particles = self.particles[:len(targets)]

        for i, pt in enumerate(targets):
            self.particles[i]['tx'] = pt[0]
            self.particles[i]['ty'] = pt[1]
            self.particles[i]['type'] = pt[2]

    def update_and_draw(self, surface):
        if self.is_heart_mode:
            self.sway_timer += HEART_SWAY_SPEED
            sway_offset_x = math.sin(self.sway_timer) * HEART_SWAY_AMP_X
            sway_offset_y = math.cos(self.sway_timer * 0.7) * HEART_SWAY_AMP_Y
            pulse_offset = math.sin(self.heart_pulse) * 3.5
            self.heart_pulse += 0.08
        else:
            sway_offset_x = 0
            sway_offset_y = 0
            pulse_offset = 0

        # 1. 粒子运动与绘制
        if self.is_ending_mode:
            for p in self.particles:
                if p['alpha'] > 0:
                    p['x'] += p['vx']
                    p['y'] += p['vy']
                    p['vx'] *= 0.985
                    p['vy'] *= 0.985
                    p['alpha'] = max(0.0, p['alpha'] - p['decay'])

                    star_c = (
                        int(p['color'][0] * (p['alpha'] / 255)),
                        int(p['color'][1] * (p['alpha'] / 255)),
                        int(p['color'][2] * (p['alpha'] / 255))
                    )
                    pygame.draw.circle(surface, star_c, (int(p['x']), int(p['y'])), p['size'])
        else:
            for p in self.particles:
                p['x'] += (p['tx'] - p['x']) * 0.08 + random.uniform(-0.5, 0.5)
                p['y'] += (p['ty'] - p['y']) * 0.08 + random.uniform(-0.5, 0.5)

                final_x = p['x'] + sway_offset_x
                final_y = p['y'] + pulse_offset + sway_offset_y

                if p['type'] == 'heart':
                    surface.blit(heart_texture_cache['heart'], (int(final_x - MINI_HEART_SIZE // 2), int(final_y - MINI_HEART_SIZE // 2)))
                elif p['type'] == 'text':
                    surface.blit(heart_texture_cache['text'], (int(final_x - 4), int(final_y - 4)))
                else:
                    pygame.draw.circle(surface, self.color, (int(final_x), int(final_y)), 3)

        # 2. 爱心爆发火花
        if self.is_heart_mode and self.heart_border_points:
            for _ in range(HEART_BURST_COUNT):
                bx, by, _ = random.choice(self.heart_border_points)
                real_bx = bx + sway_offset_x
                real_by = by + sway_offset_y
                center_x = WIDTH // 2 + sway_offset_x
                center_y = HEIGHT // 2 - 25 + sway_offset_y
                out_angle = math.atan2(real_by - center_y, real_bx - center_x)
                self.sparks.append(BurstHeartSpark(real_bx, real_by, out_angle))

        for s in self.sparks[:]:
            s.update()
            s.draw(surface)
            if s.life <= 0:
                self.sparks.remove(s)

        # 3. 逐字渐显结束语
        if self.is_ending_mode:
            self.ending_timer += 1
            for item in self.ending_char_data:
                if self.ending_timer >= item['start_frame']:
                    fade_progress = min(1.0, (self.ending_timer - item['start_frame']) / 15.0)
                    alpha = int(255 * fade_progress)
                    offset_y = (1.0 - fade_progress) * 4.0

                    char_surf = font_ending.render(item['char'], True, COLOR_ENDING_TEXT)
                    container = pygame.Surface(char_surf.get_size(), pygame.SRCALPHA)
                    container.blit(char_surf, (0, 0))
                    container.fill((255, 255, 255, alpha), special_flags=pygame.BLEND_RGBA_MULT)
                    
                    surface.blit(container, (item['x'], item['y'] - offset_y))


# ================= 主循环 =================
matrix = MatrixRain()
system = SuperParticleSystem()
system.set_target(0)

cur_state = 0
timer = 0
running = True

black_fade = pygame.Surface((WIDTH, HEIGHT))
black_fade.fill((0, 0, 0))
fade_alpha = 0
is_fading_in = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    timer += 1
    if timer > STATE_DURATIONS[cur_state]:
        if cur_state < len(STATE_DURATIONS) - 1:
            timer = 0
            cur_state += 1
            system.set_target(cur_state)
        else:
            fade_alpha += 4
            if fade_alpha >= 255:
                cur_state = 0
                timer = 0
                system.set_target(0)
                restart_music()
                is_fading_in = True

    if is_fading_in:
        fade_alpha -= 5
        if fade_alpha <= 0:
            fade_alpha = 0
            is_fading_in = False

    matrix.update_and_draw(screen)
    system.update_and_draw(screen)

    if fade_alpha > 0:
        black_fade.set_alpha(min(255, max(0, fade_alpha)))
        screen.blit(black_fade, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()