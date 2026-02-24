import pygame
from Logic.Laberinto import Laberinto
import networkx as nx

class Controller:
    def __init__(self, model, view):
        """
        Inicializa el controlador, estableciendo el modelo y la vista.
        También se encarga de la creación del tablero.

        Parámetros:
            model: El modelo del juego, que contiene la lógica de datos.
            view: La vista del juego, que maneja la representación visual.
        """
        self.model = model
        self.view = view
        self.last_direction = None
        self.move_timer = 0
        self.crear_tablero()

    def crear_tablero(self):
        """
        Crea el tablero de juego llamando a la clase Laberinto y lo asigna al modelo.
        """
        tablero = Laberinto(20)
        tablero.crear_laberinto()
        self.model.setLaberinto(tablero)

    def movimiento_pacman(self, event=None):
        """
        Maneja el movimiento de Pac-Man basado en las entradas del teclado y el temporizador.

        Args:
            event: El evento que recibe de Pygame (opcional).
        """
        player = self.model.getCurrentPlayer()

        if event and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.last_direction = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.last_direction = (1, 0)
            elif event.key == pygame.K_UP:
                self.last_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                self.last_direction = (0, 1)

        self.move_timer += 2

        if self.move_timer >= 60:
            self.move_timer = 0

            if self.last_direction:
                new_x = player.getPosition()[0] + self.last_direction[1]
                new_y = player.getPosition()[1] + self.last_direction[0]
                new_position = (new_x, new_y)

                if not self.model.check_collision(new_position):
                    new_position = self.model.check_tunnel(new_position)
                    player.update_position(new_position)

                    player.set_direction('LEFT' if self.last_direction == (-1, 0) else
                                         'RIGHT' if self.last_direction == (1, 0) else
                                         'UP' if self.last_direction == (0, -1) else
                                         'DOWN')
