import pygame
import random
import networkx as nx
import numpy as np

class Ghost:
    def __init__(self, nombre, imagen_path, pos, model, speed, scatter_target):
        self.nombre = nombre
        self.imagen = pygame.transform.scale(pygame.image.load(imagen_path), (16, 16))
        self.node_position = tuple(pos)  # La posición en nodos (fila, columna) como tupla
        self.model = model
        self.speed = speed  # La velocidad del fantasma (puede ser un valor mayor para más velocidad)
        self.move_timer = 0  # Temporizador para controlar la velocidad
        self.move_interval = 1 / self.speed  # Intervalo en segundos entre movimientos basado en la velocidad
        self.scatter_target = scatter_target  # Objetivo de dispersión (posición de dispersión)
        self.muerte = False
        self.mode_behave = "scatter"
        self.move_interval_respawn = 0.2 / self.speed

    def set_imagen(self, imagen_path):
        self.imagen = pygame.transform.scale(pygame.image.load(imagen_path), (16, 16))

    def set_muerte(self, muerte):
        self.muerte = muerte

    def set_velocidad(self, velocidad):
        self.speed = velocidad

    def set_posicion(self, pos):
        self.node_position = tuple(pos)




    def draw(self, pantalla):
        # Dibuja el fantasma en su posición actual en nodos
        pos_x = self.node_position[1] * 22  # Cambia según tu tamaño de celda
        pos_y = self.node_position[0] * 22  # Cambia según tu tamaño de celda
        pantalla.blit(self.imagen, (pos_x, pos_y))

    def frightened_mode(self):
        """
           Modo asustado para el fantasma, donde realiza movimientos aleatorios en el laberinto alejándose de Pac-Man.
           El fantasma selecciona un nodo objetivo aleatorio que no esté bloqueado, esté al menos a cinco nodos de distancia,
           y calcula el camino más corto hasta él.

           Funcionamiento:
           - Incrementa un temporizador en cada frame, limitando la frecuencia de movimiento del fantasma.
           - Verifica la posición de Pac-Man y del fantasma, y realiza teletransportación si están en túneles.
           - Selecciona un nodo aleatorio accesible en el laberinto que cumpla las condiciones de distancia y ausencia de bloqueo.
           - Calcula el camino más corto hacia este nodo y actualiza la posición del fantasma al siguiente nodo de la ruta.

           Notas:
           - La distancia mínima de 5 nodos asegura que el fantasma no se acerque a Pac-Man mientras está en modo asustado.
           - Si no se encuentra un nodo adecuado tras varios intentos, el fantasma no se mueve en este ciclo.
           """

        self.move_timer += 1 / 60
        if self.move_timer >= self.move_interval:
            self.move_timer = 0
            pacman_position = self.model.getCurrentPlayer().getPosition()
            graph = self.model.getLaberinto().tablero
            laberinto = self.model.getLaberinto()


            pacman_position = laberinto.check_tunnel(pacman_position)
            self.node_position = laberinto.check_tunnel(self.node_position)
            all_nodes = list(graph.nodes)

            def is_blocked(node):
                return graph.nodes[node].get('tipo') == 'pared'

            target_node = None
            for _ in range(10):
                candidate_node = random.choice([node for node in all_nodes if node != self.node_position])
                if not is_blocked(candidate_node):
                    try:
                        distance = nx.shortest_path_length(graph, source=self.node_position, target=candidate_node)
                        if distance > 5:
                            target_node = candidate_node
                            break
                    except nx.NetworkXNoPath:
                        continue
            if target_node is None:
                return

            try:
                path = nx.shortest_path(graph, source=self.node_position, target=target_node)
                if len(path) > 1:
                    self.node_position = path[1]
            except nx.NetworkXNoPath:
                pass

    def scatter_mode(self):
        """
        Modo de dispersión para el fantasma, donde se dirige hacia su posición de dispersión (scatter target).
        El fantasma se mueve en intervalos regulares hacia un nodo objetivo específico en el laberinto,
        que representa su posición de dispersión.

        Funcionamiento:
        - Incrementa un temporizador en cada frame para controlar la frecuencia de movimiento del fantasma.
        - Verifica si el nodo de dispersión existe en el grafo; si no, finaliza el método.
        - Calcula el camino más corto hacia el objetivo de dispersión y mueve al fantasma al siguiente nodo en la ruta.
        """
        self.move_timer += 1 / 60

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            graph = self.model.getLaberinto().tablero

            if self.scatter_target not in graph:
                print(f"El nodo objetivo de dispersión {self.scatter_target} no existe en el grafo.")
                return

            try:
                path = nx.shortest_path(graph, source=self.node_position, target=self.scatter_target)
                if len(path) > 1:
                    self.node_position = path[1]
                else:
                    print(f"{self.nombre} ya está en el objetivo de dispersión {self.scatter_target}")
            except nx.NetworkXNoPath:
                print(f"No se encontró un camino hacia el objetivo de dispersión {self.scatter_target}")

    def ghost_respawn(self):
        """
        Modo de reaparición del fantasma, que lo dirige hacia su posición de reaparición en el laberinto.
        El fantasma se mueve en intervalos regulares hacia una posición de destino específica (11, 14)
        hasta alcanzarla y "revivir".

        Funcionamiento:
        - Establece la imagen del fantasma en su estado de reaparición.
        - Incrementa un temporizador para controlar la frecuencia de movimiento.
        - Calcula el camino más corto hacia la posición de reaparición (11, 14) y avanza un nodo en la ruta.
        - Al llegar a la posición de reaparición, cambia el estado del fantasma a vivo.
        """
        self.set_imagen("icons/ghost_dead.png")
        self.move_timer += 1 / 60
        if self.move_timer >= self.move_interval_respawn:
            self.move_timer = 0
            target_position = (11, 14)
            graph = self.model.getLaberinto().tablero
            laberinto = self.model.getLaberinto()
            self.node_position = laberinto.check_tunnel(self.node_position)
            target_position = laberinto.check_tunnel(target_position)
            try:
                path = nx.shortest_path(graph, source=self.node_position, target=target_position, weight="weight")

                if len(path) > 1:
                    self.node_position = path[1]
                else:
                    self.muerte = False

            except nx.NetworkXNoPath:
                print(f"No se encontró un camino hacia la posición de reaparición {target_position}")


