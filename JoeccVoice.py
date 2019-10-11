#!/usr/bin/env python3  
########
##
##
"""
################
Goals/Tasks/ToDo:

Properly formed git project


Press for all keyboard keys and modifier combinations
Use control alt shift as order
Use alternates for symbols that normally require shift


Console only version or command line switch

Create some kind of sequence or button combo to turn off
all voice recognition services.
Possibly add a toggle
hotkeyReaction


Check properly for presence of pyaudio
rather than crashing when checkbox clicked


Parse arguments to use command line only

Startup Checks
  Check for correct python on version    - done
  Check for dependencies    - partly done
  optionally elevate    - not done, under consideration


Use other Python files for configuration
Have additional Python files for user configuration

Add support for creating mouse events:
  Control mouse, Control keyboard
  left click, right-click, middle click,
  hold and release of all
  Double click for all
  scroll wheel With repeats

  Jump commands for mouse, coordinate-based positioning commands for mouse


option to send different types of commands to different services,
separate Queues into buckets, 
Buckets: Direct commands, type, recognize, press, repeat,


Standalone, packaged, or otherwise easy to download and run Executable
via PyInstaller or something

Functions for corrections by using copy and paste
Optional clipboard history and Quick insert of former clipboard items

consider using recognize_google(audio, show_all=True)

allow dual recognizers for type and speech, google and winspeech


correction pop up?
it would have to be able to either draw on top or switch back to active app
https://stackoverflow.com/questions/10266281/obtain-active-window-using-python

control and windows key
toggles speech recognition listening well


"""
######## Note that most imports are done *way* later, see way below
######## this is because...
########
######## Several stages of preparation happen early on
######## before starting to run much code.
########   (Testing for dependencies, versions,
########    system platform requirements, etc)



######## stage 1a ########
import os, sys
from _collections import OrderedDict
if __name__ == "__main__":
    os.chdir(    os.path.dirname( os.path.abspath(sys.argv[0]) )    )

######## stage 1b ########
if __name__ == "__main__":
    try:
        assert sys.version_info >= (3, 5)
    except:
        print( sys.version )
        print("This program can not run, requires Python 3.5 or higher.")
        sys.exit(1)



######## stage 1c #############
#### Ensure needed deps are installed
import subprocess, sys

def pip_install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", "-U", "--user", package,])



"""
## Auto download of modules is currently disabled, since it needs work
## first pass to ensure dependencies are installed, such as:
## SpeechRecognition, pynput, payaudio and PySide2
##
## and possibly autoinstall them
## 
#
# Example
print( "Checking for required modules and downloading with pip  if necessary.")
if __name__ == '__main__':
    try:
        import PySide2
    except:
        ## should add something for confirmation
        ## are notice of delay while downloading/setting up
        print("Downloading and installing PySide2")
        pip_install('PySide2')
        import PySide2




if __name__ == '__main__':
    try:
        import pyaudio
    except:
        ## should add something for confirmation
        ## are notice of delay while downloading/setting up
        print("Downloading and installing pyaudio")
        print("you may need to install the package portaudio19-dev")
        pip_install('pyaudio')
        ## later import of Speech Recogntion
        ## should cover this import indirectly
        ## see Listener*.py modules
        ##      import speech_recognition 


        
if __name__ == '__main__':
    try:
        import SpeechRecognition
    except:
        ## should add something for confirmation
        ## are notice of delay while downloading/setting up
        print("Downloading and installing SpeechRecognition")
        pip_install('SpeechRecognition')
        import speech_recognition

         
        
        
if __name__ == '__main__':
    try:
        import pynput
    except:
        ## should add something for confirmation
        ## are notice of delay while downloading/setting up
        print("Downloading and installing pynput")
        pip_install('pynput')
        import pynput
"""



 

#### Modules import fix?  Disabled, might be useful later
## from pkgutil import extend_path
##__path__ = extend_path(__path__, __name__)



#### Import substandard Python Modules
#import multiprocessing

import sys, os, queue, subprocess, time, threading, traceback
from queue import Queue
#from multiprocessing.pool import job_counter


#### Imports for input emulation
import pynput
from pynput.keyboard import Key, Controller


