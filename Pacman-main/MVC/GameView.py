import pygame
from MVC.Controller import Controller


class GameView:
    """
       Clase encargada de gestionar la visualización y la interacción del usuario con el juego.
       Se encarga de la representación del estado del juego en la pantalla, la recepción de entradas del jugador
       y la actualización del juego de acuerdo con los eventos y las acciones.

       Atributos:
       - model: El modelo del juego que contiene la lógica y el estado del juego.
       - controller: El controlador que maneja las acciones del jugador.
       - screen: La ventana donde se dibujarán los elementos del juego.
       - clock: Controla la velocidad del juego (FPS).
       - font: Fuente principal utilizada para mostrar texto en la pantalla.
       - font_small: Fuente más pequeña utilizada para mensajes de texto secundarios.
       - font_extra_small: Fuente aún más pequeña para instrucciones u otros mensajes.
       - mode_timer: Temporizador para gestionar la duración de los modos de los fantasmas (persecución/dispersión).
       - chase_duration: Duración del modo de persecución de los fantasmas.
       - scatter_duration: Duración del modo de dispersión de los fantasmas.
       - frightened_time: Temporizador para gestionar el modo de asustado de los fantasmas.
       - frightened_duration: Duración del modo de asustado de los fantasmas.
       - current_mode: Modo actual de los fantasmas ('scatter' o 'chase').
       - previous_lives: Número de vidas anteriores del jugador.
       - score_guardado: Puntuación guardada.
       - vidas_guardadas: Vidas guardadas.
    """
    def __init__(self, model, controller):

        """
            Inicializa la vista del juego.

            :param model: El modelo del juego que contiene la lógica y el estado del juego.
            :param controller: El controlador que maneja las acciones del jugador.
        """
        self.model = model
        self.controller = controller
        self.screen = pygame.display.set_mode((558, 680))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("Utilitarios/PressStart2P-Regular.ttf", 50)
        self.font_small = pygame.font.Font("Utilitarios/PressStart2P-Regular.ttf", 30)
        self.font_extra_small = pygame.font.Font("Utilitarios/PressStart2P-Regular.ttf", 20)

        self.mode_timer = 0
        self.chase_duration = 15
        self.scatter_duration = 7
        self.frightened_time = 0
        self.frightened_duration = 10
        self.current_mode = 'scatter'

        self.previous_lives = self.model.getCurrentPlayer().vidas
        self.score_guardado = 0
        self.vidas_guardadas = 0

    def draw_ready_message(self):
        """
         Dibuja el mensaje de "Ready!" en la pantalla, junto con instrucciones compactas.
        """
        ready_text = self.font_small.render('Ready!', True, "yellow")
        instruction_text = self.font_extra_small.render('G = guardar, L = cargar', True, "yellow")

        ready_rect = ready_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 20))
        self.screen.blit(ready_text, ready_rect)

        instruction_rect = instruction_text.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2 + 20))
        self.screen.blit(instruction_text, instruction_rect)

        pygame.display.flip()

    def draw_game_over_message(self):
        """
         HECHO POR IA
        Dibuja el mensaje de "Game Over!" en la pantalla cuando el jugador pierde todas las vidas.
        """
        game_over_text = self.font.render('Game Over!', True, "red")
        text_rect = game_over_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(game_over_text, text_rect)

    def draw_win_message(self):
        """
         HECHO POR IA
         Dibuja el mensaje de "You Win!" en la pantalla cuando el jugador gana el juego.
        """
        win_text = self.font.render('You Win!', True, "green")
        text_rect = win_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(win_text, text_rect)

    def show_save_screen(self):

        """
         HECHO POR IA
         Muestra la pantalla de guardado, indicando que el progreso del juego ha sido guardado.
        """
        save_screen = pygame.display.set_mode((558, 680))
        save_screen.fill((0, 0, 0))

        save_text = self.font_small.render('Juego guardado!', True, "white")
        text_rect = save_text.get_rect(center=(save_screen.get_width() // 2, save_screen.get_height() // 2))
        save_screen.blit(save_text, text_rect)

        pygame.display.flip()
        pygame.time.delay(2000)

        self.screen = pygame.display.set_mode((558, 680))

    def show_load_screen(self):
        """
         HECHO POR IA
         Muestra la pantalla de carga, indicando que el progreso del juego está siendo cargado.
        """
        load_screen = pygame.display.set_mode((558, 680))
        load_screen.fill((0, 0, 0))

        load_text = self.font_small.render('Cargar partida...', True, "white")
        text_rect = load_text.get_rect(center=(load_screen.get_width() // 2, load_screen.get_height() // 2))
        load_screen.blit(load_text, text_rect)

        pygame.display.flip()
        pygame.time.delay(2000)

        self.screen = pygame.display.set_mode((558, 680))

    def reset_level(self):
        self.model.pacdots_comidos = 0
        self.model.laberinto.score = 0
        self.model.reset_pacman()
        self.model.reset_ghosts()
        self.model.laberinto.crear_laberinto()
        self.model.laberinto.dibujar_laberinto(self.screen)
        self.model.laberinto.dibujar_misc(self.screen)
        self.model._inicializar_hash_colisiones()
        self.mode_timer = 0
        self.frightened_time = 0
        self.current_mode = 'scatter'

    def game_loop(self):
        running = True
        self.adjust_ghost_speed()
        self.model.setear_personajes()

        self.draw_ready_message()
        pygame.time.delay(5000)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_g:
                        self.model.laberinto.guardar_score_vidas(self.model, "ScoreGuardado.txt")
                        self.model.laberinto.guardar_mapa(self.model, "MapaGuardado.txt")
                        self.show_save_screen()

                    if event.key == pygame.K_l:
                        self.model.laberinto.cargar_mapa(self.model, "MapaGuardado.txt")
                        self.model.laberinto.cargar_score_vidas(self.model, "ScoreGuardado.txt")
                        self.show_load_screen()

            self.screen.fill((0, 0, 0))

            if self.model.pacdots_comidos == 240:
                self.draw_win_message()
                pygame.display.flip()
                pygame.time.delay(2000)

                self.model.laberinto.nivel += 1
                if self.model.laberinto.nivel > 3:
                    self.model.laberinto.nivel = 1

                self.adjust_ghost_speed()
                self.reset_level()
                continue

            if self.model.getCurrentPlayer().vidas == 0:
                self.draw_game_over_message()
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False
                continue

            delta_time = self.clock.tick(60) / 1000.0

            self.model.update_fruit_timer(delta_time)

            self.model.check_pildoras_collision()

            if self.model.superpacman:
                self.frightened_time += delta_time
                if self.frightened_time >= self.frightened_duration:
                    self.model.normal_mode()
                    self.frightened_time = 0
                else:
                    self.model.ghosts_frightened_mode()
            else:
                self.mode_timer += delta_time
                if self.current_mode == 'chase':
                    if self.mode_timer >= self.chase_duration:
                        self.current_mode = 'scatter'
                        self.mode_timer = 0
                elif self.current_mode == 'scatter':
                    if self.mode_timer >= self.scatter_duration:
                        self.current_mode = 'chase'
                        self.mode_timer = 0

                self.model.set_ghosts_mode(self.current_mode)

            blinky = self.model.getBlinky()
            clyde = self.model.getClyde()
            inky = self.model.getInky()
            pinky = self.model.getPinky()

            if blinky.muerte:
                blinky.ghost_respawn()
            else:
                blinky.Blinky_behave()

            if clyde.muerte:
                clyde.ghost_respawn()
            else:
                clyde.Clyde_behave()

            if inky.muerte:
                inky.ghost_respawn()
            else:
                inky.Inky_behave()

            if pinky.muerte:
                pinky.ghost_respawn()
            else:
                pinky.Pinky_behave()

            self.controller.movimiento_pacman(event)
            self.controller.movimiento_pacman()

            current_lives = self.model.getCurrentPlayer().vidas
            if current_lives < self.previous_lives:
                self.model.reset_pacman()
                self.model.reset_ghosts()
                self.previous_lives = current_lives

            self.draw_labyrinth()

            pygame.display.flip()

    def draw_labyrinth(self):
        self.model.getLaberinto().dibujar_laberinto(self.screen)
        self.model.getLaberinto().dibujar_misc(self.screen)

        pacman = self.model.getCurrentPlayer()
        self.model.draw_pacman(self.screen, pacman)
        self.model.draw_ghosts(self.screen)

        self.model.check_pacdot_collision()
        self.model.check_collision_fruit()
        self.model.check_ghost_collision()
        self.model.check_pildoras_collision()

    def adjust_ghost_speed(self):
        if self.model.laberinto.nivel == 1:
            speed_increase = 3
            self.model.ghosts_add_speed(speed_increase)
        elif self.model.laberinto.nivel == 2:
            speed_increase = 50
            self.model.ghosts_add_speed(speed_increase)
        elif self.model.laberinto.nivel == 3:
            speed_increase = 9
            self.model.ghosts_add_speed(speed_increase)
