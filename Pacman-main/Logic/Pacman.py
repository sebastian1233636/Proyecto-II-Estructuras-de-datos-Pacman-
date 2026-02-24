import pygame

class Pacman:
    def __init__(self, velocidad):
        """
        Inicializa el objeto Pacman con la velocidad, vida, puntuación y dirección.
        Carga las imágenes de Pacman según la dirección y establece la posición inicial.

        """
        self.velocidad = velocidad
        self.muerte = False
        self.puntuacion = 0
        self.vidas = 3
        self.node_position = (23, 14)
        self.direccion = 'LEFT'
        self.last_direction = 'LEFT'
        self.frame_count = 0
        self.images_open = {
            'LEFT': pygame.transform.scale(pygame.image.load("icons/pacman_left.png"), (16, 16)),
            'RIGHT': pygame.transform.scale(pygame.image.load("icons/pacman_right.png"), (16, 16)),
            'UP': pygame.transform.scale(pygame.image.load("icons/pacman_up.png"), (16, 16)),
            'DOWN': pygame.transform.scale(pygame.image.load("icons/pacman_down.png"), (16, 16))
        }
        self.images_closed = {
            'LEFT': pygame.transform.scale(pygame.image.load("icons/pacman.png"), (16, 16)),
            'RIGHT': pygame.transform.scale(pygame.image.load("icons/pacman.png"), (16, 16)),
            'UP': pygame.transform.scale(pygame.image.load("icons/pacman.png"), (16, 16)),
            'DOWN': pygame.transform.scale(pygame.image.load("icons/pacman.png"), (16, 16))
        }
        self.imagen = self.images_open['LEFT']
        self.rect = self.imagen.get_rect()
        self.update_rect()

    def set_posicion(self, posicion):
        """
        Establece la posición de Pacman en el tablero.

        Args:
            posicion: Nueva posición de Pacman en el tablero.
        """
        self.node_position = posicion

    def quitarvidas(self):
        """
        Reduce en uno las vidas de Pacman si tiene vidas disponibles.
        """
        if self.vidas > 0:
            self.vidas -= 1

    def getvelocidad(self):
        """Devuelve la velocidad de Pacman."""
        return self.velocidad

    def getmuerte(self):
        """Devuelve el estado de muerte de Pacman."""
        return self.muerte

    def getpuntuacion(self):
        """Devuelve la puntuación de Pacman."""
        return self.puntuacion

    def getvidas(self):
        """Devuelve el número de vidas restantes de Pacman."""
        return self.vidas

    def getPosition(self):
        """Devuelve la posición de Pacman."""
        return self.node_position

    def update_position(self, new_pos):
        """
        Actualiza la posición de Pacman en el tablero.

        """
        self.node_position = new_pos
        self.update_rect()

    def update_rect(self):
        """Actualiza la posición del rectángulo que representa la imagen de Pacman en la pantalla."""
        self.rect.topleft = (self.node_position[1] * 22, self.node_position[0] * 22)

    def set_direction(self, direction):
        """
        Establece la dirección de Pacman y actualiza su imagen.

        """
        self.direccion = direction
        self.update_image()

    def update_image(self):
        """Actualiza la imagen de Pacman según la dirección y el tiempo de animación."""
        self.frame_count += 1
        if self.frame_count >= 2:
            self.frame_count = 0
        if self.frame_count < 1:
            self.imagen = self.images_open[self.direccion]
        else:
            self.imagen = self.images_closed[self.direccion]

    def move_left(self):
        """Establece la dirección de Pacman a izquierda."""
        self.set_direction('LEFT')

    def move_right(self):
        """Establece la dirección de Pacman a derecha."""
        self.set_direction('RIGHT')

    def move_up(self):
        """Establece la dirección de Pacman hacia arriba."""
        self.set_direction('UP')

    def move_down(self):
        """Establece la dirección de Pacman hacia abajo."""
        self.set_direction('DOWN')

    def draw(self, screen):
        """
        Dibuja la imagen de Pacman en la pantalla.

        """
        self.update_image()
        screen.blit(self.imagen, self.rect)

    def getDirection(self):
        """Devuelve la dirección actual de Pacman."""
        return self.direccion