#### Imports for Voice recognition
#import winspeech
#import speech_recognition as sr

######## impot own project submodules
#### Import Listeners
isModWinSpeechAvailable=False
try:
    import ListenerThreadWinspeech
    isModWinSpeechAvailable=True
except:
    isModWinSpeechAvailable=False    

import ListenerThreadGoogle
#import ListenerMprocWinspeech

#### Import Qtui
import Qtui  ##  rename and reorganize this later, as it might conflict

#### Import ConfigurationManager
import conf



class ThreadLockObj( object ):
    # x = property(__get_x, __set_x)  ## getter/setter property to use later
    
    def __init__(self, obj):
        self.__lock = threading.RLock()
        with self.__lock:
            self.__obj = obj
        
    def __enter__( self ):
        self.__lock.acquire()
        return self.__obj       
        
    def __exit__( self, type, value, traceback ):
        self.__lock.release()


class Job():
    def __init__(self, thread=None, data=None, queue=None, doDefaultData=False ):
        self.thread=thread
        #if queue==None:
        self.queue = queue
        if data==None and doDefaultData:
            data = {
                'active': True,
                'doFuncQuit': False,
            }
        self.data = ThreadLockObj(data)
    

class JoeccVoiceApp():
    @classmethod
    def isModWinSpeechAvailable(cls):
        return isModWinSpeechAvailable
    
    def __init__( self ):
        self.qapp = None
        self.qtui = None
        self.jobs = {}
        self.threadQueue = queue.Queue()
        self.hotkeyQueue = queue.Queue()
        self.conf = conf.Conf()
        
        self.activeOnHeard = True
        
        
        
        self.kb = Controller()
        
        ## *** all this keyboard stuff should go in a submodule later...
        self.kbListener = pynput.keyboard.Listener(
            on_press=self.kbListenerOnRelease,
            on_release=self.kbListenerOnRelease,    
        )
        self.kbListener.start()
        
    def kbListenerOnRelease(self, key ):
        self.hotkeyQueue.put(key)
        
    def hotkeyReaction(self, key ):
        if key == pynput.keyboard.Key.esc:
            tmp=0
            #### need to add a better hotkey method to turn all off
            #self.qtui.deactivateServices()
            #self.stopJobs()
        
    def run( self, qtui=True ):
        
        ## default to an error code
        exitCode = 1; 
        
        ## Create UI
        if qtui == True:
            self.qtuiInit()
            exitCode = self.qtuiExec()
        self.quit() ## self.stopJobs()  is covered by this
        
        return exitCode
            
        
    def qtuiInit(self): 
        
        #self.qappClass = QtWidgets.QApplication
        self.qapp = Qtui.Qtui.GetQapp( sys.argv )
        self.qtui = Qtui.Qtui( papp = self )
        
        
        
    def qtuiExec(self):         
        exitCode = self.qapp.exec_()
        return exitCode

    
    def exit(self):
        self.quit()
            
    def quit(self):
        self.kbListener.stop( )
        self.stopJobs()             
        #self.qapp.quit()      


        
    def stopJobs(self):
        self.stopJobsThreads()
                   
    def stopJobsThreads(self):
        ## tell job to quit
        ## Join jobs and remove from dicts
        rmKeys =[]
        ## collect keys
        for key, job in self.jobs.items():
            with job.data as d:
                d['doFuncQuit']=True
                time.sleep(0.1)
            job.thread.join(1) ## 1 second timeout
            rmKeys.append(key)
        ## remove from dict    
        for key in rmKeys:
            del self.jobs[ key ]
        
        ## Make sure the job list is empty
        assert len(self.jobs)==0
        
        ## slight delay for the multithreading, though probably unnecessary
        time.sleep(0.5)


            
    def startJobWinspeech(self):
        if self.qtui != None: self.qtui.appendToTextHeard( 
            "Winspeech service starting..."
        )   
        if not 'winspeech' in self.jobs:
            if isModWinSpeechAvailable:
                ## winspeech job
                job = Job(
                    queue=self.threadQueue,
                    doDefaultData=True,
                )
                job.thread=threading.Thread(
                        target = ListenerThreadWinspeech.worker,
                        daemon=True,
                        args=(
                            job.queue, job.data, None
        
                        ),
                        kwargs = {},
                )
                job.thread.start()
                self.jobs['winspeech'] = job


            
    def startJobGoogle(self):
        if self.qtui != None: self.qtui.appendToTextHeard( 
            "Google service starting..."
        )
        if not 'google' in self.jobs:
            job = Job(
                queue=self.threadQueue,
                doDefaultData=True,
            )
            job.thread = threading.Thread(
                target = ListenerThreadGoogle.worker,
                daemon=True,
                args=(
                    job.queue, job.data, None
                ),
                kwargs = {},
            )
            job.thread.start()
            self.jobs['google'] = job
            
               
    def stopJob(self, jobName ):
        if jobName in self.jobs:
            job = self.jobs[jobName]
            with job.data as d:
                d['doFuncQuit']=True
                time.sleep(0.1)
            job.thread.join(1) ## 1 second timeout
            del self.jobs[jobName]
            return True
        return False
    
    def stopJobWinspeech(self):
        if self.qtui != None: self.qtui.appendToTextHeard( 
            "Winspeech service stopping..."
        )
        self.stopJob('winspeech')
    
    def stopJobGoogle(self):
        if self.qtui != None: self.qtui.appendToTextHeard(
            "Google service stopping..."
        )
        self.stopJob('google')
        


               
    def update(self):
        
        while not self.hotkeyQueue.empty():
            hotkey = self.hotkeyQueue.get()
            self.hotkeyReaction(hotkey)            
            
        
        while not self.threadQueue.empty():
            ## qv means Queue Value
            qv = self.threadQueue.get()
            self.qtui.appendToTextHeard( "heard: " + qv )
            
            #if any( map( qv.lower().startswith, recogCmds)  ):
            
            
            ## qvl means Queue Value Lowercase
            qvl = qv.lower().strip()
            
            handled = False
            voiceControlStopPhrases = ['voice control stop',
                'voice controls top','voice controlled stop']
            voiceControlStartPhrases = ['voice control start',
                'voice controls start','voice controlled start']
            voiceControlSwitchPhrases = ['voice control switch',
                'voice controls switch','voice controlled switch']
            
            if qvl in voiceControlStopPhrases:
                handled = True
                self.activeOnHeard = False
                self.qtui.appendToTextHeard("action: voice control stop")
            elif qvl in voiceControlStartPhrases:
                handled = True
                self.activeOnHeard = True
                self.qtui.appendToTextHeard("action: voice control start")
            elif qvl in voiceControlSwitchPhrases:
                handled = True
                self.kb.press( pynput.keyboard.Key.ctrl_l )
                self.kb.press( pynput.keyboard.Key.cmd_l )
                time.sleep(0.03)
                self.kb.release( pynput.keyboard.Key.cmd_l)
                self.kb.release( pynput.keyboard.Key.ctrl_l )
                
                if self.activeOnHeard:
                    self.activeOnHeard = False
                else:
                    self.activeOnHeard = True
                    
            if not self.activeOnHeard:
                handled = True
            
            
            if not handled:
                googleServicePhrases = ['service with google',
                    'service with cobol',
                    'service with cool',
                    'service with goebel',
                    'service with gopal',
                    'service with to','service with two',]
                if qvl in googleServicePhrases:
                    handled = True
                    self.serviceSwitchToGoogle()
                    
            if not handled:
                winspeechServicePhrases = ['service with win speech',
                    'service with wind speech',
                    'surface with wind speech',
                    'service with winspeech']
                if qvl in winspeechServicePhrases:
                    handled = True
                    self.serviceSwitchToWinspeech()
                                    
            if not handled:
                deactivateServicesPhrases = ['deactivate services',]
                if qvl in deactivateServicesPhrases:
                    handled = True
                    self.serviceDeactivate()
                                              
            
            ## Replace this with something That uses 
            ## a list and lanbda functions  
            if not handled:
                handled = self.recogCheckForRecognizeCmd(qvl)
            
            if not handled:
                handled = self.recogCheckForVoiceCmd(qvl)
            
            if not handled:
                handled = self.recogCheckForTypeCmd( qvl )
            
            if not handled:
                self.qtui.appendToTextHeard( 
                    "No actions for given command."
                )


    def serviceDeactivate(self):
        self.qtui.deactivateServices()
        self.stopJobs()
        
    def serviceSwitchToGoogle(self):
        self.qtui.deactivateServices()
        self.stopJobs()
        self.qtui.activateServiceGoogle()
                
    def serviceSwitchToWinspeech(self):
        self.qtui.deactivateServices()
        self.stopJobs()
        self.qtui.activateServiceWinspeech()



    def recogCheckForVoiceCmd(self, queueValueLowercase):
        ## this function is not yet implemented
    
        ## qvl means Queue Value Lowercase
        qvl = queueValueLowercase
        return False
    


                
    def recogCheckForRecognizeCmd(self, queueValueLowercase):
        ## qvl means Queue Value Lowercase
        qvl = queueValueLowercase
        foundCmd = None
        
        ## split to 3 part tuple
        ##   at the first occurrence of the given argument
        ## will return a 3-tuple with the given argument as the middle value
        pt = qvl.partition(' ')
        ptStart,ptSplitter,ptEnd = pt

        recogCmds = [
            'recognize',
            'recognized',
            'to recognize',
            'to recognized',
            'and to recognize',
            'and to recognized',
            'recognition',
        ]
                    ## old idea for capped recog, removed for now
                    #recogCapCmds = [
                    #    'recognize cap',
                    #    'recognized cap',
                    #]
                    
        recogCmds = recogCmds + [s + '.' for s in recogCmds]
        recogCmdIndex = None
        recogCmd = None
        
        qvlForRecog = qvl
        
        ## check startswith 'capital' , if so then flag
        capitalForRecog = 'capital '  ## has space at end
        capitalShouldRecogStartCapped = False
        if qvlForRecog.startswith(capitalForRecog):
            qvlForRecog = qvlForRecog[
                len( capitalForRecog )
            :]
            capitalShouldRecogStartCapped = True
            
        
        ## search  for recognize-like cmd in qvl start
        for  i, cmd  in enumerate(recogCmds):
            if qvlForRecog.startswith(cmd):
                recogCmdIndex = i
                recogCmd = cmd
        
        if recogCmd != None:
            ## was totally wrong -tt = pt[2]
            sl = len(recogCmd)
            tt = qvlForRecog[sl+1:]  ## +1 for space after word
            self.qtui.appendToTextHeard( 
                "Performing: speech recognized dictation"
            )
            if capitalShouldRecogStartCapped:
                self.qtui.appendToTextHeard( "(capitlized)" )
                #if recogCmd == 'recognition':
                tt = tt[0].upper() + tt[1:]
            ## Type recognized dictated text 
            self.kb.type(  tt  )
            return True
        
        ##  recogCmd == None
        ##  Since we didn't return from the if 
        return False
            
        #### make recog check for "recognize."    
        #### to account for situations where first char after
        #### recognize directive isn't a space
        
        
        
        
        #### several more cases, currently experimental
        """
        elif 'space' in qvl:
            for word in qvl.split():
                if word=='space':
                    self.kb.type(  ' '  )

        elif 'enter' in qvl:
            for word in qvl.split():
                if word=='enter':
                    self.kb.type(  '\n'  )

        elif qvl.startswith('.'):
            for symb in qvl:
                if symb=='.':
                    self.kb.type(  symb  )

        #elif 'exclaimation' in qvl:
        #    for word in qvl.split():
        #        if word=='enter':
        #            self.kb.type(  '\n'  )
        """

    def recogCheckForTypeCmd(self, queueValueLowercase):
        ## qvl means Queue Value Lowercase
        qvl = queueValueLowercase
        
        kb =  self.kb
            
        ### start of "type" command related stuff
        phrase = qvl
        phrase = phrase.strip().lower()
        phrase = phrase.replace("?", " ? " )
        phrase = phrase.replace("!", " ! " )
        phrase = phrase.replace("'", " ' " )
        phrase = phrase.replace(".", " . " )
        phrase = phrase.replace(",", " , " )
        phrase = phrase.replace(";", " ; " )
        phrase = phrase.replace(":", " : " )
        phrase = phrase.replace("\t", " tab " )
        
        
        for k,v in conf.Conf.s2w.items():
            phrase = phrase.replace(  k, v   )
            

        
        def sub(t):
            t = t.lower()
            l = t.split(" ")
            l = [ v.strip() for v in l if v.strip() ]
            
            for i, v  in enumerate( l ):
                if v in conf.Conf.map.keys():
                    try:
                        l[i] = conf.Conf.map[v] #map[v]
                    except:
                        print( traceback.format_exc() )
                        print( "l: ", l,  " type l: ", type(l)    )
                        print( "i: ", i,  " type i: ", type(i)    )
                        print( "v: ", v,  " type v: ", type(v)    )
                        print( "map: ", map,  " type map: ", type(map)    )
                        
            #t
            return l    
        ps = sub(phrase)
        
        tysh = 'typeshift'
        
        if ps[0] == tysh:
            ps[0] = 'type'
            ps.insert(1,'shift')
        
        if len(ps) > 0:
            try:
                if ps[1] == 'of':
                    del ps[1]
            except:
                handled = True
                print( traceback.format_exc()  )
                print( 'continuing...')
            

        
        words = ps
        
        typeshift = False

        typeCmdVariants = [ 'type', 'typed', 'tape', 'taped', 'taper',]
        if words[0] in typeCmdVariants:
            words.pop(0)
        elif words[0] in ['for','to']  and words[1] in typeCmdVariants:
            for i in range(2):
                words.pop(0)
        else:
            words=[]
            return False

        if len(words)>0:
            self.qtui.appendToTextHeard( 
                "Performing simulated typing action..."
            )
        else:
            return False
            
        
        
        #if active == True  and  phraseOk  and  (not doRecog):    
        for i, word in enumerate(words):
                
            try:
                numbers = int( word )
                #if word > -9  and  word < 9:
                #tmp = str(tmp)
                #word = tmp
                
            except:
                numbers = None
            if type(word)==type(" "):
                word = word.replace( ' ', '' )
            def prel(key):
                kb.press( key )
                kb.release( key )
            if word == 'backspace':
                tmp = pynput.keyboard.Key.backspace
                kb.press( tmp )
                kb.release( tmp )
            elif word in ['tab','\t']:
                tmp = pynput.keyboard.Key.tab
                kb.press( tmp )
                kb.release( tmp )
            elif word in ['escape']:
                tmp = pynput.keyboard.Key.escape
                kb.press( tmp )
                kb.release( tmp )
            elif numbers != None:  #type(word)==type(9):
                kb.type( str(numbers) )
            elif word in conf.Conf.w2kb.keys():                    
                #print(  word )
                doShift=False
                if i>0:
                    if words[i-1] in ['shift','shifts','ships', 'cap', 'kappa']:
                        doShift=True
                if doShift==True:
                    kb.press( pynput.keyboard.Key.shift_l)
                
                kb.type( conf.Conf.w2kb[word] )
                
                if doShift==True:
                    kb.release( pynput.keyboard.Key.shift_l)
                
            elif word in [
                '', 'a', 'of', 'the', 'shift',
                'shifts','ships', 'cap', 'kappa',
                ]:
                
                print('emptyWord')
            else:
                print(  'phrase: ' + phrase )
                print(  'word: ' + word )
                ##print( [ w for w in phrase ] )
                print( words )
                self.qtui.appendToTextHeard( 
                    "A key couldn't be recognized"
                )
                kb.type( '*' )
                time.sleep(0.1)
                kb.press( pynput.keyboard.Key.backspace )
                time.sleep(0.031)
                kb.release( pynput.keyboard.Key.backspace )
        return True

         

                    
## Run only if called directly, mostly for future proofing
## although this app may have no other use case.
if __name__ == '__main__':
    ## Initialise which contains qapp, a QApplication
    ## which runs the event loop
    app = JoeccVoiceApp()
    exitCode = app.run()   ## calls exec_ indirectly
    sys.exit( exitCode )   ## exit code essentially from exec_

