import pygame

# --- Setup ---
pygame.init()
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

# Colors
colors = {
    "black": (0, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
    "red": (255, 0, 0),
    "pink": (255, 180, 180),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0)
}

# Maze and pellets
maze = [
    "1111111111",
    "1000000001",
    "1011110101",
    "1010000101",
    "1010110101",
    "1000000001",
    "1111111111"
]
pellets = [(x*60 + 30, y*60 + 30) for y, row in enumerate(maze) for x, block in enumerate(row) if block == "0"]

# --- Game Objects ---
class GameObject:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = 20
        self.rect = pygame.Rect(x - self.size, y - self.size, self.size * 2, self.size * 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

    def move(self, dx, dy):
        new_x = self.x + dx * 30
        new_y = self.y + dy * 30

        # Check for boundaries within the window
        if not (0 <= new_x < 600 and 0 <= new_y < 600):
            return

        # Calculate grid position for potential new location
        grid_x = new_x // 60
        grid_y = new_y // 60

        # Check if the new position is within a wall or outside maze boundaries
        if maze[grid_y][grid_x] == '1':
            return

        # Update position and rectangle if the move is valid
        self.x = new_x
        self.y = new_y
        self.rect.topleft = (new_x - self.size, new_y - self.size)

class Ghost(GameObject):
    def __init__(self, x, y, color, ai_type):
        super().__init__(x, y, color)
        self.ai_type = ai_type
        self.state = "Chase"
        self.target = None
        self.initial_position = (x, y)

    def update(self):
        if self.state == "Chase":
            self.move_towards_target()

    def move_towards_target(self):
        dx = dy = 0
        if abs(self.x - self.target[0]) > 30:
            if self.x < self.target[0]:
                dx = 1
            elif self.x > self.target[0]:
                dx = -1
        if abs(self.y - self.target[1]) > 30:
            if self.y < self.target[1]:
                dy = 1
            elif self.y > self.target[1]:
                dy = -1
        self.move(dx, dy)

# --- Game Logic ---
pacman = GameObject(90, 90, colors["yellow"])
ghosts = [
    Ghost(270, 270, colors["red"], "Blinky"),
    Ghost(270, 90, colors["pink"], "Pinky"),
    Ghost(90, 270, colors["cyan"], "Inky"),
    Ghost(90, 90, colors["orange"], "Clyde")
]
score = 0
lives = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type is pygame.KEYDOWN:
            if event.key == pygame.K_a:
                pacman.move(-1, 0)
            elif event.key == pygame.K_d:
                pacman.move(1, 0)
            elif event.key == pygame.K_w:
                pacman.move(0, -1)
            elif event.key == pygame.K_s:
                pacman.move(0, 1)

    # Update and draw ghosts
    for ghost in ghosts:
        ghost.target = (pacman.x, pacman.y)
        ghost.update()
        ghost.draw(screen)

    # Collision detection for pellets
    eaten_pellets = len(pellets)
    pellets = [pellet for pellet in pellets if not pacman.rect.collidepoint(pellet)]
    eaten_pellets -= len(pellets)
    score += 10 * eaten_pellets

    # Collision detection for ghosts
    for ghost in ghosts:
        if pacman.rect.colliderect(ghost.rect):
            lives -= 1
            pacman.x, pacman.y = 90, 90  # Reset positions
            pacman.rect.topleft = (90 - pacman.size, 90 - pacman.size)
            for ghost in ghosts:
                ghost.x, ghost.y = ghost.initial_position
                ghost.rect.topleft = (ghost.x - ghost.size, ghost.y - ghost.size)

    # Drawing
    screen.fill(colors["black"])
    for y, row in enumerate(maze):
        for x, block in enumerate(row):
            if block == "1":
                pygame.draw.rect(screen, colors["white"], (x*60, y*60, 60, 60))
    for pellet in pellets:
        pygame.draw.circle(screen, colors["white"], pellet, 5)
    pacman.draw(screen)

    # Display score and lives
    score_text = font.render(f"Score: {score}", True, colors["white"])
    lives_text = font.render(f"Lives: {lives}", True, colors["white"])
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 40))

    pygame.display.flip()
    clock.tick(30)  # Slower update for easier gameplay

# Game Over message
game_over_text = font.render("Game Over", True, colors["white"])
screen.blit(game_over_text, (250, 300))
pygame.display.flip()
pygame.time.delay(3000)  # Display for 3 seconds

pygame.quit()
