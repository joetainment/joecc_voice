
#### Import substandard Python Modules
#import multiprocessing

import sys, os, queue, subprocess, time, threading, traceback
from queue import Queue


#### Imports for Voice recognition
import speech_recognition as sr


## This needs to be moved to conf module ***
class RecogPrefs():
    @classmethod
    def setPrefs(cls, recog):    
        recog.pause_threshold = 0.6  # seconds of non-speaking audio before a phrase is considered complete
        recog.phrase_threshold = 0.8  # minimum seconds of speaking audio before recog
        recog.non_speaking_duration = 0.3  # seconds of non-speaking audio to keep on both sides of the recording
        recog.energy_threshold = 2800
        recog.dynamic_energy_threshold = True
        recog.dynamic_energy_adjustment_ratio = 2000
        
        recog.operation_timeout = 10    


def worker( *args, **kargs ):
    w = ListenerThreadGoogleWorker(
        *args, **kargs
    )
    #return w

def workerForRecog( *args, **kargs ):
    w = GoogleCloudRecognizerThread(
        *args, **kargs
    )
    #return w)

def isQuitRequested(threadDict):
    doQuit=False
    with threadDict as d:
        if d['doFuncQuit']==True:
            doQuit=True
    return doQuit

class GoogleCloudRecognizerThread(object):
    def __init__(  self, q, t2q, threadDict ):
        recog = sr.Recognizer()
        RecogPrefs.setPrefs(recog)
        self.q = q
        self.t2q = t2q
        self.threadDict = threadDict
        self.doQuit = False
        while True:
            if isQuitRequested(self.threadDict):  ## module level func
                break
            ## Sleep briefly
            time.sleep(0.05)

            while not t2q.empty():
                if isQuitRequested(self.threadDict):
                    break
                audio = t2q.get()

                try:
                    #print("Making Google request...")
                    reqres = (
                        recog.recognize_google(
                            audio,
                        )
                    )
                    
                    #print( "Req: ", reqres )
                    q.put(reqres)
                    
                except sr.UnknownValueError:
                    ## improve this later with a fail count or something ***
                    #print("Audio cannot be translated")
                    tmp = 0
                except:
                    print("Audio cannot be translated")
                    print( traceback.format_exc() )
                    print('continuing...')

    
        
        
        
        
class ListenerThreadGoogleWorker(object):
    def __init__(  self, q, threadDict, speechCommandsTuple=None  ):
        #print(    "args: ",  args,  "kargs: ",  kargs    )
        self.q = q
        self.threadDict = threadDict
        
        ## Make a new extr queue for the audio chunks going to google
        self.t2q = queue.Queue()
        
        r = sr.Recognizer()
        RecogPrefs.setPrefs(r)
        mic = sr.Microphone()
        with mic as source:
            self.t2 = threading.Thread(
                target=workerForRecog,
                daemon=True,
                ## kinda hacky, same ThreadDict...
                args=( self.q, self.t2q, self.threadDict ,),
                
            )
            self.t2.start()
            
            while True:
                #print("LISTENING")
                found = r.listen(source)
                #print( type(found)  )
                #print( found )
                #assert type(found) != type('')
    
                #print('HEARD ?')
                #print( found )
                self.t2q.put( found )
        
                if isQuitRequested(self.threadDict):
                    break
    
                time.sleep(0.05)
                
                #googleTesting
                
        

        print( 'exiting worker...')
    
                
                
    
    def onListen(  self, phrase, listener  ):
        self.tq.put( phrase )





## This function should be removed in the future ***
def google_listen_thread():
    r = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        r.energy_threshold = 400
        r.pause_threshold = 0.5
        r.operation_timeout = 2

        t2 = threading.Thread(target=google_recognize_thread)
        t2.start()
           
        while True:
            found = r.listen(source)

            gaq.put( found )

            time.sleep(0.05)


