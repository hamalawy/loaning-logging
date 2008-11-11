# Create your views here.
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from Earls_Admin.printer_admin.models import *


def index(request):

    #LOOK FOR THE UNIQUE ROOMS
    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT location FROM printer_admin_printer_admin")
    row = cursor.fetchall()

    t = loader.get_template('printer_admin/index.html')
	
    strings = []
    for elem in row:
	strings.append(elem[0])
    print strings

    c = Context({'rooms': strings,})
    return HttpResponse(t.render(c))

def all_jobs(request):
    p = printer_admin.objects.all().order_by("make")

    string = "<table>"
    for elem in p:
		string += "<tr><td>"+elem.make+"</td><td>"+elem.model +"</td><td>"+str(elem.totalcount)+"</td><td>"+str(elem.date)+"</td><tr><tr>"
    return HttpResponse(string)

def room(request, room):
    p = printer_admin.objects.all().filter(location = room)

    from django.db import connection
    cursor = connection.cursor()
    cursor.execute("SELECT DISTINCT make,model, location FROM printer_admin_printer_admin")
    rows = cursor.fetchall()

    make = []
    model = []
    printers = []
    url = []

    for elem in rows:
	if elem[2] == room:
		make.append(elem[0])
		model.append(elem[1])
		printers.append([elem[0],elem[1]])
		string = "%s_%s"%(elem[0],elem[1])
		url.append(string.replace(" ","_"))
    t = loader.get_template('printer_admin/room_printer.html')

    c = Context({'room': room,'make':make,'model':model,'printers':printers,'url':url,})
    return HttpResponse(t.render(c))

def printer_vals(request,room,printer):
    
    
    printer_arr = printer.split("_")
    pr_model = ""
    for i in range(1,len(printer_arr)):
	if i == len(printer_arr)-2:
		pr_model += printer_arr[i]+" "
	else:
		pr_model += printer_arr[i]

    p = printer_admin.objects.all().filter(location=room,make=printer.split("_")[0],model=pr_model).order_by("date")

    diffs = [0,]
    i=len(p)
    for elem in p:
	if i<len(p):
		diffs.append(p[i].totalcount - p[i-1].totalcount)	
	i-=1

    i=0
    for elem in p:
	q = printer_admin.objects.all().get(id = elem.id)
	q.difftotal = diffs[i]	
	q.save()	
	i+=1

    t = loader.get_template('printer_admin/printer_vals.html')
    c = Context({'printer_vals':p,'room':room,'printer':printer,'diff':diffs})

    return HttpResponse(t.render(c))