class Blinky(Ghost):
    def __init__(self, nombre, imagen_path, pos, model, speed, scatter_target):
        super().__init__(nombre, imagen_path, pos, model, speed, scatter_target)  # Pasar scatter_target al inicializador

    def chase_modeB(self):
        """
        Modo de persecución del fantasma, que lo mueve hacia la posición actual de Pac-Man.
        Funcionamiento:
        - Incrementa un temporizador para controlar la frecuencia de movimiento del fantasma.
        - Calcula el camino más corto hacia la posición de Pac-Man, considerando los túneles.
        - El fantasma se mueve un nodo en la ruta hacia Pac-Man.
                """
        self.move_timer += 1 / 60

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            pacman_position = self.model.getCurrentPlayer().getPosition()
            graph = self.model.getLaberinto().tablero
            laberinto = self.model.getLaberinto()

            pacman_position = laberinto.check_tunnel(pacman_position)
            self.node_position = laberinto.check_tunnel(self.node_position)

            try:
                path = nx.shortest_path(graph, source=self.node_position, target=pacman_position)
                if len(path) > 1:
                    self.node_position = path[1]
            except nx.NetworkXNoPath:
                pass

    def Blinky_behave(self):
        """
        Define el comportamiento del fantasma Blinky en función del modo actual.
        denido a que todos los fantasmas tienen el mismo metodo, no se hablará de los demas

        """
        if self.mode_behave == "scatter":
            self.scatter_mode()
        elif self.mode_behave == "chase":
            self.chase_modeB()
        elif self.mode_behave == "frightened":
            self.frightened_mode()
        elif self.mode_behave == "respawn":
            self.ghost_respawn()




