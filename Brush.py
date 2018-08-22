#-*- coding:utf-8 -*-
import pygame
import math
from pygame.locals import *
# 定义刷子类
class Brush(object):
    def __init__(self, screen):
        # 刷子的屏幕
        self.screen = screen
        self.drawing = False
        # 颜色
        self.color = (0, 0, 0)
        self.size = 1
        self.last_pos = None
        self.space = 1
        # if style is True, normal solid brush
        # if style is False, png brush
        self.style = False
        self.brush = pygame.image.load("./images/brush.png")
        # 设置当前刷子的尺寸
        self.brush_now = self.brush.subsurface((0, 0), (1, 1))

    def start_draw(self, pos):
        self.drawing = True
        # 当前鼠标位置
        self.last_pos = pos
    def end_draw(self):
        self.drawing = False
    # 设置刷子类型
    def set_brush_style(self,style):
        print("* set brush style to", style)
        self.style = style
    def get_brush_style(self):
        return self.style

    def get_current_brush(self):
        return self.brush_now

    def set_size(self, size):
        # 设置刷子大小上下限
        # if size < 0.5: size = 0.5
        if size < 1: size = 1
        elif size > 50: size = 50
        print("* set brush size to", size)
        self.size = size
        #刷新新的刷子大小
        self.brush_now = self.brush.subsurface((0, 0), (size*2, size*2))
    # 得到刷子的大小
    def get_size(self):
        return self.size
    # 设定颜色
    def set_color(self, color):
        self.color = color
        for i in xrange(self.brush.get_width()):
            for j in xrange(self.brush.get_height()):
                self.brush.set_at((i, j), color + (self.brush.get_at((i, j)).a,))
    def get_color(self):
        return self.color

    def draw(self, pos):
        # line(Surface, color, start_pos, end_pos, width=1) -> Rect
        # pygame.draw.line(self.screen, self.color, self.last_pos, pos, self.size*2)
        # self.last_pos = pos
        # circle(Surface, color, pos, radius, width=0) -> Rect
        # pygame.draw.circle(self.screen, self.color, pos, self.size)
        if self.drawing:
            # 从_get_points方法得到点集
            for p in self._get_points(pos):
                # 如果刷子类型没有改变则直接画图
                if self.style == False:
                        pygame.draw.circle(self.screen, self.color, p, self.size)
                else:
                    self.screen.blit(self.brush_now, p)

            self.last_pos = pos

    def _get_points(self, pos):
        # 得到当前鼠标的坐标
        points = [(self.last_pos[0], self.last_pos[1])]
        len_x = pos[0] - self.last_pos[0]
        len_y = pos[1] - self.last_pos[1]
        # 向量x，y的长度
        length = math.sqrt(len_x ** 2 + len_y ** 2)
        # x，y的单位向量
        step_x = len_x / length
        step_y = len_y / length
        for i in xrange(int(length)):
            # 添加上一个点到下一个点之间所有的点
            points.append((points[-1][0] + step_x, points[-1][1] + step_y))
        # 五入取整
        points = map(lambda x: (int(0.5 + x[0]), int(0.5 + x[1])), points)
        # 去重
        return list(set(points))
