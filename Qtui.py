## Qt UI For JoeccVoice

"""
Notes:

Some of these options may prove useful in the future:

QtWindowFlags that might be needed
to create unfocused or transparent
windows:

Qt::WindowTransparentForInput	0x00080000
Qt::WindowDoesNotAcceptFocus	0x00200000
Qt::WindowStaysOnTopHint	0x00040000
  possibly when using x11 also needs:
  Qt::BypassWindowManagerHint	0x00000400


Qt::WindowStaysOnBottomHint	0x04000000


"""



#### Import substandard Python Modules
#import multiprocessing

import sys, os, traceback


#### Imports for GUI

import PySide2
## initialization requires separate import of submodules
from PySide2 import QtCore, QtWidgets, QtGui


########  Several imports have been factored out and should be
########  removed from this file ***
##
# import time, threading
# 
# import queue
# from queue import Queue
##
#### Imports for input emulation
#import pynput
#from pynput.keyboard import Key, Controller
##
#### Imports for Voice recognition
#import winspeech
#import speech_recognition as sr
##
#### Import multiprocessing submodules
#import ListenerMprocWinspeech








class Qtui(PySide2.QtWidgets.QMainWindow):
    @classmethod
    def GetQapp( cls, argv ):
         return QtWidgets.QApplication(argv)
        
    def __init__(self, papp):
        super().__init__()

        self.papp = papp
        self.qapp = PySide2.QtWidgets.QApplication.instance()

        self.Icon = self.setWindowIcon(  QtGui.QIcon("media.png")  )  

        self.setWindowTitle( "JoeccVoice")
        self.setMinimumWidth(400)
        # Button that allows loading of images
        self.centralLayoutWidget = PySide2.QtWidgets.QWidget()
        self.setCentralWidget( self.centralLayoutWidget )
        # A Vertical layout to include the button layout and then the image
        self.layout = PySide2.QtWidgets.QFormLayout()
        self.centralLayoutWidget.setLayout( self.layout )        
    
        ## service checkboxes
        self.serviceLabel = PySide2.QtWidgets.QLabel("Please choose a voice recognition provider:")
        self.winspeechCheck = PySide2.QtWidgets.QCheckBox('WindowsSpeech Recognition (Winspeech SAPI)' )
        self.googleCheck = PySide2.QtWidgets.QCheckBox('Google' )
        if self.papp.isModWinSpeechAvailable():
            self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Checked )
            self.onWinspeechActivate()  ## simulate actual checking
            self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        else:
            self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
            self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.winspeechCheck.stateChanged.connect( self.onWinspeechCheckChanged )
        self.googleCheck.stateChanged.connect( self.onGoogleCheckChanged )
        self.layout.addRow( self.serviceLabel )
        self.layout.addRow( self.googleCheck, self.winspeechCheck )
        ## end service checkboxes
    
        ## Label:
        #you can talk here
        self.introLabel = PySide2.QtWidgets.QLabel(
            "\n"
            "Please speak, and voice commands will be converted " 
            "to keystrokes. This will continue working "
            "even if you switch to other applications. \n\n"
            "Available commnds are: 'recognize' and 'type' \n"
            "followed by words to be dictated or phonetic "
            "alphabet keys to be typed."        
        )
        self.introLabel.setWordWrap(True)
        self.layout.addRow(self.introLabel)
        
        
        self.textHeard = PySide2.QtWidgets.QTextEdit( )
        self.textHeard.setReadOnly( True )
        self.layout.addRow(self.textHeard)
        
        
        
        ## text area
        starterText = \
        """
Try saying:
recognize hello world \n
Or say:
Type shift hotel echo lima lima oscar space whiskey oscar romeo lima delta
        """
        
        self.textEdit = PySide2.QtWidgets.QTextEdit( starterText )
        self.layout.addRow(self.textEdit)
        
        ## button
        self.button = PySide2.QtWidgets.QPushButton("Exit")
        self.button.clicked.connect( self.onExitButtonClick  )
        
        self.button.setFocus()
        self.layout.addRow(self.button)
        self.menuEdit = self.menuBar().addMenu("&JoeccVoice")
        self.menuEditExitAction = self.menuEdit.addAction("&Exit" )
        self.menuEditExitAction.setShortcut( 
            PySide2.QtGui.QKeySequence.Quit 
        )
        self.menuEditExitAction.triggered.connect( self.exit )

        self.show()
        
        ## Prep text edit area for testing
        self.textEdit.selectAll()
        self.textEdit.setFocus()
        #self.button.setFocus()
        
        ## Create tmer based update loop
        self.updateTimerInterval = 30
        self.updateTimer = QtCore.QTimer()
        self.updateTimer.timeout.connect( self.update )
        self.setNextTimerUpdate()
    
    def deactivateServices(self,):        
        self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )

    def activateServiceGoogle(self):
        self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Checked )

    def activateServiceWinspeech(self):
        self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )        
        self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Checked )

    def setNextTimerUpdate(self):
        self.updateTimer.start(
          self.updateTimerInterval ## milliseconds
        )
    
    def appendToTextHeard(self, txt ):
        self.textHeard.append(txt)
        
    def update(self):
        self.papp.update()
        self.setNextTimerUpdate()
        

    def onExitButtonClick(self):
        self.exit()
    
    
    
    def onGoogleCheckChanged(self):
        if self.googleCheck.isChecked():
            self.onGoogleActivate()
        else:
            self.onGoogleDeactivate()
            
    def onGoogleActivate(self):
        self.winspeechCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )        
        self.papp.startJobGoogle()
        
    def onGoogleDeactivate(self):
        self.papp.stopJobGoogle()
        
        
    def onWinspeechCheckChanged(self):
        if self.winspeechCheck.isChecked():
            self.onWinspeechActivate()
        else:
            self.onWinspeechDeactivate()
            
    def onWinspeechActivate(self):
        self.googleCheck.setCheckState( PySide2.QtCore.Qt.CheckState.Unchecked )
        self.papp.startJobWinspeech()
        
    def onWinspeechDeactivate(self):
        self.papp.stopJobWinspeech()
        
    def exit(self):
        self.button.setText('Exiting...')
        self.button.repaint()
        self.qapp.quit()
        ## the parent app will quit at this point if it has
        ## nothing else to do
        
        
        