class Clyde(Ghost):
    def __init__(self, nombre, imagen_path, pos, model, speed, scatter_target=(29, 1)):
        super().__init__(nombre, imagen_path, pos, model, speed, scatter_target)
        self.scatter_position = scatter_target

    def chase_modeC(self):
        """
        Modo de persecución de Clyde, que lo mueve hacia Pac-Man si está lo suficientemente lejos,
        o hacia una posición predeterminada si está cerca.

        Funcionamiento:
        - Incrementa un temporizador para controlar la frecuencia de movimiento.
        - Calcula la distancia entre Clyde y Pac-Man. Si está a más de 8 celdas, Clyde se mueve hacia Pac-Man.
        - Si está a 8 o menos celdas, Clyde se mueve hacia la casilla (29, 1).
        - Verifica si Clyde o Pac-Man están en un túnel y los teletransporta si es necesario.
        """
        self.move_timer += 1 / 60

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            pacman_position = self.model.getCurrentPlayer().getPosition()
            graph = self.model.getLaberinto().tablero
            laberinto = self.model.getLaberinto()

            pacman_position = laberinto.check_tunnel(pacman_position)
            self.node_position = laberinto.check_tunnel(self.node_position)

            try:
                distancia_a_pacman = nx.shortest_path_length(graph, self.node_position, pacman_position)
            except nx.NetworkXNoPath:
                distancia_a_pacman = float('inf')

            if distancia_a_pacman > 8:
                try:
                    path = nx.shortest_path(graph, source=self.node_position, target=pacman_position)
                    if len(path) > 1:
                        self.node_position = path[1]
                except nx.NetworkXNoPath:
                    pass
            else:
                try:
                    path = nx.shortest_path(graph, source=self.node_position, target=self.scatter_position)
                    if len(path) > 1:
                        self.node_position = path[1]
                except nx.NetworkXNoPath:
                    pass

            self.node_position = laberinto.check_tunnel(self.node_position)

    def Clyde_behave(self):
        if self.mode_behave == "scatter":
            self.scatter_mode()
        elif self.mode_behave == "chase":
            self.chase_modeC()
        elif self.mode_behave == "frightened":
            self.frightened_mode()
        elif self.mode_behave == "respawn":
            self.ghost_respawn()





