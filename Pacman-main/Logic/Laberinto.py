import pygame
import networkx as nx

from Logic import Pacman
from Logic import Ghosts

class Laberinto:
    def __init__(self, cell_size, archivo_mapa='Mapa.txt'):
        self.nivel = 1
        self.tablero = nx.Graph()
        self.score = 0
        self.lives = 3
        self.cell_size = cell_size
        self.font = pygame.font.Font("Utilitarios/PressStart2P-Regular.ttf", 20)
        self.pacman = None
        self.pinky = None
        self.blinky = None
        self.inky = None
        self.clyde = None
        self.vida_icono = pygame.transform.scale(pygame.image.load("icons/corazon.png"), (25, 25))
        self.frutas_por_nivel = [
            "icons/Fresa.png",
            "icons/Naranja.png",
            "icons/Cereza.png"
        ]
        nivel_index = self.nivel - 1
        self.fruta_icono = pygame.transform.scale(pygame.image.load(self.frutas_por_nivel[nivel_index]), (16, 16))
        self.items = {'pacman': None, 'pinky': None, 'blinky': None, 'inky': None, 'clyde': None, 'tunnel': [], 'fruit': None}

        # Intentar cargar el mapa guardado, si no existe, lanzará un error
        try:
            with open(archivo_mapa, 'r') as f:
                self.board = [line.strip() for line in f.readlines()]
                print(f"Mapa cargado desde {archivo_mapa}")
        except FileNotFoundError:
            print(f"Error: El archivo {archivo_mapa} no se encontró.")
            raise  # Lanza el error para que el programa se detenga si no se encuentra el mapa


    def set_pacman(self, pacman):
        self.pacman = pacman

    def set_pinky(self, pinky):
        self.pinky = pinky

    def set_blinky(self, blinky):
        self.blinky = blinky

    def set_inky(self, inky):
        self.inky = inky

    def set_clyde(self, clyde):
        self.clyde = clyde

    def set_vidas(self, vidas):
        self.lives = vidas

    def set_score(self, score):
        self.score = score

    def generar_fruta(self):

        nivel_index = self.nivel - 1
        self.fruta_icono = pygame.transform.scale(pygame.image.load(self.frutas_por_nivel[nivel_index]), (16, 16))

        self.items['fruit'] = (17, 14)
        self.tablero.nodes[(17, 14)]['tipo'] = 'fruit'

        print(f"Nivel {self.nivel} - Fruta cargada: {self.frutas_por_nivel[self.nivel - 1]}")

    def crear_laberinto(self):
        """
        Crea el laberinto a partir del tablero dado, configurando las posiciones de los elementos
        (paredes, pacdots, píldoras, túneles, fantasmas y Pac-Man) en el grafo que representa el laberinto.
        Además, establece las conexiones entre los nodos adyacentes.
        """
        self.tablero.clear()

        for i, row in enumerate(self.board):
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell == '#':
                    self.tablero.add_node(pos, tipo='pared')
                elif cell == '.':
                    self.tablero.add_node(pos, tipo='pacdot')
                elif cell == '-':
                    self.tablero.add_node(pos, tipo='linea')
                elif cell == 'o':
                    self.tablero.add_node(pos, tipo='pildoras')
                elif cell == 'M':
                    self.items['pacman'] = pos
                    self.tablero.add_node(pos, tipo='camino')
                elif cell == 'P':
                    self.items['pinky'] = pos
                    self.tablero.add_node(pos, tipo='camino')
                elif cell == 'B':
                    self.items['blinky'] = pos
                    self.tablero.add_node(pos, tipo='camino')
                elif cell == 'I':
                    self.items['inky'] = pos
                    self.tablero.add_node(pos, tipo='camino')
                elif cell == 'C':
                    self.items['clyde'] = pos
                    self.tablero.add_node(pos, tipo='camino')
                elif cell == '$':
                    self.items['tunnel'].append(pos)
                    self.tablero.add_node(pos, tipo='tunnel')
                elif cell == 'F':
                    self.tablero.add_node(pos, tipo='fruit')

                if cell != '#':
                    if i < len(self.board) - 1 and self.board[i + 1][j] != '#':
                        self.tablero.add_edge(pos, (i + 1, j), weight=1)
                    if j < len(row) - 1 and self.board[i][j + 1] != '#':
                        self.tablero.add_edge(pos, (i, j + 1), weight=1)

    def guardar_mapa(self, model, nombre_archivo='MapaGuardado.txt'):
        """
        Guarda el estado actual del laberinto, incluyendo las posiciones de Pac-Man y los fantasmas,
        en un archivo de texto. El archivo contiene una representación del mapa con caracteres que
        indican las posiciones de los elementos (como paredes, pacdots, píldoras, túneles, etc.).
        """
        self.items['pacman'] = self.pacman.node_position
        self.items['pinky'] = self.pinky.node_position
        self.items['blinky'] = self.blinky.node_position
        self.items['inky'] = self.inky.node_position
        self.items['clyde'] = self.clyde.node_position

        with open(nombre_archivo, 'w') as f:
            for i in range(len(self.board)):
                fila = ""
                for j in range(len(self.board[i])):
                    pos = (i, j)
                    if pos == self.items['pacman']:
                        fila += 'M'  # Pac-Man
                    elif pos == self.items['pinky']:
                        fila += 'P'  # Pinky
                    elif pos == self.items['blinky']:
                        fila += 'B'  # Blinky
                    elif pos == self.items['inky']:
                        fila += 'I'  # Inky
                    elif pos == self.items['clyde']:
                        fila += 'C'  # Clyde
                    else:
                        nodo = self.tablero.nodes.get(pos, {})
                        tipo = nodo.get('tipo', None)
                        if tipo == 'pared':
                            fila += '#'
                        elif tipo == 'pacdot':
                            fila += '.'
                        elif tipo == 'linea':
                            fila += '-'
                        elif tipo == 'pildoras':
                            fila += 'o'
                        elif tipo == 'camino':
                            fila += ' '
                        elif tipo == 'fruit':
                            fila += 'F'
                        elif tipo == 'tunnel':
                            fila += '$'
                        else:
                            fila += ' '
                f.write(fila + '\n')

    def guardar_score_vidas(self, model, nombre_archivo='ScoreYVidas.txt'):
        """
        Guarda el puntaje y las vidas actuales en un archivo de texto.

        Esta función escribe el puntaje y las vidas del jugador en un archivo especificado. Si no se
        proporciona un nombre de archivo, se utilizará el valor por defecto 'ScoreYVidas.txt'.
        """
        try:
            score = model.laberinto.score
            vidas = model.laberinto.lives

            with open(nombre_archivo, 'w') as f:
                f.write(f"Score: {score}\n")
                f.write(f"Vidas: {vidas}\n")

            print(f"Score y vidas guardados correctamente en {nombre_archivo}")
        except Exception as e:
            print(f"Error al guardar score y vidas: {e}")

    def cargar_mapa(self, model, nombre_archivo='MapaGuardado.txt'):
        """
        Carga el mapa guardado desde un archivo y establece las posiciones de los elementos del juego.

        Esta función lee el archivo especificado, carga la información del mapa y reconstruye el tablero,
        incluyendo la ubicación de Pac-Man, los fantasmas y otros objetos en el mapa.

        """
        try:
            with open(nombre_archivo, 'r') as f:
                self.board = [line.strip() for line in f.readlines()]

            self.tablero.clear()
            self.items['pacman'] = None
            self.items['pinky'] = None
            self.items['blinky'] = None
            self.items['inky'] = None
            self.items['clyde'] = None
            self.items['tunnel'] = []

            for i, row in enumerate(self.board):
                for j, cell in enumerate(row):
                    pos = (i, j)

                    if cell == '#':
                        self.tablero.add_node(pos, tipo='pared')
                    elif cell == '.':
                        self.tablero.add_node(pos, tipo='pacdot')
                    elif cell == '-':
                        self.tablero.add_node(pos, tipo='linea')
                    elif cell == 'o':
                        self.tablero.add_node(pos, tipo='pildoras')
                    elif cell == 'M':
                        self.items['pacman'] = pos
                        self.tablero.add_node(pos, tipo='camino')
                    elif cell == 'P':
                        self.items['pinky'] = pos
                        self.tablero.add_node(pos, tipo='camino')
                    elif cell == 'B':
                        self.items['blinky'] = pos
                        self.tablero.add_node(pos, tipo='camino')
                    elif cell == 'I':
                        self.items['inky'] = pos
                        self.tablero.add_node(pos, tipo='camino')
                    elif cell == 'C':
                        self.items['clyde'] = pos
                        self.tablero.add_node(pos, tipo='camino')
                    elif cell == '$':
                        self.items['tunnel'].append(pos)
                        self.tablero.add_node(pos, tipo='tunnel')
                    elif cell == 'F':
                        self.tablero.add_node(pos, tipo='fruit')
                    elif cell == ' ' or cell == '':
                        self.tablero.add_node(pos, tipo='vacío')

                    if cell != '#':
                        if i < len(self.board) - 1 and self.board[i + 1][j] != '#':
                            self.tablero.add_edge(pos, (i + 1, j), weight=1)
                        if j < len(row) - 1 and self.board[i][j + 1] != '#':
                            self.tablero.add_edge(pos, (i, j + 1), weight=1)

            pacman_pos = self.items['pacman']
            blinky_pos = self.items['blinky']
            clyde_pos = self.items['clyde']
            inky_pos = self.items['inky']
            pinky_pos = self.items['pinky']
            model.set_positions(pacman_pos, blinky_pos, clyde_pos, inky_pos, pinky_pos)
        except FileNotFoundError:
            print(f"Error: El archivo {nombre_archivo} no se encontró.")


    def cargar_score_vidas(self, model, nombre_archivo='ScoreYVidas.txt'):
        """
        Carga el puntaje y las vidas guardados desde un archivo y actualiza el modelo.

        Esta función lee el archivo especificado, extrae el puntaje y las vidas guardadas,
        y actualiza los valores correspondientes en el modelo del juego.

        """
        try:
            with open(nombre_archivo, 'r') as f:
                lines = f.readlines()

                score_line = lines[0].strip()
                lives_line = lines[1].strip()

                score = int(score_line.split(":")[1].strip())
                lives = int(lives_line.split(":")[1].strip())

                model.laberinto.set_score(score)
                model.laberinto.set_vidas(lives)
        except FileNotFoundError:
            print(f"Error: El archivo {nombre_archivo} no se encontró.")
        except Exception as e:
            print(f"Error al cargar score y vidas: {e}")

    def dibujar_laberinto(self, pantalla):
        """
        Dibuja el laberinto en la pantalla.

        Esta función recorre todos los nodos del laberinto, determina su tipo
        y dibuja los elementos correspondientes en la pantalla utilizando Pygame.
        Dependiendo del tipo de nodo, se dibujan diferentes elementos gráficos
        como pacdots, líneas, paredes, píldoras, caminos y frutas.
        """
        for (i, j), data in self.tablero.nodes(data=True):
            x = j * self.cell_size
            y = i * self.cell_size
            tipo = data.get('tipo', None)

            if tipo == 'pacdot':
                pygame.draw.circle(pantalla, "pink", (x + self.cell_size // 2, y + self.cell_size // 2),
                                   self.cell_size // 6)
            elif tipo == 'linea':
                pygame.draw.rect(pantalla, "white", (x, y + (self.cell_size - 7) // 2, self.cell_size, 7))
            elif tipo == 'pared':
                pygame.draw.rect(pantalla, "dark blue", (x, y, self.cell_size - 3, self.cell_size - 3))
            elif tipo == 'pildoras':
                pygame.draw.circle(pantalla, "yellow", (x + self.cell_size // 2, y + self.cell_size // 2),
                                   self.cell_size // 4)
            elif tipo == 'camino':
                pygame.draw.rect(pantalla, "black", (x, y, self.cell_size - 3, self.cell_size - 3))
            elif tipo == 'fruit':
                pantalla.blit(self.fruta_icono, (x + self.cell_size // 2 - self.fruta_icono.get_width() // 2,
                                                 y + self.cell_size // 2 - self.fruta_icono.get_height() // 2))

    #----------------------HECHO CON IA--------------------------
    def dibujar_misc(self, pantalla):
        """
        Dibuja los elementos adicionales en la pantalla, como la puntuación, el nivel y los iconos de las vidas.

        Esta función utiliza Pygame para renderizar el texto de la puntuación y el nivel, y para mostrar los iconos de las vidas restantes.
        """
        score_text = self.font.render(f'Score: {self.score}', True, 'white')
        pantalla.blit(score_text, (25, 640))

        nivel_text = self.font.render(f'Level: {self.nivel}', True, 'white')
        pantalla.blit(nivel_text, (250, 640))

        for i in range(self.lives):
            pantalla.blit(self.vida_icono, (450 + i * 30, 635))

    #----------------------------------------------------------------

    def check_tunnel(self, player_position):
        """
        Verifica si el jugador está en un túnel y, de ser así, lo teletransporta a la otra salida.

        Si el jugador está en uno de los túneles definidos, se moverá a la otra salida del túnel. Si no está en un túnel,
        la posición del jugador no cambiará.

        """
        if player_position in self.items['tunnel']:
            tunnel_positions = self.items['tunnel']
            new_position = tunnel_positions[1] if player_position == tunnel_positions[0] else tunnel_positions[0]
            return new_position
        return player_position


