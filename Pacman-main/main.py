from MVC.Controller import Controller
from MVC.GameView import GameView
from MVC.Model import Model
import pygame

def main():
    pygame.init()
    model = Model()
    controller = Controller(model, None)
    view = GameView(model, controller)
    view.game_loop()
    pygame.quit()

if __name__ == "__main__":
    main()