class Inky(Ghost):
    def __init__(self, nombre, imagen_path, pos, model, speed, scatter_target):
        super().__init__(nombre, imagen_path, pos, model, speed, scatter_target)


    #---------------------------------------------HEHCO CON IA--------------------------------------------------------------
    def chase_modeI(self):
        """
        Modo de persecución para Blinky, que ajusta su comportamiento dependiendo de la distancia a Pac-Man y su dirección.
        Si está lo suficientemente cerca, Blinky se mueve directamente hacia Pac-Man. Si no, calcula una casilla intermedia
        en la dirección de Pac-Man y luego invierte la dirección para confundir a Pac-Man. Si no es posible moverse
        directamente, se mueve hacia el nodo adyacente más cercano o aleatoriamente si no hay opciones.

        Este metodo fue hecho con IA
        """
        self.move_timer += 1 / 60

        if self.move_timer >= self.move_interval:
            self.move_timer = 0

            posicion_pacman = self.model.getCurrentPlayer().getPosition()
            direccion_pacman = self.model.getCurrentPlayer().getDirection()
            grafo = self.model.getLaberinto().tablero

            posicion_blinky = self.model.getBlinky().node_position

            posicion_pacman = self.model.getLaberinto().check_tunnel(posicion_pacman)

            try:
                distancia = nx.shortest_path_length(grafo, source=posicion_blinky, target=posicion_pacman)
                if distancia <= 3:
                    posicion_objetivo = posicion_pacman
                else:
                    posicion_intermedia = posicion_pacman
                    for _ in range(2):
                        if direccion_pacman == 'UP':
                            posicion_intermedia = (posicion_intermedia[0] - 1, posicion_intermedia[1])
                        elif direccion_pacman == 'DOWN':
                            posicion_intermedia = (posicion_intermedia[0] + 1, posicion_intermedia[1])
                        elif direccion_pacman == 'LEFT':
                            posicion_intermedia = (posicion_intermedia[0], posicion_intermedia[1] - 1)
                        elif direccion_pacman == 'RIGHT':
                            posicion_intermedia = (posicion_intermedia[0], posicion_intermedia[1] + 1)

                        if not grafo.has_node(posicion_intermedia):
                            posicion_intermedia = posicion_pacman
                            break

                    dx = posicion_blinky[0] - posicion_intermedia[0]
                    dy = posicion_blinky[1] - posicion_intermedia[1]

                    nuevo_dx = -dx
                    nuevo_dy = -dy

                    objetivo = (posicion_intermedia[0] + nuevo_dx, posicion_intermedia[1] + nuevo_dy)

                    if grafo.has_node(objetivo):
                        posicion_objetivo = objetivo
                    else:
                        adyacentes = list(grafo.neighbors(self.node_position))
                        if adyacentes:
                            distancia_minima = float('inf')
                            nodo_adyacente_cercano = None
                            for nodo in adyacentes:
                                distancia = nx.shortest_path_length(grafo, nodo, posicion_pacman)
                                if distancia < distancia_minima:
                                    distancia_minima = distancia
                                    nodo_adyacente_cercano = nodo
                            posicion_objetivo = nodo_adyacente_cercano
                        else:
                            posicion_objetivo = self.node_position
            except nx.NetworkXNoPath:
                posicion_objetivo = self.node_position

            if posicion_objetivo == self.node_position or not grafo.has_node(posicion_objetivo):
                adyacentes = list(grafo.neighbors(self.node_position))
                if adyacentes:
                    posicion_objetivo = random.choice(adyacentes)
                else:
                    posicion_objetivo = self.node_position

            if posicion_objetivo:
                if posicion_objetivo == self.node_position:
                    return

                try:
                    path = nx.shortest_path(grafo, source=self.node_position, target=posicion_objetivo)
                    if len(path) > 1:
                        self.node_position = path[1]
                except nx.NetworkXNoPath:
                    adyacentes = list(grafo.neighbors(self.node_position))
                    if adyacentes:
                        self.node_position = random.choice(adyacentes)

            self.node_position = self.model.getLaberinto().check_tunnel(self.node_position)

    # --------------------------------------------------------------------------------------------------------------------

    def Inky_behave(self):
        if self.mode_behave == "scatter":
            self.scatter_mode()
        elif self.mode_behave == "chase":
            self.chase_modeI()
        elif self.mode_behave == "frightened":
            self.frightened_mode()
        elif self.mode_behave == "respawn":
            self.ghost_respawn()

