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
MUSIC_FILENAME = 'bgm.mp3'  
MUSIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), MUSIC_FILENAME)


# ------------------ 【A. 背景代码雨独立配置】 ------------------
FONT_SIZE_MATRIX = 25          # 代码雨字号
MATRIX_COL_SPACING = 2.8       # 列间距（支持小数微调）
MATRIX_SPEED_MIN = 0.2         # 下落最小速度
MATRIX_SPEED_MAX = 1.0         # 下落最大速度
FADE_TRAIL_ALPHA = 22          # 拖影长度（越小拖影越长）
MATRIX_CHARS = "但愿人长久，千里共婵娟。若可，我愿与你共婵娟，也共人间烟火"

# 代码雨文字跳变速率
MATRIX_CHAR_MUTATE_RATE = 0.08

HEX_COLORS_RAIN = [
    "#6e9dad",  # 雾霾蓝
    "#b36879",  # 柔粉
    "#ad9a50",  # 暖金
    "#afaaaa"   # 纯白
]


# ------------------ 【B-1. 爱心本体独立配置】 ------------------
HEX_COLOR_HEART       = "#f688a7"   # 爱心本体颜色
HEX_COLOR_CENTER_TEXT = "#FFF066"   # 爱心中心字颜色（暖金黄）

MINI_HEART_SIZE       = 12         # 大爱心本体的粒子大小（保持你的饱满大颗粒）
HEART_SCALE           = 16         # 爱心大小
HEART_THICKNESS       = 3          # 爱心厚度

# 【核心优化】：爱心中间汉字独立粒子参数（彻底解决臃肿黏连糊在一起！）
CENTER_PARTICLE_SIZE  = 5          # 中文字粒子大小（默认4，笔画纤细分明绝不糊，可调 3~5）
CENTER_TEXT_STEP      = 3          # 文字采样间距

HEART_SWAY_AMP_X      = 17.0       # 左右晃动幅度
HEART_SWAY_AMP_Y      = 11.0       # 上下晃动幅度
HEART_SWAY_SPEED      = 0.020      # 漂浮速度


# ------------------ 【B-2. 爱心周围扩散火花粒子独立配置】 ------------------
HEX_COLORS_SPARKS = [
    "#c6e2ff",  # 蓝火花
    "#FF85A1",  # 粉火花
    "#FFE066",  # 金火花
    "#FFFFFF"   # 白火花
]

SPARK_COUNT        = 19        # 每帧向外爆发扩散的粒子数量
SPARK_SIZE_MIN     = 5         # 扩散粒子的最小尺寸（像素）
SPARK_SIZE_MAX     = 20        # 扩散粒子的最大尺寸（像素）
SPARK_SPEED_MIN    = 1.2       # 扩散向外飞散的最小初速度
SPARK_SPEED_MAX    = 2.7       # 扩散向外飞散的最大初速度
SPARK_LIFE         = 55        # 扩散粒子存活寿命/距离
SPARK_DRAG         = 0.96      # 空气阻力减速比
SPARK_SPREAD_ANGLE = 0.6       # 发散角度扰动


# ------------------ 【C. 前景文字序列（含 10 字超长句）】 ------------------
FONT_SIZE_LARGE   = 190        # 基准大字字号
HEX_COLOR_FOREGROUND = "#c6e2ff" # 优雅冰蓝

FONT_SIZE_CENTER  = 48         # 爱心双行中心字字号（统一 48px，工整对称）

FOREGROUND_TEXTS = [
    "3", "2", "1",
    "亲爱的",
    "见字如面",
    "今夕何夕",
    "月满中秋",
    "祝 你",
    "中秋快乐",
    "所念皆所愿",
    "所行皆坦途",
    "与你",
    "皓月同心",
    "共赴婵娟",
    "愿我如星君如月",
    "夜夜流光相皎洁",
    "月亮是天空的情书",
    "你是我的已读心动",
    "中秋月圆",
    "愿往后年年良辰",
    "皆与你相伴"
]

FOREGROUND_DURATIONS = [
    70, 70, 70,               # 3, 2, 1 倒计时
    100,                       # 亲爱的
    105,                       # 见字如面
    105,                       # 今夕何夕
    105,                       # 月满中秋
    105,                       # 祝 你
    105,                      # 中秋快乐
    120,                      # 所念皆所愿
    120,                      # 所行皆坦途
    100,                       # 与你
    120,                      # 皓月同心
    120,                       # 共赴婵娟
    150,                       # 愿我如星君如月 (7字)
    150,                       # 夜夜流光相皎洁 (7字)
    155,                       # 月亮是天空的情书 (8字)
    155,                       # 你是我的已读心动 (8字)
    135,                       # 中秋月圆
    140,                       # 愿往后年年良辰 (7字)
    150                        # 皆与你相伴
]


