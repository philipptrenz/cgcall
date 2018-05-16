#!/usr/bin/env python

import os, subprocess, time
from ftplib import FTP

ffmpeg_cmd = 'ffmpeg -i audio/latest.mp3 -ac 1 -ar 22000 -acodec pcm_s16le -y audio/latest_new.wav'

def read_config():


	config = {'server': None, 'user': None, 'password': None, 'frequency': None}

	ftp_user =		""
	ftp_pwd = 		""
	ftp_server =	""
	ftp_check_frequency = 	30

	with open('cgcall.cfg', 'r') as f:
		for line in f:
			line = line.rstrip()  # remove '\n' at end of line
				
			if line.startswith('fd='):
				config['server'] = line.replace('fd=', '').replace(' ', '')

			if line.startswith('fu='):
				config['user'] = line.replace('fu=', '').replace(' ', '')

			if line.startswith('fp='):
				config['password'] = line.replace('fp=', '').replace(' ', '')

			if line.startswith('ff='):
				config['frequency'] = int(line.replace('ff=', '').replace(' ', ''))

	return config

def is_new_recording_available(config):
	print("checking for new recording ...")

	try:
		latest = ""

		with FTP(config['server']) as ftp:
			ftp.login(user=config['user'], passwd=config['password'])
			files = ftp.nlst()

			for f in files:
				if not f.endswith(".mp3"):
					files.remove(f)

			files.sort(reverse=True)
			
			latest = files[0]

			if not os.path.exists('.latest'):

				with open('.latest', 'a') as f:
					f.write(latest)
				get_latest(config, latest)
				return True
				
			else:

				with open('.latest') as f:
					first_line = f.readline()
					if (latest[:10] != first_line[:10]):
						get_latest(config, latest)
						return True
					else:
						return False
	except:
		print("Accessing ftp failed, trying again in normal interval")
		return False



def get_latest(config, latest):

	print("loading latest recording via ftp ...")

	try:
		with FTP(config['server']) as ftp:
			ftp.login(user=config['user'], passwd=config['password'])

			ftp.retrbinary('RETR '+latest, open('audio/latest.mp3', 'wb').write)

			print("received")

			ffmpeg_cmd_arr = ffmpeg_cmd.split(" ")
			res = subprocess.call(ffmpeg_cmd, shell=True)

			if (res == 0):

				os.remove("audio/latest.mp3")

				print("converted")
				
				print("done.")
				return True

			else:
				print('ffmpeg conversion failed!')
				return False
	except:
		print("Accessing ftp failed, trying again in normal interval")
		return False

if __name__ == "__main__":

	print("read config ...")

	config = read_config()

	print("running ...")

	latest = ""
	new_ready = False
	start_time = time.time()

	# initial lookup
	new_ready = is_new_recording_available(config)

	while(True):

		# check if there is a new recording already 
		# downloaded and no currently ongoing call
		if (new_ready and not os.path.exists('.activecall')):

			if os.path.exists("audio/latest.wav"):
				os.remove("audio/latest.wav")
			os.rename("audio/latest_new.wav", "audio/latest.wav")

			print('New recording got copied and is now available')
			
			new_ready = False
			start_time = time.time() # reset

		# check for new recording in intercal
		elif (time.time() - start_time > config['frequency'] * 60):

			new_ready = is_new_recording_available(config)
			start_time = time.time() # reset

		else:

			time.sleep(30) # 30 secs

	