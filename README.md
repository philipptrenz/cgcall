# cgcall – A SIP audio player for audio records

This software provides a "softphone", a Voice over IP software client, to provide a audio player for WAV-files via telephony running on a Raspberry Pi.

Dependencies:
- PJSUA API (http://www.pjsip.org)
- eSpeak (http://espeak.sourceforge.net)

Based on https://github.com/binerry/RaspberryPi/

## Installation on Raspberry Pi 3

```bash
# Install dependencies
sudo apt install autoconf checkinstall libgpac-dev libmp3lame-dev libopencore-amrnb-dev \
libopencore-amrwb-dev libtheora-dev libvorbis-dev yasm zlib1g-dev libsdl-sound1.2-dev \
libportaudio-dev espeak espeak-data git python3 ffmpeg

# Install pjsip
wget http://www.pjsip.org/release/2.7.2/pjproject-2.7.2.tar.bz2
tar xvfj pjproject-2.7.2.tar.bz2
cd pjproject-2.7.2/
./configure --disable-video --disable-libwebrtc
make dep && make clean && make
sudo make install

cd ~/

# Build cgcall
git clone https://github.com/philipptrenz/cgcall.git
cd cgcall
make
```


## Usage

```cgcall --config-file=/path/to/cgcall.cfg [-s 1]```

## Commandline

* --config-file=string   _Set config file_   

Optional:

* -s=int       _Silent mode (0/1)_   

## Config file

### Mandatory options  

* sd=string   _Set sip provider domain._   
* su=string   _Set sip username._   
* sp=string   _Set sip password._   
* ln=string   _Language identifier for espeak TTS (e.g. en = English or de = German)._

* tts=string  _String to be read as a intro message_

### _and at least one dtmf configuration (X = dtmf-key index)_   

* dtmf.X.active=int           _Set dtmf-setting active (0/1)._   
* dtmf.X.description=string   _Set description._   
* dtmf.X.tts-intro=string     _Set tts intro._   
* dtmf.X.tts-answer=string    _Set tts answer._   
* dtmf.X.cmd=string           _Set shell command._   

### Optional

* rc=int      _Record call (0=no/1=yes)_   
* af=string   _announcement wav file to play; tts will not be read, if this parameter is given. File format is Microsoft WAV (signed 16 bit) Mono, 22 kHz;_ 
* cmd=string  _command to check if the call should be taken; the wildcard # will be replaced with the calling phone number; should return a "1" as first char, if you want to take the call._
* am=string   _aftermath: command to be executed after call ends. Will be called with two parameters: $1 = Phone number $2 = recorded file name_

Hint: Audio files can be converted via `ffmpeg -i inputfile -ac 1 -ar 22000 -acodec pcm_s16le output.wav`

**A sample configuration can be found in cgcall-sample.cfg**
  
## Activate cgcall service

```bash
sudo cp scripts/cgcall.sh /etc/init.d/cgcall
sudo update-rc.d cgcall defaults 
```

Now cgcall gets started at boot and can be controlled via `sudo service cgcall [start|stop|status]`

## Raspberry Pi case

I designed a Rasperry Pi 2/3 case to be 3D printed, check it out at [Thingiverse](https://www.thingiverse.com/thing:2918026).
