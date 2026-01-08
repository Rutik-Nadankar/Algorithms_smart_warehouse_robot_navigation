import pygame, os, random
from agents.bfs import bfs
from agents.astar import astar
from environment.warehouse import Warehouse

CELL = 60
ROWS, COLS = 10, 10

# Right panel for buttons
RIGHT_PANEL_WIDTH = 200
BUTTON_HEIGHT = 40
BUTTON_SPACING = 20

RESULT_HEIGHT = 100  # Height of result area below grid

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "images")

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,200,0)
RED = (200,0,0)
BLUE = (50,50,255)

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = (229, 231, 235)
        self.border_color = (17, 24, 39)
        self.hover_color = (209, 213, 219)
        self.border_radius = 8

    def draw(self, screen, font):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=self.border_radius)
        txt_surf = font.render(self.text, True, self.border_color)
        screen.blit(txt_surf, txt_surf.get_rect(center=self.rect.center))

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

class WarehouseGUI:
    def __init__(self):
        pygame.init()
        # total height = grid + result area
        self.width = COLS*CELL + RIGHT_PANEL_WIDTH
        self.height = ROWS*CELL + RESULT_HEIGHT
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Smart Warehouse AI")
        self.font = pygame.font.SysFont(None, 28)

        # Load images
        self.robot = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG,"robot.png")), (CELL,CELL))
        self.shelf = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG,"shelf.png")), (CELL,CELL))
        self.floor = pygame.transform.scale(
            pygame.image.load(os.path.join(IMG,"floor.png")), (CELL,CELL))

        self.create_buttons()
        self.grid = Warehouse(ROWS, COLS)
        self.reset()

        # Results storage
        self.result_astar = None
        self.result_bfs = None
        self.final_result = ""
        self.info = ""

    def create_buttons(self):
        x = COLS*CELL + 30
        y = 20
        self.btn_astar = Button(x, y, RIGHT_PANEL_WIDTH-60, BUTTON_HEIGHT, "Run A*")
        self.btn_bfs = Button(x, y + BUTTON_HEIGHT + BUTTON_SPACING, RIGHT_PANEL_WIDTH-60, BUTTON_HEIGHT, "Run BFS")
        self.btn_shuffle = Button(x, y + 2*(BUTTON_HEIGHT + BUTTON_SPACING), RIGHT_PANEL_WIDTH-60, BUTTON_HEIGHT, "Shuffle")
        self.btn_reset = Button(x, y + 3*(BUTTON_HEIGHT + BUTTON_SPACING), RIGHT_PANEL_WIDTH-60, BUTTON_HEIGHT, "Restart")

    def reset(self):
        self.start = None
        self.end = None
        self.path = []
        self.robot_pos = None
        self.result_astar = None
        self.result_bfs = None
        self.final_result = ""
        self.info = ""

    def draw_grid(self):
        # Draw floor
        for r in range(ROWS):
            for c in range(COLS):
                self.screen.blit(self.floor,(c*CELL,r*CELL))

        # Draw shelves
        for r,c in self.grid.shelves:
            self.screen.blit(self.shelf,(c*CELL,r*CELL))

        # Start/end highlights
        if self.start:
            pygame.draw.rect(self.screen,GREEN,(self.start[1]*CELL,self.start[0]*CELL,CELL,CELL),3)
        if self.end:
            pygame.draw.rect(self.screen,RED,(self.end[1]*CELL,self.end[0]*CELL,CELL,CELL),3)

        # Path
        for r,c in self.path:
            s = pygame.Surface((CELL,CELL), pygame.SRCALPHA)
            pygame.draw.circle(s, (59,130,246,180), (CELL//2,CELL//2), 8)
            self.screen.blit(s, (c*CELL,r*CELL))

        # Robot
        if self.robot_pos:
            self.screen.blit(self.robot,(self.robot_pos[1]*CELL,self.robot_pos[0]*CELL))

    def draw_ui(self):
        # Draw buttons
        self.btn_astar.draw(self.screen,self.font)
        self.btn_bfs.draw(self.screen,self.font)
        self.btn_shuffle.draw(self.screen,self.font)
        self.btn_reset.draw(self.screen,self.font)

        # Draw result panel below grid
        panel_y = ROWS*CELL
        panel_height = RESULT_HEIGHT
        pygame.draw.rect(self.screen, (245,245,245), (0, panel_y, COLS*CELL, panel_height))
        pygame.draw.rect(self.screen, (17,24,39), (0, panel_y, COLS*CELL, panel_height), 2)

        y = panel_y + 10
        x = 10
        if self.result_astar:
            txt = self.font.render(f"A* explored: {self.result_astar['explored']}, Steps: {self.result_astar['steps']}", True, (17,24,39))
            self.screen.blit(txt, (x, y))
            y += 25
        if self.result_bfs:
            txt = self.font.render(f"BFS explored: {self.result_bfs['explored']}, Steps: {self.result_bfs['steps']}", True, (17,24,39))
            self.screen.blit(txt, (x, y))
            y += 25
        if self.final_result:
            txt = self.font.render(self.final_result, True, (200,50,50))
            self.screen.blit(txt, (x, y))
            y += 25
        if self.info:
            txt = self.font.render(self.info, True, (200,50,50))
            self.screen.blit(txt, (x, y))

    def run_algorithm(self, algo):
        if not self.start or not self.end:
            self.info = "Set start and end points!"
            return

        self.info = ""

        if algo == "A*":
            path, explored = astar(self.start, self.end, self.grid)
            if not path or path[0] != self.start:
                self.info = "Sorry, location unreachable!"
                self.path = []
                self.robot_pos = self.start
                self.result_astar = None
                return
            self.result_astar = {'explored': explored, 'steps': len(path)}
        else:
            path, explored = bfs(self.start, self.end, self.grid)
            if not path or path[0] != self.start:
                self.info = "Sorry, location unreachable!"
                self.path = []
                self.robot_pos = self.start
                self.result_bfs = None
                return
            self.result_bfs = {'explored': explored, 'steps': len(path)}

        self.path = path
        self.animate(path)

        if self.result_astar and self.result_bfs:
            diff_steps = self.result_bfs['steps'] - self.result_astar['steps']
            diff_explored = self.result_bfs['explored'] - self.result_astar['explored']
            winner = "A*" if self.result_astar['steps'] <= self.result_bfs['steps'] else "BFS"
            self.final_result = f"{winner} is better! Step diff: {diff_steps}, Explored diff: {diff_explored}"

    def animate(self, path):
        for pos in path:
            self.robot_pos = pos
            self.draw()
            pygame.time.delay(200)

    def draw(self):
        self.screen.fill(WHITE)
        self.draw_grid()
        self.draw_ui()
        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.draw()
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                if e.type == pygame.MOUSEBUTTONDOWN:
                    x,y = e.pos

                    # Grid selection
                    if y < ROWS*CELL and x < COLS*CELL:
                        r,c = y//CELL, x//CELL
                        if not self.start and (r,c) not in self.grid.shelves:
                            self.start = (r,c)
                            self.robot_pos = (r,c)
                        elif not self.end and (r,c) not in self.grid.shelves:
                            self.end = (r,c)

                    # Buttons
                    if self.start and self.end:
                        if self.btn_astar.clicked((x,y)):
                            self.run_algorithm("A*")
                        if self.btn_bfs.clicked((x,y)):
                            self.run_algorithm("BFS")

                    if self.btn_shuffle.clicked((x,y)):
                        self.grid = Warehouse(ROWS,COLS)
                        self.start = None
                        self.end = None
                        self.robot_pos = None
                        self.path = []
                        self.result_astar = None
                        self.result_bfs = None
                        self.final_result = ""
                        self.info = "Warehouse shuffled!"

                    if self.btn_reset.clicked((x,y)):
                        self.reset()

            clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    WarehouseGUI().run()
