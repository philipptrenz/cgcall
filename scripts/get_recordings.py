#!/usr/bin/env python

import sys, os, subprocess, time, datetime
from ftplib import FTP

ffmpeg_cmd = 'ffmpeg -i audio/latest.mp3 -ac 1 -ar 22000 -acodec pcm_s16le -y audio/latest_new.wav'

def read_config():


	config = {'server': None, 'user': None, 'password': None, 'frequency': None}

	ftp_user =		""
	ftp_pwd = 		""
	ftp_server =	""
	ftp_check_frequency = 	30

	with open(sys.argv[1], 'r') as f:
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
	print(datetime.datetime.now(), "Checking for new recording ...")

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
					if (latest != first_line or not os.path.exists("audio/latest.wav")):
						get_latest(config, latest)
						return True
					else:
						return False
	except:
		print(datetime.datetime.now(), "Accessing ftp failed, trying again in normal interval")
		return False



def get_latest(config, latest):

	print(datetime.datetime.now(), "Loading latest recording via ftp ...")

	try:
		with FTP(config['server']) as ftp:
			ftp.login(user=config['user'], passwd=config['password'])

			ftp.retrbinary('RETR '+latest, open('audio/latest.mp3', 'wb').write)

			print(datetime.datetime.now(), "Received new audio file as mp3")

			ffmpeg_cmd_arr = ffmpeg_cmd.split(" ")
			res = subprocess.call(ffmpeg_cmd, shell=True)

			if (res == 0):

				os.remove("audio/latest.mp3")

				print(datetime.datetime.now(), "Converted mp3 to wav")

				return True

			else:
				print(datetime.datetime.now(), 'ffmpeg conversion failed!')
				return False
	except:
		raise

if __name__ == "__main__":

	print(datetime.datetime.now(), "Read config", sys.argv[1], "...")

	config = read_config()

	print(datetime.datetime.now(), "Service running ...")

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

			print(datetime.datetime.now(), 'New recording got copied and is now available')

			new_ready = False
			start_time = time.time() # reset

		# check for new recording in intercal
		elif (time.time() - start_time > config['frequency'] * 60):

			new_ready = is_new_recording_available(config)
			start_time = time.time() # reset

		else:

			time.sleep(30) # 30 secs


