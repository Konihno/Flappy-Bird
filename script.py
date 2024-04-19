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

# Charger l'arrière-planbackground = 
 
pygame.image.load("/Users/nicolaslong/flappy-bird/flappy bird backgground.jpeg")

# Charger l'image de l'oiseau
bird_img = pygame.image.load("/Users/nicolaslong/flappy-bird/Flappy-Bird-PNG-File.png")
bird_img = pygame.transform.scale(bird_img, (50, 50))  # Redimensionner l'image de l'oiseau à une taille de 50x50 pixels

# Charger la police pour afficher le score
font = pygame.font.Font(None, 36)  # Définir la police par défaut pour le rendu du texte

# Charger la police pour afficher le message de fin
end_font = pygame.font.Font(None, 24)  # Redimensionner la police pour le message de fin

# Définir la variable font avant de l'utiliser dans la fonction draw_restart_button()
restart_button_text = font.render("Rejouer", True, BLACK)
restart_button_rect = restart_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

# Paramètres de l'oiseau
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_radius = 20
bird_angle = 0  # Nouvel attribut pour l'angle de rotation de l'oiseau
bird_rotation_speed = 5  # Vitesse de rotation de l'oiseau
rotation_direction = 0  # Direction de rotation de l'oiseau

# Définir la position initiale de l'oiseau après avoir défini les paramètres de l'oiseau
bird_rect = bird_img.get_rect(center=(bird_x, bird_y))

# Vitesse de chute de l'oiseau
bird_dy = 0

# Score initial
score = 0

# Meilleur score initial
best_score = 0

play_button_text = font.render("Jouer", True, BLACK)
play_button_rect = play_button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(50, SCREEN_HEIGHT - 300)  # Modifier la hauteur maximale des tuyaux
        self.top_pipe = pygame.Rect(self.x, 0, 50, self.height)
        self.bottom_pipe = pygame.Rect(self.x, self.height + 200, 50, SCREEN_HEIGHT)
        self.passed = False  # Initialiser l'attribut 'passed' à False

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
pygame.time.set_timer(SPAWNPIPE, 1700)  # Modifier la fréquence d'apparition des tuyaux

running = True

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return  # Quitter la fonction et passer au jeu

        # Afficher l'arrière-plan
        screen.blit(background, (0, 0))

        # Afficher le bouton "Jouer"
        screen.blit(play_button_text, play_button_rect)

        # Mettre à jour l'écran
        pygame.display.flip()

def main_game():
    global bird_dy, bird_angle, bird_y, score, pipes, bird_rect, best_score
    bird_dy = 0
    bird_angle = 0
    bird_y = SCREEN_HEIGHT // 2
    score = 0
    pipes = []

    game_over = False  # Initialiser la variable game_over en dehors de la boucle

    while running:  # Boucle principale du jeu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_dy = -5
                    bird_angle = 45  # Rotation de l'oiseau lorsqu'on appuie sur la touche d'espace
                    rotation_direction = 1  # Rotation vers le haut
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:  # Vérifier si le jeu est terminé et la souris a été cliquée
                if restart_button_rect.collidepoint(event.pos):
                    main_game()

            elif event.type == SPAWNPIPE and not game_over:  # Gérer l'événement de génération de nouveaux tuyaux uniquement lorsque le jeu est en cours
                new_pipe = Pipe(SCREEN_WIDTH)
                pipes.append(new_pipe)

        # Rotation de l'oiseau
        if bird_angle > 0:
            bird_angle -= bird_rotation_speed
        else:
            bird_angle = 0

        # Mouvement de l'oiseau
        bird_dy += 0.2
        bird_y += bird_dy
        bird_rect.centery = bird_y  # Mettre à jour la position de l'oiseau

        # Effacer l'écran
        screen.fill(WHITE)

        # Dessiner l'arrière-plan
        screen.blit(background, (0, 0))

        # Vérifier la collision entre l'oiseau et chaque tuyau
        for pipe in pipes:
            if pipe.collision():
                game_over = True
                break  # Sortir de la boucle dès qu'une collision est détectée

        if game_over:
            # Afficher le bouton "Rejouer"
            screen.blit(restart_button_text, restart_button_rect)
            # Afficher le message de fin avec le score
            end_text = end_font.render("Bravo ! Votre score est de " + str(score), True, BLACK)
            end_rect = end_text.get_rect(center=(SCREEN_WIDTH // 2, restart_button_rect.top - 30))
            screen.blit(end_text, end_rect)
            pygame.display.flip()  # Mettre à jour l'écran
            
            # Mise à jour du meilleur score si nécessaire
            if score > best_score:
                best_score = score

            continue  # Passer à la prochaine itération de la boucle

        # Dessiner l'oiseau en utilisant son image
        rotated_bird_img = pygame.transform.rotate(bird_img, bird_angle)  # Rotation de l'image de l'oiseau
        bird_rect = rotated_bird_img.get_rect(center=(bird_x, bird_y))
        screen.blit(rotated_bird_img, bird_rect)

        # Gérer les tuyaux
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x < -50:
                pipes.remove(pipe)

        # Gérer le score
        for pipe in pipes:
            if pipe.x + 50 < bird_x and not pipe.passed:  # Si le tuyau est passé par l'oiseau
                score += 1
                pipe.passed = True

        # Afficher le score
        score_text = font.render("Score: " + str(score), True, BLACK)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(score_text, score_rect)

        # Afficher le meilleur score
        best_score_text = font.render("Meilleur score: " + str(best_score), True, BLACK)
        best_score_rect = best_score_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(best_score_text, best_score_rect)

        # Mettre à jour l'écran
        pygame.display.flip()

        # Limiter la vitesse de la boucle
        pygame.time.Clock().tick(60)

        if game_over:
            break  # Si le jeu est terminé, sortir de la boucle principale

# Afficher l'écran de démarrage
start_screen()

# Démarrer le jeu une fois que le joueur clique sur le bouton "Jouer"
main_game()
