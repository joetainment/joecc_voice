JoeccVoice
===========
### Easy Voice Recognition Software for Controlling a Computer by Voice.

<br>

Free and Open Source, as well as being Cross Platform (Windows/Linux/Mac)
the aim of this software is to be able to perform arbitrary keyboard input,
as well as provide speech to text functionality.

( Programmers should note the actual Python module name is:  joecc_voice )

<br><br>

About This Software
=========================

JoeccVoice let's users control computers by voice recognition with an easy to use graphical user interface.   (Note that it currently makes use of Google's voice recognition or Windows SAPI to do the actual speech to text transcriptions. Hopefully a viable open source backend will exist in the future, perhaps Mozilla's voice project.)

JoeccVoice is essentially just short for "Joseph Cameron Crawford's Voice Recognition Software". 
I (the original writer of this software) am named Joseph Cameron Crawford, 
and I often use Joecc as an abbreviation, similar to initials. 
I prefix most of my code with Joecc. I originally created this app for my own use, 
to help me use computers, since I have major joint problems which make typing difficult.
Later on I realized other may find it useful, so I have made it available to the public.

It should be noted that I have not written the underlying speech to text engines, 
which do the actual voice recognition.  All I've done is created an easy user interface, 
which allows users to control the systems and do simple things like typing by voice..

Hopefully someone finds this software useful.

Sincerely,

Joe Crawford

<br>


Setup and Requirements
=============

You need the following to run JoeccVoice:
Python 3.5 or higher
PySide2
pynput
pyaudio
SpeechRecognition



Note: pyaudio requires the portaudio libraries and header files, 
usually in a dev package on most Linux distributions.






Linux
---------------------

On Debian and Ubuntu Systems, the following commands should
work to install the required dependencies:
```
sudo apt install portaudio19-dev python3-pip
pip3 install -U --user PySide2 pyaudio SpeechRecognition pynput
```


You can run the program itself, from its folder, with the command:
```
python3 JoeccVoice.py
```

If you are using other distributions, you can follow similar steps,
using whatever package manager you distro has available.



Windows
-------------------

I am working on an automated installer for JoeccVoice on Windows.
Currently it's a bit of a pain to setup, since Windows doesn't ship with
Python by default.

Anyway...

On windows you can usually install the dependencies with something like:
```
python -m pip install -U --user PySide2 pyaudio SpeechRecognition pynput
```

You can run the program itself, from its folder, with the command:
```
python JoeccVoice.py
```
