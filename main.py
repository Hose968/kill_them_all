from __future__ import annotations

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
pygame.init()

import argparse

from models.internal.configs import GameConfig
from game import Game

def get_max_screen_resolution():
    info = pygame.display.Info()
    return info.current_w, info.current_h

def get_args():
    parser = argparse.ArgumentParser(
        prog="KillThemAll", 
        description="KillThemAll: is a zombie shooter game written in python, pygame", 
        allow_abbrev=False
    )
    parser.add_argument("--screen_height", type=int, default=720, help="Screen height")
    parser.add_argument("--screen_width", type=int, default=1280, help="Screen width")
    parser.add_argument("--game_fps", type=int, default=30, help="Game fps")
    parser.add_argument("--full_screen", action='store_true', help="Full screen switch")

    args = parser.parse_args()

    if args.full_screen:
        args.screen_width, args.screen_height = get_max_screen_resolution()

    return args

def main():
    args = get_args()
    
    configs = GameConfig(
        args.screen_width, 
        args.screen_height, 
        args.game_fps
    )
    
    game = Game(configs)
    game.run()



if __name__ == "__main__":
    main()