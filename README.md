# cgcall – A SIP audio player for event records

This software 


Dependencies:
- PJSUA API (http://www.pjsip.org)
- eSpeak (http://espeak.sourceforge.net)

Forked from: https://github.com/fabianhu/SIP-Pi
Copyright (C) 2012 by _Andre Wussow_, desk@binerry.de
Major changes 2017 by _Fabian Huslik, github.com/fabianhu_


## Installation

```bash
# Install dependencies
sudo apt install autoconf checkinstall libgpac-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev yasm zlib1g-dev libsdl-sound1.2-dev libportaudio-dev

# Install pjsip
wget http://www.pjsip.org/release/2.7.2/pjproject-2.7.2.tar.bz2
tar xvfj pjproject-2.7.2.tar.bz2
cd pjproject-2.7.2/
./configure --disable-video --disable-libwebrtc
make dep && make clean && make
sudo make install

# Optional: Install pjsip python3 bindings
cd pjsip-apps/src
git clone https://github.com/mgwilliams/python3-pjsip.git 
cd python3-pjsip
sudo python3 setup.py install

# Build cgcall
git clone https://github.com/philipptrenz/cgcall.git
cd cgcall
make
```


## Usage

  ```cgcall [options]```

## Commandline

### Mandatory options

* --config-file=string   _Set config file_   

### Optional options

* -s=int       _Silent mode (hide info messages) (0/1)_   

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

### Optional options
  
* rc=int      _Record call (0=no/1=yes)_   
* af=string   _announcement wav file to play; tts will not be read, if this parameter is given. File format is Microsoft WAV (signed 16 bit) Mono, 22 kHz;_ 
* cmd=string  _command to check if the call should be taken; the wildcard # will be replaced with the calling phone number; should return a "1" as first char, if you want to take the call._
* am=string   _aftermath: command to be executed after call ends. Will be called with two parameters: $1 = Phone number $2 = recorded file name_

## a sample configuration can be found in cgcall-sample.cfg
  
## sipserv can be controlled with 

```bash
./cgcall.sh start and 
./cgcall.sh stop
```

## License

This tools are free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This tools are distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.
