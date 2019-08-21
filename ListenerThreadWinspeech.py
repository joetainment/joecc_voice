import sys, os, queue, subprocess, time, threading, traceback
from queue import Queue


#### Imports for Voice recognition
import winspeech

def worker( *args, **kargs ):
    w = ListenerThreadWinspeechWorker(
        *args, **kargs
    )
    #return w
    
class ListenerThreadWinspeechWorker(object):
    def __init__(  self, q, threadDict, speechCommandsTuple=None  ):
        #print(    "args: ",  args,  "kargs: ",  kargs    )
        self.q = q
        self.tq = queue.Queue()

        print( 'working...')
        
        winspeech.initialize_recognizer(winspeech.INPROC_RECOGNIZER)
        with threadDict as td:
            if speechCommandsTuple==None:
              if 0:  ## quick test
                listener = winspeech.listen_for_anything( self.onListen )
              else:
                listener = winspeech.listen_joecc( None , self.onListen )
            else:            
                listener = winspeech.listen_for( 
                    speechCommandsTuple, self.onListen
                )
                
        while listener.is_listening():
             
            with threadDict as d:
                doFuncQuit = d['doFuncQuit']
                active = d['active']
            if doFuncQuit == True:
                    listener.stop_listening()
                    winspeech.stop_listening()
                    break

            time.sleep(0.03)
            while not self.tq.empty():
                qv = self.tq.get()
                q.put(qv)
               
        print( 'exiting worker...')
    
                
                
    
    def onListen(  self, phrase, listener  ):
        self.tq.put( phrase )

