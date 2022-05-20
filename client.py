import pygame
from network import Network

WIDTH, HEIGHT = 500, 500
LEFT_BORDER, RIGHT_BORDER = 0, 500
TOP_BORDER, BOTTOM_BORDER = 0, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


clientNumber = 0

# RGB COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
MAGENTA = (255, 0, 255)
TEAL = (0, 128, 128)


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        # self.rect = (x, y, width, height)
        self.rect = pygame.Rect(x, y, width, height)
        self.vel = 3

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.color, self.rect)

    def jump(self):
        # TODO implement jumping
        self.jumping = False
        self.falling = 0

    def move(self, players):
        keys = pygame.key.get_pressed()
        players = players

        if keys[pygame.K_LEFT] and (self.x >= LEFT_BORDER + self.vel):
            self.x -= self.vel
            if self.check_collision(players):
                self.x += self.vel

        if keys[pygame.K_RIGHT] and (self.x <= RIGHT_BORDER - self.vel - self.width):
            self.x += self.vel
            if self.check_collision(players):
                self.x -= self.vel

        if keys[pygame.K_UP] and (self.y >= TOP_BORDER + self.vel):
            self.y -= self.vel
            if self.check_collision(players):
                self.y += self.vel

        if keys[pygame.K_DOWN] and (self.y < +BOTTOM_BORDER - self.vel - self.height):
            self.y += self.vel
            if self.check_collision(players):
                self.y -= self.vel

        self.update()

    def update(self):
        # self.rect = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def check_collision(self, players):
        self.update()

        if len(players) >= 1:
            for p in players.values():
                print(p)
                if pygame.Rect.colliderect(self.rect, p):
                    # if collision occur
                    return True
        else:
            return False


def redrawWindow(WIN, player, players):
    # WIN.fill((255, 255, 255))
    WIN.fill(TEAL)

    player.draw(WIN)

    for colorP in players:
        rect = players[colorP]
        pygame.draw.rect(WIN, colorP, rect)

    pygame.display.update()


def remove_player(players, player):
    for p in players:
        if p == player.color:
            players.pop(p)
            return players


def main():
    run = True
    connected = True

    # check connestion to server
    try:
        n = Network()
        color = n.getPos()
    except Exception as e:
        print(e)
    else:
        connected = False
        players_dict = {}
        color = RED

    player = Player(0, 0, 100, 100, color)
    players = []
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # things related to server
        if connected:
            # Send and receive player RECT objects to/from server
            players = n.send(player.rect)

            # handle server shutting down
            # TODO check
            #
            if not players:
                connected = False
                players_dict = {}
                break

            players_dict = remove_player(players, player)

        # run if not connecting to server
        else:
            pass  # TODO display server disconnected

        player.move(players_dict)
        redrawWindow(WIN, player, players_dict)

    # IF run loop ends
    pygame.quit()


# call main game start
main()
