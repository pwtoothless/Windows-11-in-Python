import pygame
import json

with open('settings.json') as f:
    settings = json.load(f)
SCREEN_WIDTH = settings.get("screen_width", 1000)
SCREEN_HEIGHT = settings.get("screen_height", 720)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

class PaintApp:
    def __init__(self, name, width, height, rounded_corners_radius):
        self.name = name
        self.width = width
        self.height = height
        self.rounded_corners_radius = rounded_corners_radius
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.minimized = False
        self.maximized = False
        self.dragging = False
        self.closed = False
        self.offset = (0, 0)
        self.surface = pygame.Surface((800, 600))
        self.surface.fill((255, 255, 255))  # Example background color
        self.rect = self.surface.get_rect()
        # Control buttons (close, maximize, minimize)
        self.close_button = pygame.Rect(self.width - 30, 0, 30, 30)
        self.maximize_button = pygame.Rect(self.width - 60, 0, 30, 30)
        self.minimize_button = pygame.Rect(self.width - 90, 0, 30, 30)

    def draw(self, screen):
        if self.closed:
            return
        pygame.draw.rect(self.surface, (255, 255, 255), self.surface.get_rect(), border_radius=self.rounded_corners_radius)
        screen.blit(self.surface, self.rect.topleft)

        # Draw control buttons
        pygame.draw.rect(self.surface, (255, 0, 0), self.close_button)       # Close
        pygame.draw.rect(self.surface, (0, 255, 0), self.maximize_button)    # Maximize
        pygame.draw.rect(self.surface, (0, 0, 255), self.minimize_button)    # Minimize


    def handle_events(self, event):
        pass  # Handle events specific to Paint App window
        if self.closed:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.close_button.collidepoint(event.pos):
                    self.closed = True  # Close the app
                elif self.maximize_button.collidepoint(event.pos):
                    if not self.maximized:                        
                        self.maximize()                    
                    else:
                        self.restore_normal()
                elif self.minimize_button.collidepoint(event.pos):
                    self.minimize()
                elif self.rect.collidepoint(event.pos):
                    if event.pos[1] < self.rect.top + 30:  # Title bar
                        self.dragging = True
                        mouse_x, mouse_y = event.pos
                        self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset[0]
            self.rect.y = mouse_y + self.offset[1]

    def minimize(self):
        self.minimized = True

    def restore(self):
        self.minimized = False

    def maximize(self):
        self.maximized = True
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

    def restore_normal(self):
        self.maximized = False
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.rect.center)