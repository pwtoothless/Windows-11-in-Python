import json
import os
import threading
from datetime import datetime
import ntplib

# import ntplib
import pygame
import pytz
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Read settings from JSON file
with open('settings.json') as f:
    settings = json.load(f)

# Set up the screen using values from settings.json
SCREEN_WIDTH = settings.get("screen_width", 1280)
SCREEN_HEIGHT = settings.get("screen_height", 720)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Windows 11 Simulation")

# Load Windows 11 default wallpaper
background = pygame.image.load(settings['wallpaper'])
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 120, 215)

# Font
font = pygame.font.Font(None, 24)

# List to store app windows
app_windows = []

class AppWindow:
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
        self.offset = (0, 0)

    def draw(self, screen):
        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), border_radius=self.rounded_corners_radius)
        screen.blit(self.surface, self.rect.topleft)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                if event.pos[1] < self.rect.top + 30:
                    self.dragging = True
                    mouse_x, mouse_y = event.pos
                    self.offset = (self.rect.x - mouse_x, self.rect.y - mouse_y)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            mouse_x, mouse_y = event.pos
            self.rect.x = mouse_x + self.offset[0]
            self.rect.y = mouse_y + self.offset[1]

    def minimize(self):
        self.minimized = True
        self.surface.fill((200, 200, 200, 0))

    def restore(self):
        self.minimized = False
        self.surface.fill((255, 255, 255, 255))

    def maximize(self):
        self.maximized = True
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()

    def restore_normal(self):
        self.maximized = False
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect(center=self.rect.center)

class FileExplorer(AppWindow):
    def __init__(self):
        super().__init__("File Explorer", 600, 400, settings["file_explorer"]["rounded_corners_radius"])
        self.current_path = settings["file_explorer"]["current_path"]

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(self.surface, GRAY, (0, 0, self.width, 30), border_radius=self.rounded_corners_radius)
        title_text = font.render(self.name, True, BLACK)
        screen.blit(title_text, (self.rect.left + 10, self.rect.top + 5))

    def open(self):
        os.system('python file_explorer.py')

class WebBrowser(AppWindow):
    def __init__(self):
        super().__init__("Web Browser", 800, 600, settings["web_browser"]["rounded_corners_radius"])

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(self.surface, GRAY, (0, 0, self.width, 30), border_radius=self.rounded_corners_radius)
        title_text = font.render(self.name, True, BLACK)
        screen.blit(title_text, (self.rect.left + 10, self.rect.top + 5))

    def open(self):
        os.system('python web_browser.py')

class PaintApp(AppWindow):
    def __init__(self):
        super().__init__("Paint", 800, 600, settings["paint_app"]["rounded_corners_radius"])

    def draw(self, screen):
        super().draw(screen)
        pygame.draw.rect(self.surface, GRAY, (0, 0, self.width, 30), border_radius=self.rounded_corners_radius)
        title_text = font.render(self.name, True, BLACK)
        screen.blit(title_text, (self.rect.left + 10, self.rect.top + 5))

    def open(self):
        os.system('python paint_app.py')

class StartMenu(AppWindow):
    def __init__(self):
        super().__init__("Start Menu", 400, 400, settings["start_menu"]["rounded_corners_radius"])
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - self.height - settings["taskbar_thickness"]
        self.visible = False
        self.start_icon = pygame.image.load(settings["start_menu"]["icon"]).convert_alpha()
        self.start_icon = pygame.transform.scale(self.start_icon, (30, 30))
        self.icon_rect = pygame.Rect((SCREEN_WIDTH - 30) // 2, SCREEN_HEIGHT - settings["taskbar_thickness"], 30, 30)

        # Load icons
        self.icons = {
            "File Explorer": pygame.image.load(settings["file_explorer"]["icon"]),
            "Web Browser": pygame.image.load(settings["web_browser"]["icon"]),
            "Paint": pygame.image.load(settings["paint_app"]["icon"])
        }

        # Resize icons
        for key in self.icons:
            self.icons[key] = pygame.transform.scale(self.icons[key], (64, 64))

    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(self.surface, WHITE, self.surface.get_rect(), border_radius=self.rounded_corners_radius)
            screen.blit(self.surface, self.rect.topleft)

            # Draw icons and names
            items = ["File Explorer", "Web Browser", "Paint"]
            for i, item in enumerate(items):
                screen.blit(self.icons[item], (self.rect.left + 20, self.rect.top + 20 + i * 100))
                item_text = font.render(item, True, BLACK)
                screen.blit(item_text, (self.rect.left + 100, self.rect.top + 50 + i * 100))

    def toggle_visibility(self):
        self.visible = not self.visible

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                if self.icon_rect.collidepoint(event.pos):
                    self.toggle_visibility()
                elif self.visible:
                    for i, item in enumerate(self.icons):
                        icon_rect = pygame.Rect(self.rect.left + 20, self.rect.top + 20 + i * 100, 64, 64)
                        if icon_rect.collidepoint(event.pos):
                            self.launch_app(item)
                            self.visible = False

    def launch_app(self, app_name):
        if app_name == "File Explorer":
            app_windows.append(FileExplorer())
        elif app_name == "Web Browser":
            app_windows.append(WebBrowser())
        elif app_name == "Paint":
            app_windows.append(PaintApp())

# Taskbar class
class Taskbar:
    def __init__(self):
        self.height = settings["taskbar_thickness"]
        self.surface = pygame.Surface((SCREEN_WIDTH, self.height))
        self.rect = self.surface.get_rect()
        self.rect.bottomleft = (0, SCREEN_HEIGHT)

    def draw(self, screen, current_time, start_menu):
        pygame.draw.rect(self.surface, WHITE, self.surface.get_rect())
        screen.blit(self.surface, self.rect.topleft)

        time_text = font.render(current_time, True, BLACK)
        screen.blit(time_text, (SCREEN_WIDTH - 150, SCREEN_HEIGHT - self.height + 10))

        # Draw start menu icon
        screen.blit(start_menu.start_icon, start_menu.icon_rect.topleft)

    def handle_events(self, event):
        pass

# Function to get the current time
def get_current_time():
    now = datetime.now(pytz.timezone(settings['timezone']))
    if settings['time_format'] == '12':
        return now.strftime('%I:%M:%S %p')
    else:
        return now.strftime('%H:%M:%S')

# Function to synchronize time with NTP
 #def sync_time_with_ntp():
    try:
        client = ntplib.NTPClient()
        response = client.request('time.google.com', version=3)
        t = datetime.fromtimestamp(response.tx_time, pytz.utc)
        # Store time in a variable instead of using sudo
        return t.strftime('%Y-%m-%d %H:%M:%S')
    except Exception as e:
        print(f"Error synchronizing time: {e}")
        return None

# Main loop
def main():
    start_menu = StartMenu()
    taskbar = Taskbar()
    clock = pygame.time.Clock()
    running = True

    # Initialize time variable
    current_time = get_current_time()
    # Start a thread to sync time periodically
    #sync_time_thread = threading.Thread(target=sync_time_with_ntp)
    #sync_time_thread.start()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            start_menu.handle_events(event)

            for app_window in app_windows:
                app_window.handle_events(event)

        screen.blit(background, (0, 0))

        # Update current time from the NTP sync
        #current_time = sync_time_with_ntp() or current_time  # Use current_time if sync fails

        # Draw app windows
        for app_window in app_windows:
            app_window.draw(screen)

        # Draw taskbar
        taskbar.draw(screen, current_time, start_menu)

        # Draw start menu
        start_menu.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
