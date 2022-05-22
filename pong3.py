import random

import pygame
import sys

# Inicialização
pygame.init()

# Configurando a janela
screenWidth = 1280
screenHeight = 960
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Pong')
FONT = pygame.font.match_font('arial')
FONT_SIZE = 30
FPS = 60


# Classes
class Entity:
    def update(self, dt):
        pass


class Physics:
    def update(self, world, dt):
        pass


class Graphics:
    def draw(self, world):
        pass


class Referee:
    def __init__(self):
        self.player_score = 0
        self.opponent_score = 0
        self.draw_score()

    def update(self):
        self.draw_score()

    def player_scores(self):
        self.player_score += 1
        self.draw_score()

    def opponent_scores(self):
        self.opponent_score += 1
        self.draw_score()

    def draw_score(self):
        # pontuação do jogador
        FONTa = pygame.font.SysFont("arial", FONT_SIZE)
        ptext = FONTa.render(str(self.player_score), False, (240, 240, 240))
        ptext_rect = ptext.get_rect()
        ptext_rect.midtop = ((screenWidth / 2) + 200, 50)
        screen.blit(ptext, ptext_rect)
        # pontuação do oponente
        FONTb = pygame.font.SysFont("arial", FONT_SIZE)
        otext = FONTb.render(str(self.opponent_score), False, (240, 240, 240))
        otext_rect = otext.get_rect()
        otext_rect.midtop = ((screenWidth / 2) - 200, 50)
        screen.blit(otext, otext_rect)

        pygame.display.flip()


class Menu:
    def __init__(self):
        # menu loop
        self.playing = True
        self.show_start_screen()
        pygame.display.flip()
        while self.playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    self.playing = False
            pygame.time.Clock().tick(FPS)

    def show_start_screen(self):
        FONTa = pygame.font.SysFont("arial", 300)
        ptext = FONTa.render("PONG", False, (240, 240, 240))
        ptext_rect = ptext.get_rect()
        ptext_rect.midtop = ((screenWidth / 2), 200)
        screen.blit(ptext, ptext_rect)

        FONTb = pygame.font.SysFont("arial", 30)
        ptext = FONTb.render("Pressione qualquer tecla para começar", False, (240, 240, 240))
        ptext_rect = ptext.get_rect()
        ptext_rect.midtop = ((screenWidth / 2), 800)
        screen.blit(ptext, ptext_rect)


class BallPhysics(Physics):
    def update(self, world, dt):
        world.ball.body.x = world.ball.body.x + world.ball.speedX * dt
        world.ball.body.y = world.ball.body.y + world.ball.speedY * dt
        if world.ball.body.top <= 0 or world.ball.body.bottom >= screenHeight:
            world.ball.speedY = -world.ball.speedY
        if world.ball.body.right < 0:
            world.referee.player_scores()
            self.reset(world)
        if world.ball.body.left > screenWidth:
            world.referee.opponent_scores()
            self.reset(world)

    def reset(self, world):
        world.ball.body.center = (screenWidth / 2, screenHeight / 2)
        world.ball.speedX = random.choice((-0.5, 0.5))


class BallGraphics(Graphics):
    def draw(self, world):
        pygame.draw.ellipse(screen, (200, 200, 200), world.ball.body)


class PlayerPhysics(Physics):
    def update(self, world, dt):
        if world.ball.body.bottom >= world.player.body.top and world.ball.body.top <= world.player.body.bottom and \
                world.ball.body.right >= world.player.body.left:
            delta = world.ball.body.centery - world.player.body.centery
            world.ball.speedY = delta * 0.01
            world.ball.speedX *= -1
        (x, y) = pygame.mouse.get_pos()
        world.player.body.y = y - 70


class PlayerGraphics(Graphics):
    def draw(self, world):
        pygame.draw.rect(screen, (200, 200, 200), world.player.body)


class OpponentPhysics(Physics):
    def update(self, world, dt):
        if world.opponent.body.bottom < world.ball.body.y:
            world.opponent.body.bottom += world.opponent.speed
        if world.opponent.body.top > world.ball.body.y:
            world.opponent.body.top -= world.opponent.speed
        if world.ball.body.bottom >= world.opponent.body.top and world.ball.body.top <= world.opponent.body.bottom and world.ball.body.left <= world.opponent.body.right:
            delta = world.ball.body.centery - world.opponent.body.centery
            world.ball.speedY = delta * 0.01
            world.ball.speedX *= -1


class OpponentGraphics(Graphics):
    def draw(self, world):
        pygame.draw.rect(screen, (200, 200, 200), world.opponent.body)


class Ball(Entity):
    def __init__(self, physics, graphics):
        self.physics = physics
        self.graphics = graphics
        self.body = pygame.Rect(screenWidth / 2 - 15, screenHeight / 2 - 15, 30, 30)
        self.speedX = 0.4
        self.speedY = 0.4


class Player(Entity):
    def __init__(self, physics, graphics):
        self.physics = physics
        self.graphics = graphics
        self.body = pygame.Rect(screenWidth - 20, screenHeight / 2 - 70, 10, 140)


class Opponent(Entity):
    def __init__(self, physics, graphics):
        self.physics = physics
        self.graphics = graphics
        self.body = pygame.Rect(10, screenHeight / 2 - 70, 10, 140)
        self.speed = 8


class World:
    def __init__(self):
        bphysics = BallPhysics()
        bgraphics = BallGraphics()
        self.ball = Ball(bphysics, bgraphics)

        Pphysics = PlayerPhysics()
        pgraphics = PlayerGraphics()
        self.player = Player(Pphysics, pgraphics)

        Ophysics = OpponentPhysics()
        ographics = OpponentGraphics()
        self.opponent = Opponent(Ophysics, ographics)

        self.referee = Referee()


def inputs():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Objetos
menu = Menu()
world = World()
entities = [world.ball, world.player, world.opponent]

previous = pygame.time.get_ticks()
lag = 0
MS_PER_UPDATE = 1000 / FPS
while True:
    current = pygame.time.get_ticks()
    elapsed = current - previous
    previous = current
    lag += elapsed
    # Entradas
    inputs()
    # Atualização
    while lag >= MS_PER_UPDATE:
        # Atualização
        for e in entities:
            e.physics.update(world, MS_PER_UPDATE)
        lag -= MS_PER_UPDATE
    # Desenho
    screen.fill((0, 0, 0))
    for e in entities:
        e.graphics.draw(world)
    world.referee.update()
    pygame.display.flip()

