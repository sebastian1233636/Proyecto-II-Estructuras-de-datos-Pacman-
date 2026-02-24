from Logic.Ghosts import Blinky, Clyde, Inky, Pinky
from Logic.Pacman import Pacman
import pygame

class Model:
    def __init__(self):
        self.current_player = Pacman(0.8)
        self.ghosts = [
            Blinky('blinky', 'icons/Blinky.png', (11, 14), self,3, (1,26)),
            Clyde('clyde', 'icons/Clyde.png', (14, 15), self,3, (29,1)),
            Inky('inky', 'icons/Inky.png', (14, 14), self,3, (29,26)),
            Pinky('pinky', 'icons/Pinky.png', (14, 13), self,3, (1,1))
        ]
        self.laberinto = None
        self.paredes = {}
        self.pacdots = {}
        self.frutas = {}
        self.pildoras = {}
        self.pacdots_comidos = 0
        self.fruit_timer = 0
        self.frightened_timer = 0
        self.superpacman = False
        self.dead_ghost = ""

    def getCurrentPlayer(self): return self.current_player
    def getGhosts(self): return self.ghosts
    def getLaberinto(self): return self.laberinto
    def getBlinky(self): return self.ghosts[0]
    def getClyde(self): return self.ghosts[1]
    def getInky(self): return self.ghosts[2]
    def getPinky(self): return self.ghosts[3]

    def setear_personajes(self):
        """
        Asigna los personajes (Pac-Man y los fantasmas) al laberinto,
        colocando a cada uno en su posición correspondiente dentro del entorno de juego.
        """

        self.laberinto.set_pacman(self.current_player)
        self.laberinto.set_blinky(self.ghosts[0])
        self.laberinto.set_clyde(self.ghosts[1])
        self.laberinto.set_inky(self.ghosts[2])
        self.laberinto.set_pinky(self.ghosts[3])


    def ghosts_add_speed(self, velocidad):
        for ghost in self.ghosts:
            ghost.set_velocidad(velocidad)

    def setLaberinto(self, laberinto):
        self.laberinto = laberinto
        self._inicializar_hash_colisiones()

    def _inicializar_hash_colisiones(self):
        """
        Recorre el tablero del laberinto y clasifica las distintas entidades (paredes, pacdots,
        pildoras, frutas) en diccionarios correspondientes según su tipo,
        utilizando las posiciones (i, j) como claves.
        """

        for (i, j), data in self.laberinto.tablero.nodes(data=True):
            pos = (i, j)
            if data.get('tipo') == 'pared':
                self.paredes[pos] = data
            elif data.get('tipo') == 'pacdot':
                self.pacdots[pos] = data
            elif data.get('tipo') == 'pildoras':
                self.pildoras[pos] = data
            elif data.get('tipo') == 'fruta':
                self.frutas[pos] = data

    def draw_pacman(self, pantalla, pacman):
        i, j = pacman.node_position
        x = j * self.laberinto.cell_size
        y = i * self.laberinto.cell_size
        pantalla.blit(pacman.imagen, (x, y))

    def draw_ghosts(self, pantalla):
        for ghost in self.ghosts:
            i, j = ghost.node_position
            x = j * self.laberinto.cell_size
            y = i * self.laberinto.cell_size
            pantalla.blit(ghost.imagen, (x, y))

    def ghosts_chase_mode(self):
        self.getBlinky().chase_modeB()
        self.getClyde().chase_modeC()
        self.getInky().chase_modeI()
        self.getPinky().chase_modeP()

    def ghosts_scatter_mode(self):
        for ghost in self.ghosts:
            ghost.scatter_mode()

    def ghosts_frightened_mode(self):
        for ghost in self.ghosts:
            ghost.set_imagen('icons/scared_ghosts.png')
            ghost.mode_behave = 'frightened'

    def normal_mode(self):
        """
        Restaura el comportamiento normal de los fantasmas.

        """
        self.superpacman = False
        for ghost in self.ghosts:
            ghost.set_imagen("icons/" + ghost.nombre + ".png")
            ghost.mode_behave = 'chase'

    def reset_pacman(self):
        self.current_player.node_position = (23, 14)

    def reset_ghosts(self):
        """
        Restaura la posición de los fantasmas a sus posiciones iniciales.

        """
        self.getBlinky().node_position = (11, 14)
        self.getClyde().node_position = (14, 15)
        self.getInky().node_position = (14, 14)
        self.getPinky().node_position = (14, 13)

    def update_blinky(self):
        self.getBlinky().chase_modeB()

    def scatter_modeBlinky(self):
        self.getBlinky().scatter_mode()

    def getBlinkyPosition(self):
        return self.getBlinky().node_position

    def update_clyde(self):
        self.getClyde().chase_modeC()

    def scatter_modeClyde(self):
        self.getClyde().scatter_mode()

    def getClydePosition(self):
        return self.getClyde().node_position

    def update_inky(self):
        self.getInky().chase_modeI()

    def scatter_modeInky(self):
        self.getInky().scatter_mode()

    def getInkyPosition(self):
        return self.getInky().node_position

    def update_pinky(self):
        self.getPinky().chase_modeP()

    def scatter_modePinky(self):
        self.getPinky().scatter_mode()

    def getPinkyPosition(self):
        return self.getPinky().node_position

    def set_positions(self, pacman_pos, blinky_pos, clyde_pos, inky_pos, pinky_pos):
        """
        Establece las posiciones de los personajes en el tablero.

        """
        self.getBlinky().set_posicion(blinky_pos)
        self.getClyde().set_posicion(clyde_pos)
        self.getInky().set_posicion(inky_pos)
        self.getPinky().set_posicion(pinky_pos)
        self.current_player.set_posicion(pacman_pos)

    def set_ghosts_mode(self, behavior):
        for ghost in self.ghosts:
            ghost.mode_behave = behavior

    def check_tunnel(self, position):
        return self.laberinto.check_tunnel(position)

    def check_collision(self, new_position):
        """
        Verifica si una nueva posición está ocupada por una pared en el laberinto.
        Devuelve True si hay colisión (es decir, si la nueva posición está en el diccionario de paredes),
        de lo contrario, devuelve False.
        """

        return new_position in self.paredes

    def check_pacdot_collision(self):
        """
           Verifica si el jugador ha colisionado con un pacdot.
           Si hay colisión, incrementa la puntuación, elimina el pacdot del laberinto y
           actualiza su estado. Si el jugador ha comido una cantidad específica de pacdots,
           genera una fruta si aún no está presente.
        """
        player = self.getCurrentPlayer()
        pos = player.node_position
        if pos in self.pacdots:
            self.laberinto.score += 10
            self.pacdots.pop(pos)
            self.laberinto.tablero.nodes[pos]['tipo'] = 'vacio'
            self.pacdots_comidos += 1
            if self.pacdots_comidos in [70, 190] and self.laberinto.items['fruit'] is None:
                self.laberinto.generar_fruta()

    def check_collision_fruit(self):
        player = self.getCurrentPlayer()
        pos = player.node_position
        if pos == self.laberinto.items['fruit']:
            puntos_por_nivel = {1: 100, 2: 300, 3: 500}
            puntos = puntos_por_nivel.get(self.laberinto.nivel)
            self.laberinto.score += puntos
            self.laberinto.tablero.nodes[pos]['tipo'] = 'vacio'
            self.laberinto.items['fruit'] = None

    def update_fruit_timer(self, delta_time):
        """
            Verifica si el jugador ha colisionado con una fruta.
            Si es así, incrementa la puntuación según el nivel actual y elimina la fruta del laberinto.
        """
        if self.laberinto.items['fruit'] is not None:
            self.fruit_timer += delta_time
            if self.fruit_timer >= 10:
                self.remove_fruit()

    def remove_fruit(self):
        """
           Elimina la fruta del laberinto, marcando su posición como vacía y
           restableciendo el temporizador de la fruta.
        """
        fruit_pos = self.laberinto.items['fruit']
        if fruit_pos is not None:
            self.laberinto.tablero.nodes[fruit_pos]['tipo'] = 'vacio'
            self.laberinto.items['fruit'] = None
        self.fruit_timer = 0

    def check_pildoras_collision(self):
        """
            Verifica si el jugador ha colisionado con una pildora.
            Si hay colisión, activa el modo Super Pac-Man y elimina la pildora del laberinto.
        """
        player = self.getCurrentPlayer()
        pos = player.node_position
        if pos in self.pildoras:
            self.superpacman = True
            self.pildoras.pop(pos)
            self.laberinto.tablero.nodes[pos]['tipo'] = 'vacio'

    def check_ghost_collision(self):

        """
            Verifica si Pac-Man ha colisionado con algún fantasma.
            Si Pac-Man está en modo Super Pac-Man, los fantasmas que colisionen con él serán comidos y
            se incrementará la puntuación. Si no está en modo Super Pac-Man, Pac-Man pierde vidas al colisionar con un fantasma.
        """
        pacman_pos = self.getCurrentPlayer().node_position
        eaten_ghosts = 0

        for ghost in self.ghosts:
            if ghost.node_position == pacman_pos:
                if self.superpacman:
                    if ghost.nombre == 'blinky':
                        self.getBlinky().set_muerte(True)
                        eaten_ghosts += 1

                    elif ghost.nombre == 'clyde':
                        self.getClyde().set_muerte(True)
                        eaten_ghosts += 1

                    elif ghost.nombre == 'inky':
                        self.getInky().set_muerte(True)
                        eaten_ghosts += 1
                    elif ghost.nombre == 'pinky':
                        self.getPinky().set_muerte(True)
                        eaten_ghosts += 1

                    if eaten_ghosts == 1:
                        self.laberinto.score += 200
                    elif eaten_ghosts == 2:
                        self.laberinto.score += 400
                    elif eaten_ghosts == 3:
                        self.laberinto.score += 800
                    elif eaten_ghosts >= 4:
                        self.laberinto.score += 1600
                else:
                    if ghost.nombre == 'blinky':
                        self.getCurrentPlayer().quitarvidas()
                        self.laberinto.lives -= 1
                    elif ghost.nombre == 'clyde':
                        self.getCurrentPlayer().quitarvidas()
                        self.laberinto.lives -= 1
                    elif ghost.nombre == 'inky':
                        self.getCurrentPlayer().quitarvidas()
                        self.laberinto.lives -= 1
                    elif ghost.nombre == 'pinky':
                        self.getCurrentPlayer().quitarvidas()
                        self.laberinto.lives -= 1













