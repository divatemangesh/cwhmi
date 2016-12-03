

from flask.ext.socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event
from base64 import b64encode
import cv2
import numpy as np
# import thread as LibThread

__author__ = 'kake'

class Server(Thread):
    def __init__(self, __name__):
        Thread.__init__(self)
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'secret!'
        self.app.config['DEBUG'] = False
        self.socketio = SocketIO(self.app)

    def run(self):
        print 'starting run in Server'
        self.socketio.run(self.app, port=5001, host='0.0.0.0')
        print 'ERROR ---------------------socket io exited'

server = Server(__name__)

thread = Thread()
thread_stop_event = Event()

class UpdateWeb(Thread):
    def __init__(self):
        self.delay = 3
        Thread.__init__(self)

    def Plot(self, x, y):
        x = list(x)
        y = list(y)
        number = {'x': x, 'y': y, 'type': 'scatter' }
        server.socketio.emit('newnumber', {'number': number}, namespace='/test')

    def Imshow(self, im, quality):
        # if len(quality) == 0:
        #     quality = 10
        self._encodeStatus, self._imJpeg = cv2.imencode('.jpg', im, [cv2.IMWRITE_JPEG_QUALITY, quality])
        self._imJpegEncoded = b64encode(self._imJpeg)
        server.socketio.emit('newImage', {'imageRgb':self._imJpegEncoded}, namespace='/test')

    def run(self):
        pass
        # self.randomNumberGenerator()
        # while True:
        #     print 'testing thread'
        #     sleep(2)

@server.app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@server.socketio.on('connect', namespace='/test')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.isAlive():
        print "Starting Thread"
        # thread = RandomThread()
        thread = UpdateWeb()
        # thread.start()

@server.socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

def Trash(fn, var):
    LibThread.start_new_thread(fn, (var,))
    while True:
        pass

if __name__ == '__main__':
    # LibThread.start_new_thread(socketio.run, (app,))
    # Trash(socketio.run, app)

    # rt = RandomThread()
    # rt.run()
    server.start()

    rt = UpdateWeb()

    # server.socketio.run(server.app)
    # socketio.run(app)
    # pass
    # while True:
    #     pass