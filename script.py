import pygame
import sys
import random


pygame.init()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

background = pygame.image.load("/Users/nicolaslong/flappy-bird/flappy bird backgground.jpeg")


pygame.display.set_caption("Flappy Bird")

pygame.image.load("/Users/nicolaslong/flappy-bird/flappy bird backgground.jpeg")

bird_img = pygame.image.load("/Users/nicolaslong/flappy-bird/Flappy-Bird-PNG-File.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))  

font = pygame.font.Font(None, 36)  

end_font = pygame.font.Font(None, 24)  

restart_button_text = font.render("Rejouer", True, BLACK)
restart_button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_radius = 20
bird_angle = 0  
bird_rotation_speed = 5  
rotation_direction = 0  

bird_rect = bird_img.get_rect(center=(bird_x, bird_y))

bird_dy = 0

score = 0

best_score = 0

play_button_text = font.render("Jouer", True, BLACK)
play_button_rect = play_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - 300)  
        self.top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + 200, 50, SCREEN_HEIGHT)
        self.passed = False

    def move(self):
        self.x -= 2
        self.top_pipe.x -= 2
        self.bottom_pipe.x -= 2

    def draw(self):
        pygame.draw.rect(screen, (0, 255, 0), self.top_pipe)
        pygame.draw.rect(screen, (0, 255, 0), self.bottom_pipe)

    def collision(self):
        if self.top_pipe.colliderect(bird_rect) or self.bottom_pipe.colliderect(bird_rect):
            return True
        return False

pipes = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1700)  

running = True

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return 

        screen.blit(background, (0, 0))

        screen.blit(play_button_text, play_button_rect)

        pygame.display.flip()

def main_game():
    global bird_dy, bird_angle, bird_y, score, pipes, bird_rect, best_score
    bird_dy = 0
    bird_angle = 0
    bird_y = SCREEN_HEIGHT // 2
    score = 0
    pipes = []

    game_over = False  

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_dy = -5
                    bird_angle = 45  
                    rotation_direction = 1  
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:  
                if restart_button_rect.collidepoint(event.pos):
                    main_game()

            elif event.type == SPAWNPIPE and not game_over: 
                new_pipe = Pipe(SCREEN_WIDTH)
                pipes.append(new_pipe)

        if bird_angle > 0:
            bird_angle -= bird_rotation_speed
        else:
            bird_angle = 0

        bird_dy += 0.2
        bird_y += bird_dy
        bird_rect.centery = bird_y 

        screen.fill(WHITE)

        screen.blit(background, (0, 0))

        for pipe in pipes:
            if pipe.collision():
                game_over = True
                break 

        if game_over:
        
            screen.blit(restart_button_text, restart_button_rect)
            
            end_text = end_font.render("Bravo ! Votre score est de " + str(score), True, BLACK)
            end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, restart_button_rect.top - 30))
            screen.blit(end_text, end_rect)
            pygame.display.flip()  
            
            if score > best_score:
                best_score = score

            continue 

    
        rotated_bird_img = pygame.transform.rotate(bird_img, bird_angle)  
        bird_rect = rotated_bird_img.get_rect(center=(bird_x, bird_y))
        screen.blit(rotated_bird_img, bird_rect)

        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x < -50:
                pipes.remove(pipe)

      
        for pipe in pipes:
            if pipe.x + 50 < bird_x and not pipe.passed:  
                score += 1
                pipe.passed = True

     
        score_text = font.render("Score: " + str(score), True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, score_rect)


        best_score_text = font.render("Meilleur score: " + str(best_score), True, BLACK)
        best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(best_score_text, best_score_rect)

       
        pygame.display.flip()

   
        pygame.time.Clock().tick(60)

        if game_over:
            break  

start_screen()

main_game()
