import os
import pygame
import manager
from classes.map import map_model
from flask import Flask, jsonify, request
from constants import screen, display, clock
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({'content': 'Floresta Inteligente'})

@app.route('/fire', methods=['POST'])
def fire():
    data = request.json

    s1 = data.get('s1', False)
    s2 = data.get('s2', False)
    s3 = data.get('s3', False)
    s4 = data.get('s4', False)

    map_model.toggle_fire_focus(s1, s2, s3, s4)
    return jsonify({'status': 'ok'})

class Main:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse click at:", pygame.mouse.get_pos())

            manager.run_activity()
            display.blit(screen, (0, 0))
            pygame.display.update()
            clock.tick(60)

def run_flask():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    Main().run()