class Pinky(Ghost):
    def __init__(self, nombre, imagen_path, pos, model, speed, scatter_target):
        super().__init__(nombre, imagen_path, pos, model, speed, scatter_target)

    def chase_modeP(self):
        """
        Mueve al fantasma siguiendo a Pac-Man con base en su posición y dirección.
        El fantasma calcula la posición proyectada de 2 nodos adelante de la direccion
        de Pac-Man y toma decisiones sobre su movimiento dependiendo del tipo de nodo al
        que se dirige (camino, túnel, muro, etc.).
        Si el fantasma está cerca de Pac-Man, se mueve hacia él, de lo contrario, sigue un camino accesible.

        Su hizo apoyo de IA para el calculo de la posicion proyectada
        """
        self.move_timer += 1 / 60  # Incrementar el temporizador por cada frame (60 FPS)

        if self.move_timer >= self.move_interval:
            self.move_timer = 0  # Reiniciar el temporizador

            posicion_pacman = self.model.getCurrentPlayer().getPosition()
            direccion_pacman = self.model.getCurrentPlayer().getDirection()
            grafo = self.model.getLaberinto().tablero

            posicion_pacman = self.model.getLaberinto().check_tunnel(posicion_pacman)

            posicion_proyectada = posicion_pacman
            for _ in range(3):
                if direccion_pacman == 'UP':
                    posicion_proyectada = (posicion_proyectada[0] - 1, posicion_proyectada[1])
                    posicion_proyectada_izquierda = (posicion_proyectada[0], posicion_proyectada[1] - 1)
                    if self.model.getLaberinto().tablero.has_node(posicion_proyectada_izquierda):
                        posicion_proyectada = posicion_proyectada_izquierda
                        break
                elif direccion_pacman == 'DOWN':
                    posicion_proyectada = (posicion_proyectada[0] + 1, posicion_proyectada[1])
                elif direccion_pacman == 'LEFT':
                    posicion_proyectada = (posicion_proyectada[0], posicion_proyectada[1] - 1)
                elif direccion_pacman == 'RIGHT':
                    posicion_proyectada = (posicion_proyectada[0], posicion_proyectada[1] + 1)

                if not self.model.getLaberinto().tablero.has_node(posicion_proyectada):
                    posicion_proyectada = posicion_pacman
                    break

            nodo_dato = grafo.nodes.get(posicion_proyectada, {}).get('tipo', None)

            if nodo_dato == 'pared' or nodo_dato is None:
                adyacentes = list(grafo.neighbors(self.node_position))
                if adyacentes:
                    distancia_minima = float('inf')
                    nodo_adyacente_cercano = None
                    for nodo in adyacentes:
                        distancia = nx.shortest_path_length(grafo, nodo, posicion_pacman)
                        if distancia < distancia_minima:
                            distancia_minima = distancia
                            nodo_adyacente_cercano = nodo
                    posicion_objetivo = nodo_adyacente_cercano
                else:
                    posicion_objetivo = self.node_position
            elif nodo_dato == 'tunnel':
                posicion_objetivo = self.model.getLaberinto().check_tunnel(posicion_proyectada)
            elif nodo_dato in ('pacdot', 'camino', 'bonus', 'fruit'):
                posicion_objetivo = posicion_proyectada
            else:
                adyacentes = list(grafo.neighbors(self.node_position))
                if adyacentes:
                    distancia_minima = float('inf')
                    nodo_adyacente_cercano = None
                    for nodo in adyacentes:
                        distancia = nx.shortest_path_length(grafo, nodo, posicion_pacman)
                        if distancia < distancia_minima:
                            distancia_minima = distancia
                            nodo_adyacente_cercano = nodo
                    posicion_objetivo = nodo_adyacente_cercano
                else:
                    posicion_objetivo = self.node_position

            distancia_a_pacman = nx.shortest_path_length(grafo, self.node_position, posicion_pacman)

            if distancia_a_pacman <= 3:
                posicion_objetivo = posicion_pacman

            if posicion_objetivo:
                if posicion_objetivo == self.node_position:
                    return

                try:
                    path = nx.shortest_path(grafo, source=self.node_position, target=posicion_objetivo)
                    if len(path) > 1:
                        self.node_position = path[1]
                except nx.NetworkXNoPath:
                    pass

            self.node_position = self.model.getLaberinto().check_tunnel(self.node_position)

    def Pinky_behave(self):
        if self.mode_behave == "scatter":
            self.scatter_mode()
        elif self.mode_behave == "chase":
            self.chase_modeP()
        elif self.mode_behave == "frightened":
            self.frightened_mode()
        elif self.mode_behave == "respawn":
            self.ghost_respawn()











