import pygame
import manager
from classes.map import model
from flask import Flask, jsonify, request
from constants import screen, display, clock
import threading

app = Flask(__name__)

@app.route('/')
def index():
    data = {'content': 'Floresta Inteligente'}
    return jsonify(data)

@app.route('/fire', methods=['POST'])
def fire():
    data = request.json
    print(f'[FIRE] {data}')

    model.setFireFocus(data['fireIndex'])

    return jsonify({'status': 'ok'})

class Main:
    def __init__(self):
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    exit()

            manager.run_activity()

            display.blit(screen, (0, 0))
            pygame.display.update()
            clock.tick(60)

def run_flask():
    app.run(host='0.0.0.0')

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    Main().run()
