# Built-in libraries
import os, time, re, random
from urllib.parse import urlparse

# Pipy libraries
from cryptography.fernet import Fernet
import mechanize
from mechanize._http import RobotExclusionError
from bs4 import BeautifulSoup


class KijijiAutoReposter:
	def __init__(self):
		try:
			os.environ['KIJIJI_email']
			os.environ['KIJIJI_password']
			os.environ['KIJIJI_key']
		except KeyError as e:
			print(f'ERROR: Environment variable `{e.args[0]}` not set.', flush=True)
		self.br = mechanize.Browser()
		self.fernet = Fernet(os.environ['KIJIJI_key'].encode())

	def check_kijiji_manager(self):
		try:
			self.br.open('http://127.0.0.1:5000')
		except RobotExclusionError as e:
			return False
		return True

	def wait_for_kijiji_manager(self):
		while not self.check_kijiji_manager():
			delay = 5*60
			print(f'WARNING: Waiting {delay}s before checking Kijiji Manager again.', flush=True)
			time.sleep(delay)

	def login(self):
		self.br.open('http://127.0.0.1:5000')
		if urlparse(self.br.geturl()).path == '/login':
			self.br.select_form(id='login')
			self.br['email'] = self.fernet.decrypt(os.environ['KIJIJI_email'].encode())
			self.br['password'] = self.fernet.decrypt(os.environ['KIJIJI_password'].encode())
			self.br.submit()
		if 'Welcome back,' in str(self.br.response().read()):
			return True
		return False

	def wait_for_login(self):
		while not self.login():
			delay = 5*60
			print(f'WARNING: Waiting {delay}s before logging into Kijiji Manager again.', flush=True)
			time.sleep(delay)

	def repost(self):
		print('INFO: Reposting all ads.', flush=True)
		self.br.open('http://127.0.0.1:5000/repost_all')
		soup = BeautifulSoup(self.br.response().read(), 'html.parser')
		for ad in soup.find('ul', class_='flashes').children:
			ad_id = re.search(r'(?<=[\\/])[0-9]+(?=.xml)', ad.string)
			if ad_id:
				print(f"WARNING: Couldn't repost ad #{ad_id.group(0)}. XML file doesn't exist.", flush=True)

	def wait_for_next_repost(self):
		t = time.localtime()
		time_s = (t.tm_hour*60 + t.tm_min)*60 + t.tm_sec
		delay_s = (8 + (23-8)*random.random()) * 3600 - time_s
		t_next = time.localtime(time.mktime(t)+delay_today+delay_tomorrow)
		print(f'INFO: Next repost will be on {time.strftime("%a, %d %b %Y %H:%M:%S", t_next)}.', flush=True)
		time.sleep(delay_today + delay_tomorrow)

	def run(self):
		while True:
			self.wait_for_next_repost()
			self.wait_for_kijiji_manager()
			self.wait_for_login()
			self.repost()
