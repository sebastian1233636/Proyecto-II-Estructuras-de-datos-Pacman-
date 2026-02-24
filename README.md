# Pac-Man(2024)

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de una versión del clásico juego de arcade **Pac-Man**. El juego incluye todos los elementos esenciales, como pacdots, frutas, fantasmas, atajos en el laberinto y píldoras de poder. Este proyecto fue realizado durante el curso de **Estructuras de Datos** de la **Universidad Nacional de Costa Rica (UNA)**.

El objetivo principal del proyecto es implementar la inteligencia artificial de los fantasmas utilizando grafos, así como optimizar el rendimiento del juego mediante técnicas de hashing.

## Integrantes del Proyecto

- **Sebastián Álvarez Gómez**
- **Anthony Li Perera**

## Características Principales

- **Inteligencia Artificial de los Fantasmas**:
  - Implementación de comportamientos de fantasmas:
    - **Blinky (Rojo)**: Persigue directamente a Pac-Man.
    - **Pinky (Rosa)**: Predice la dirección de Pac-Man.
    - **Inky (Cian)**: Calcula su objetivo basándose en la posición de Pac-Man y Blinky.
    - **Clyde (Naranja)**: Comportamiento errático.
  - Modos de comportamiento: Persecución, Dispersión y Asustado.
  
- **Algoritmos de Búsqueda**:
  - Uso de BFS (Breadth-First Search) o DFS (Depth-First Search) para encontrar el camino más corto hacia Pac-Man.
  - Implementación de un sistema de pesos en los caminos para decisiones más inteligentes.

- **Optimización mediante Hashing**:
  - Gestión de elementos del juego (puntos, frutas, etc.) usando tablas hash para acceso rápido.
  - Detección de colisiones entre Pac-Man y los fantasmas mediante hashing.
  - Almacenamiento de rutas óptimas para los fantasmas utilizando técnicas de hashing.

- **Guardado y Recuperación de Estado**:
  - Permite guardar el estado del juego en cualquier momento y recuperarlo al reiniciar la aplicación.