# ------------------ 【D. 时长数学锁死：总时长精确 1 分 17 秒】 ------------------
TARGET_TOTAL_SECONDS  = 77                         # 目标总时长 1分17秒 = 77秒
TARGET_TOTAL_FRAMES   = TARGET_TOTAL_SECONDS * FPS # 77 * 60 = 4620 帧

ENDING_TEXT           = "今夜月明人尽望\n我的秋思只落你身上"   # 结束寄语
FONT_SIZE_ENDING      = 54                         # 矢量高清字号
HEX_COLOR_ENDING_TEXT = "#c6e2ff"                  # 优雅冰蓝
CHAR_APPEAR_INTERVAL  = 10                         # 每一个字出现的间隔帧数
ENDING_DURATION       = 312                        # 结束画面总时长（约5.2秒）

# 动态精准计算爱心时长
HEART_DURATION = TARGET_TOTAL_FRAMES - sum(FOREGROUND_DURATIONS) - ENDING_DURATION

STATE_DURATIONS = FOREGROUND_DURATIONS + [HEART_DURATION, ENDING_DURATION]


# ------------------ 【E. 右下角若隐若现水印签名独立配置】 ------------------
WATERMARK_TEXT          = "-To my kxx"          # 水印内容
FONT_SIZE_WATERMARK     = FONT_SIZE_MATRIX     # 默认与背景字体大小相同（25px）
WATERMARK_MAX_ALPHA     = 5                   # 最高显现亮度
WATERMARK_MIN_ALPHA     = 2                    # 最低隐去亮度
WATERMARK_BREATHE_SPEED = 0.020                # 呼吸明暗起伏速度


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
COLOR_FOREGROUND  = hex_to_rgb(HEX_COLOR_FOREGROUND)
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

font_matrix    = pygame.font.Font(FONT_PATH, FONT_SIZE_MATRIX)
font_large     = pygame.font.Font(FONT_PATH, FONT_SIZE_LARGE)
font_center    = pygame.font.Font(FONT_PATH, FONT_SIZE_CENTER)
font_ending    = pygame.font.Font(FONT_PATH, FONT_SIZE_ENDING)
font_watermark = pygame.font.Font(FONT_PATH, FONT_SIZE_WATERMARK)

def create_heart_texture(size, color):
    surf = pygame.Surface((size, size), pygame.SRCALPHA)
    r = size / 4.0
    pygame.draw.circle(surf, color, (int(r), int(r)), int(r))
    pygame.draw.circle(surf, color, (int(3 * r), int(r)), int(r))
    points = [(0, int(r * 1.2)), (size, int(r * 1.2)), (size / 2, size)]
    pygame.draw.polygon(surf, color, points)
    return surf

# 贴图缓存：中心文字使用独立的纤细小爱心贴图（4px），彻底告别粗笨重叠！
heart_texture_cache = {
    'heart': create_heart_texture(MINI_HEART_SIZE, COLOR_HEART),
    'text': create_heart_texture(CENTER_PARTICLE_SIZE, COLOR_CENTER_TEXT)
}


# ================= 背景代码雨 =================
class MatrixRain:
    def __init__(self):
        self.cols = int(WIDTH / MATRIX_COL_SPACING)
        self.drops = [random.randint(-40, 0) for _ in range(self.cols)]
        self.speeds = [random.uniform(MATRIX_SPEED_MIN, MATRIX_SPEED_MAX) for _ in range(self.cols)]
        self.col_colors = [random.choice(RAIN_COLORS) for _ in range(self.cols)]
        self.col_chars = [random.choice(MATRIX_CHARS) for _ in range(self.cols)]
        self.trail_surface = pygame.Surface((WIDTH, HEIGHT))
        self.trail_surface.fill((0, 0, 0))

    def update_and_draw(self, surface):
        self.trail_surface.set_alpha(FADE_TRAIL_ALPHA)
        surface.blit(self.trail_surface, (0, 0))

        for i in range(self.cols):
            if random.random() < MATRIX_CHAR_MUTATE_RATE:
                self.col_chars[i] = random.choice(MATRIX_CHARS)
            char = self.col_chars[i]

            base_col = self.col_colors[i]
            shade = random.randint(0, 50)
            color = (max(0, base_col[0] - shade), max(0, base_col[1] - shade), max(0, base_col[2] - shade))
            txt = font_matrix.render(char, True, color)
            
            x = int(i * MATRIX_COL_SPACING)
            y = self.drops[i] * FONT_SIZE_MATRIX
            surface.blit(txt, (x, y))

            if y > HEIGHT and random.random() > 0.96:
                self.drops[i] = 0
                self.col_colors[i] = random.choice(RAIN_COLORS)
                self.col_chars[i] = random.choice(MATRIX_CHARS)
                
            self.drops[i] += self.speeds[i] * 0.18


