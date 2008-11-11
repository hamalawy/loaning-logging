import popen2
import os
import sys
from datetime import datetime

#>>> p = Poll(question="What's up?", pub_date=datetime.now())
#p.save()

def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Must set up environment before imports.
setup_environment()

from Earls_Admin.printer_admin.models import *

def T3Las():

	#STORE THE VALUES SOMEWHERE TEMPERARILY
	vals = ["Brother","HL4040CN",datetime.now(),"T3",0,0,0,0,0,0,0,0,0]
	
	(o,i,e) = popen2.popen3("wget -qO- http://10.240.251.34/etc/mnt_info.html?kind=item")
	data = o.read()
	data = data.split("\n")
	
	if e.read() != " ":
		for i in range(len(data)):
			if data[i].find("Total Page Count") != -1:
				vals[4]=int(data[i+2].strip("\r\n"))
			elif data[i].find("Color Page Count") != -1:
				vals[5]=int(data[i+2].strip("\r\n"))
			elif data[i].find("Monochrome Page Count") != -1:
				vals[6]=int(data[i+2].strip("\r\n"))
			elif data[i].find("Image Count Cyan (C)") != -1:
				vals[7] =int(data[i+2].strip("\r\n"))
			elif data[i].find("Image Count Magenta (M)") != -1:
				vals[8] =int(data[i+2].strip("\r\n"))
			elif data[i].find("Image Count Yellow (Y)") != -1:
				vals[9] =int(data[i+2].strip("\r\n"))
			elif data[i].find("Image Count Black (K)") != -1:
				vals[10]=int(data[i+2].strip("\r\n"))
			elif data[i].find("Drum Count") != -1:
				vals[11]=int(data[i+2].strip("\r\n"))
		
		p = printer_admin(make=vals[0],model=vals[1],date=vals[2],location=vals[3],totalcount=vals[4],colourcount=vals[5],monocount=vals[6],cyancount=vals[7],magcount=vals[8],yelcount=vals[9],blackcount=vals[10],drumcount=vals[11],difftotal=vals[12])
		p.save()
			
def B15Las():
	vals = ["Xerox","Phaser 7400",datetime.now(),"B15",0,0,0,0,0,0,0,0,0]

	(o,i,e) = popen2.popen3("wget -qO- http://10.240.250.248/status.html")
	data = o.read()
	data = data.split("\n")
	
	if e.read() != " ":
		for i in range(len(data)):
			if data[i].find("<td>Page Count") != -1:
				vals[4] = int(data[i+1].strip("\r\n").strip("<td>").strip("</"))

		p = printer_admin(make=vals[0],model=vals[1],date=vals[2],location=vals[3],totalcount=vals[4],colourcount=vals[5],monocount=vals[6],cyancount=vals[7],magcount=vals[8],yelcount=vals[9],blackcount=vals[10],drumcount=vals[11],difftotal=vals[12])
		p.save()


print T3Las()
print B15Las()
