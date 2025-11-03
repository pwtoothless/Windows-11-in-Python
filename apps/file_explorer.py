import pygame
import sys

# Define colors
WHITE = (255, 255, 255)
LIGHT_GREY = (200, 200, 200)
DARK_GREY = (100, 100, 100)
BLUE = (0, 120, 215)

# Define window size
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

class FileExplorer:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('File Explorer')

        # Create a surface for the sidebar
        self.sidebar_surface = pygame.Surface((200, WINDOW_HEIGHT))
        self.sidebar_surface.fill(LIGHT_GREY)
        self.sidebar_rect = self.sidebar_surface.get_rect(topleft=(0, 0))

        # Create a surface for the file display area
        self.file_display_surface = pygame.Surface((WINDOW_WIDTH - 200, WINDOW_HEIGHT))
        self.file_display_surface.fill(WHITE)
        self.file_display_rect = self.file_display_surface.get_rect(topleft=(200, 0))

    def draw(self):
        # Draw the sidebar
        self.screen.blit(self.sidebar_surface, self.sidebar_rect.topleft)

        # Draw the file display area
        self.screen.blit(self.file_display_surface, self.file_display_rect.topleft)

        # Example of drawing text in the sidebar
        font = pygame.font.Font(None, 36)
        text_surface = font.render('This PC', True, DARK_GREY)
        self.screen.blit(text_surface, (20, 20))

        # Example of drawing files in the file display area
        for i in range(5):
            pygame.draw.rect(self.screen, LIGHT_GREY, (220, 50 + i * 60, 560, 50))
            file_text = font.render(f'File {i+1}', True, DARK_GREY)
            self.screen.blit(file_text, (230, 60 + i * 60))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.handle_click(event.pos)

    def handle_click(self, pos):
        if self.sidebar_rect.collidepoint(pos):
            print('Clicked in sidebar')
        elif self.file_display_rect.collidepoint(pos):
            print('Clicked in file display area')

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            pygame.display.update()

if __name__ == '__main__':
    explorer = FileExplorer()
    explorer.run()