# 定义菜单类
class Menu(object):
    def __init__(self, screen):
        self.screen = screen
        self.brush = None
        self.colors = [
            (0xff, 0x00, 0xff), (0x80, 0x00, 0x80),
            (0x00, 0x00, 0xff), (0x00, 0x00, 0x80),
            (0x00, 0xff, 0xff), (0x00, 0x80, 0x80),
            (0x00, 0xff, 0x00), (0x00, 0x80, 0x00),
            (0xff, 0xff, 0x00), (0x80, 0x80, 0x00),
            (0xff, 0x00, 0x00), (0x80, 0x00, 0x00),
            (0xc0, 0xc0, 0xc0), (0xff, 0xff, 0xff),
            (0x00, 0x00, 0x00), (0x80, 0x80, 0x80),
        ]
        # 初始化颜色条
        self.colors_rect = []
        # 得到序号和颜色
        for (i, rgb) in enumerate(self.colors):
            rect = pygame.Rect(10 + i % 2 * 32, 254 + i / 2 * 32, 32, 32)
            self.colors_rect.append(rect)

        self.pens = [
                pygame.image.load("./images/pen1.png").convert_alpha(),
                pygame.image.load("./images/pen2.png").convert_alpha()
        ]
        # 设置出笔
        self.pens_rect = []
        for (i, img) in enumerate(self.pens):
            rect = pygame.Rect(10, 10 + i * 64, 64, 64)
            self.pens_rect.append(rect)

        self.sizes = [
                pygame.image.load("./images/big.png").convert_alpha(),
                pygame.image.load("./images/small.png").convert_alpha()
        ]
        # 设置调整大小加减号
        self.sizes_rect = []
        for (i, img) in enumerate(self.sizes):
            rect = pygame.Rect(10 + i * 32, 138, 32, 32)
            self.sizes_rect.append(rect)

    def set_brush(self, brush):
        self.brush = brush
    # 画出所有菜单栏
    def draw(self):
        for (i, img) in enumerate(self.pens):
            self.screen.blit(img, self.pens_rect[i].topleft)
        for (i, img) in enumerate(self.sizes):
            self.screen.blit(img, self.sizes_rect[i].topleft)
            # draw current pen / color
        self.screen.fill((255, 255, 255), (10, 180, 64, 64))
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 180, 64, 64), 1)
        size = self.brush.get_size()
        x = 10 + 32
        y = 180 + 32
        if self.brush.get_brush_style():
            x = x - size
            y = y - size
            self.screen.blit(self.brush.get_current_brush(), (x, y))
        else:
            pygame.draw.circle(self.screen, self.brush.get_color(), (x, y), size)
        # draw colors panel
        for (i, rgb) in enumerate(self.colors):
            pygame.draw.rect(self.screen, rgb, self.colors_rect[i])
    # 实现按键功能化
    def click_button(self, pos):
        # pen buttons
        for (i, rect) in enumerate(self.pens_rect):
            # 如果给定的点位于矩形内，则返回true。 沿着右边缘或底部边缘的点不被认为是在矩形内部。
            if rect.collidepoint(pos):
                # 确认点击后设定刷子类型
                self.brush.set_brush_style(bool(i))
                return True
        # size buttons
        for (i, rect) in enumerate(self.sizes_rect):
            if rect.collidepoint(pos):
                # self.brush.set_size(self.brush.get_size() - 0.5)
                # else:
                    # self.brush.set_size(self.brush.get_size() + 0.5)
                if i:  # i == 1, size down
                    self.brush.set_size(self.brush.get_size() - 1)
                else:
                    self.brush.set_size(self.brush.get_size() + 1)
                return True
        # color buttons
        for (i, rect) in enumerate(self.colors_rect):
            # 如果鼠标点击了这个矩形，则为True
            if rect.collidepoint(pos):
                # 设置刷子的颜色
                self.brush.set_color(self.colors[i])
                return True
        return False

class Painter(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Painter")
        self.clock = pygame.time.Clock()
        self.brush = Brush(self.screen)
        self.menu = Menu(self.screen)
        self.menu.set_brush(self.brush)

    def run(self):
        self.screen.fill((255, 255, 255))
        while True:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.screen.fill((255, 255, 255))
                elif event.type == MOUSEBUTTONDOWN:
                    # <= 74, coarse judge here can save much time
                    if ((event.pos)[0] <= 74 and self.menu.click_button(event.pos)):
                        # if not click on a functional button, do drawing
                        pass
                    else:
                        self.brush.start_draw(event.pos)

                elif event.type == MOUSEMOTION:
                    self.brush.draw(event.pos)
                elif event.type == MOUSEBUTTONUP:
                    self.brush.end_draw()
            self.menu.draw()
            pygame.display.update()

if __name__ == '__main__':
    app = Painter()
    app.run()

