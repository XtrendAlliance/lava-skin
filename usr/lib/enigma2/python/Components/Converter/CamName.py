#
#  CamName Converter

from Components.Converter.Converter import Converter
from enigma import iServiceInformation, iPlayableService
from Components.Element import cached
from Poll import Poll

class CamName(Poll, Converter, object):
	def __init__(self, type):
		Poll.__init__(self)
		Converter.__init__(self, type)
		self.type = type

		self.poll_interval = 1000
		self.poll_enabled = True


	@cached
	def getText(self):
		textvalue = ""
		service = self.source.service
		if service:
			info = service and service.info()
			if info:
				if info.getInfoObject(iServiceInformation.sCAIDs):
					ecm_info = self.ecmfile()
					if ecm_info:								
						# name	
						using = ecm_info.get("using", "")
						if using:
							if using == "emu":
								textvalue = "(CCcam: EMU)" 
							elif using == "CCcam-s2s":
								textvalue = "(CCcam-s2s)" 						
							else:
								textvalue = "(CCcam)"		
						else:
							# mgcamd
							source = ecm_info.get("source", None)
							if source:
								if source == "emu":
									textvalue = "(mgcamd: EMU)"
								else:
									textvalue = "(mgcamd)"
							# oscam
							oscsource = ecm_info.get("from", None)
							if oscsource:
								textvalue = "(oscam)"
							# gbox
							decode = ecm_info.get("decode", None)
							if decode:
								if decode == "Internal":
									textvalue = "(gbox: EMU)"
								else:
									textvalue = "(gbox)"
							
		return textvalue 

	text = property(getText)

	def ecmfile(self):
		ecm = None
		info = {}
		service = self.source.service
		if service:
			frontendInfo = service.frontendInfo()
			if frontendInfo:
				try:
					ecmpath = "/tmp/ecm%s.info" % frontendInfo.getAll(False).get("tuner_number")
					ecm = open(ecmpath, "rb").readlines()
				except:
					try:
						ecm = open("/tmp/ecm.info", "rb").readlines()
					except: pass
			if ecm:
				for line in ecm:
					x = line.lower().find("msec")
					if x != -1:
						info["ecm time"] = line[0:x+4]
					else:
						item = line.split(":", 1)
						if len(item) > 1:
							info[item[0].strip().lower()] = item[1].strip()
						else:
							if not info.has_key("caid"):
								x = line.lower().find("caid")
								if x != -1:
									y = line.find(",")
									if y != -1:
										info["caid"] = line[x+5:y]

		return info

	def changed(self, what):
		if (what[0] == self.CHANGED_SPECIFIC and what[1] == iPlayableService.evUpdatedInfo) or what[0] == self.CHANGED_POLL:
			Converter.changed(self, what)