# ================= 爱心爆发火花 =================
class BurstHeartSpark:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        spd = random.uniform(SPARK_SPEED_MIN, SPARK_SPEED_MAX)
        self.vx = math.cos(angle) * spd + random.uniform(-SPARK_SPREAD_ANGLE, SPARK_SPREAD_ANGLE)
        self.vy = math.sin(angle) * spd + random.uniform(-SPARK_SPREAD_ANGLE, SPARK_SPREAD_ANGLE)
        self.life = SPARK_LIFE
        self.max_life = SPARK_LIFE
        self.color = random.choice(SPARK_COLORS)
        self.size = random.randint(SPARK_SIZE_MIN, SPARK_SIZE_MAX)
        self.texture = create_heart_texture(self.size, self.color)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= SPARK_DRAG
        self.vy *= SPARK_DRAG
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

def sample_dynamic_foreground_text(text):
    clean_len = len(text.replace(" ", ""))
    if clean_len >= 10:
        target_size = int(FONT_SIZE_LARGE * 0.44)
    elif clean_len >= 8:
        target_size = int(FONT_SIZE_LARGE * 0.52)
    elif clean_len >= 7:
        target_size = int(FONT_SIZE_LARGE * 0.60)
    elif clean_len >= 5:
        target_size = int(FONT_SIZE_LARGE * 0.72)
    elif clean_len == 4:
        target_size = int(FONT_SIZE_LARGE * 0.85)
    else:
        target_size = FONT_SIZE_LARGE             
    
    dyn_font = pygame.font.Font(FONT_PATH, target_size)
    return sample_text_to_particles(text, dyn_font, step=4)

def get_heart_curve_point(t, scale):
    x = 16 * (math.sin(t) ** 3)
    y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
    return WIDTH // 2 + x * scale, HEIGHT // 2 + y * scale - 25


# ================= 主粒子系统 =================
class SuperParticleSystem:
    def __init__(self):
        self.particles = []
        self.sparks = []
        self.color = COLOR_FOREGROUND
        self.is_heart_mode = False
        self.is_ending_mode = False
        self.heart_border_points = []
        self.heart_pulse = 0.0
        self.sway_timer = 0.0
        
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
        num_texts = len(FOREGROUND_TEXTS)

        # 1. 前置文字序列播放
        if state_idx < num_texts:
            self.is_heart_mode = False
            self.is_ending_mode = False
            current_text = FOREGROUND_TEXTS[state_idx]
            raw_pts = sample_dynamic_foreground_text(current_text)
            for pt in raw_pts:
                targets.append((pt[0], pt[1], 'normal'))

        # 2. 大爱心内部双行统一字号（应用独立微雕级粒子步长）
        elif state_idx == num_texts:
            self.is_heart_mode = True
            self.is_ending_mode = False
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

            # 中心文字使用独立的 CENTER_TEXT_STEP 细腻采样
            pts_top = sample_text_to_particles("中秋快乐", font_center, step=CENTER_TEXT_STEP)
            for pt in pts_top:
                targets.append((pt[0], pt[1] - 28, 'text'))

            pts_sub = sample_text_to_particles("不止中秋", font_center, step=CENTER_TEXT_STEP)
            for pt in pts_sub:
                targets.append((pt[0], pt[1] + 28, 'text'))

        # 3. 结束画面落幕
        else:
            self.is_heart_mode = False
            self.is_ending_mode = True
            pygame.mixer.music.fadeout(2500)
            self.prepare_ending_text()
            
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
                    # 【核心优化】：按独立的 4px 精细尺寸居中贴图，笔画彻底分明！
                    surface.blit(heart_texture_cache['text'], (int(final_x - CENTER_PARTICLE_SIZE // 2), int(final_y - CENTER_PARTICLE_SIZE // 2)))
                else:
                    pygame.draw.circle(surface, self.color, (int(final_x), int(final_y)), 3)

        if self.is_heart_mode and self.heart_border_points:
            for _ in range(SPARK_COUNT):
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


# ================= 水印绘制辅助函数 =================
def draw_watermark(surface, alpha):
    if alpha <= 0:
        return
    text_surf = font_watermark.render(WATERMARK_TEXT, True, (200, 225, 255))
    temp_surf = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
    temp_surf.blit(text_surf, (0, 0))
    
    alpha_mask = pygame.Surface(text_surf.get_size(), pygame.SRCALPHA)
    alpha_mask.fill((255, 255, 255, alpha))
    temp_surf.blit(alpha_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    
    pos = (WIDTH - text_surf.get_width() - 25, HEIGHT - text_surf.get_height() - 20)
    surface.blit(temp_surf, pos)


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

watermark_time = 0.0

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

    watermark_time += WATERMARK_BREATHE_SPEED
    norm_sin = (math.sin(watermark_time) + 1.0) / 2.0
    cur_wm_alpha = int(WATERMARK_MIN_ALPHA + norm_sin * (WATERMARK_MAX_ALPHA - WATERMARK_MIN_ALPHA))
    draw_watermark(screen, cur_wm_alpha)

    if fade_alpha > 0:
        black_fade.set_alpha(min(255, max(0, fade_alpha)))
        screen.blit(black_fade, (0, 0))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
