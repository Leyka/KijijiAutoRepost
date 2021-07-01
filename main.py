# Built-in libraries
import threading, os

# User libraries
from kijiji_auto_reposter import KijijiAutoReposter
from kijiji_manager.app import create_app

def run_kijiji_manager():
	app = create_app('/config/kijiji-manager.cfg')
	app.run(host='0.0.0.0', port=5000)

def run_kijiji_auto_reposter():
	reposter = KijijiAutoReposter()
	reposter.run()

kijiji_manager_thread = threading.Thread(target=run_kijiji_manager)
reposter_thread = threading.Thread(target=run_kijiji_auto_reposter)

kijiji_manager_thread.start()
reposter_thread.start()

# Wait for thread to finish
kijiji_manager_thread.join()
