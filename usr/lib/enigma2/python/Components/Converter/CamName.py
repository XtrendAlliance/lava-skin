################################################################################
#                                                                              #
# CamName Converter show your current SoftCam Name: in InfoBar/SecondInfobar   #
#                                                                              #
# Skin Example:                                                                #
#                                                                              #
#        <widget source="session.CurrentService" render="Label" .......>       #
#          <convert type="CamName">                                            #
#           </convert>                                                         #
#        </widget>                                                             #
#                                                                              #
################################################################################

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService, iPlayableServicePtr 
from Components.Element import cached
from ServiceReference import ServiceReference
from Screens.InfoBar import InfoBar
from Tools.Directories import fileExists
import os

class CamName(Converter, object):
	def __init__(self, type):
		Converter.__init__(self, type)
		self.type = type

	@cached
	def getText(self):
                if fileExists("/etc/init.d/softcam"):
			camname = ""
			try:
				x = os.popen("/etc/init.d/softcam info")
				for current in x.readlines():
					camname = current
			except: 
				pass
		else:
			camname = ""
                return camname
                
	text = property(getText)