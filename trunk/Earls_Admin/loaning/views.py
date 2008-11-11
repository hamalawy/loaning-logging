# Create your views here.
# Create your views here.
from django.template import Context, loader
from django.shortcuts import get_object_or_404, render_to_response
from django.http import HttpResponse
from Earls_Admin.loaning.models import *
import datetime

#####################################################################
# BORROWER TABLE:
#   borrowerStatus - Used for status when defining new staff/students
# INVENTORY TABLE:
#   inventoryCat - Inventory category
#   inventorySub - Inventory sub-category
#   inventoryLoc - Inventory location
#   inventoryPCStatus - Inventory PC status
#   inventoryLoanable - Inventory loanable
#   inventoryService - Inventory is in service
#   loanedByUser - Users that can loan items
#####################################################################
#
# LOANING:
#
# To enable loaning a status field is used within the forms. This is
# hidden, and changes value, depending on what the form is being used
# for.
#
# VALUES:
#
# 1) 0 - Represents simply displaying the values of the search criteria
# 2) 1 - Represents the first stage of the loaning process
# 3) 2 - Represents the second stage of the loaning process
#
######################################################################



def index(request):
	"""Display the index page"""
	t = loader.get_template('loaning/index.html')
	c = Context()
	return HttpResponse(t.render(c))

def addOption(request):
	"""Display the page used to add options to the database"""
	t = loader.get_template('loaning/addOption.html')
	c = Context()
	return HttpResponse(t.render(c))

def addOptionDB(request):
	"""Takes options as entered into the addOptions webpage and loads them into the database"""
	values = request.POST['value']
	optionval = request.POST['option_options']

	values = values.split('|')

	for elem in values:
		p = Options(option = optionval,value=elem)
		success = p.save()
			
	print values

	string = ""
	if success == None:
		string = "Success<br><a href='/loaning/'>Go Back</a>"
	else:
		string = "Unsuccessful<br><a href='/loaning/'>Go Back</a>"
	print success
	return HttpResponse(string)

def addPerson(request):
	"""Takes the options relevant to the addPerson webpage (such as status = Staff | Student
	and displays these as part of the form used to add people to the database"""
	#THIS VIEW IS USED TO BE ABLE TO ADD A PERSON TO THE DATABASE
	

	#GET THE OPTION INFORMATION FOR STATUS FROM THE DBs
	p = Options.objects.all().filter(option="borrowerStatus")
	
	vals = []
	for elem in p:
		print elem.value
		vals.append(elem.value)

	t = loader.get_template('loaning/addPerson.html')
	c = Context({'status':vals,})
	return HttpResponse(t.render(c))

def addItem (request):
	"""Takes the options relevant to the addPerson webpage (such as category = Computing | AV
	and displays these as part of the form used to add items to the database"""
	#THIS VIEW IS USED TO BE ABLE TO ADD AN INVENTORY ITEM TO THE DATABASE
	
	#GET THE OPTION INFORMATION FOR STATUS'S FROM DB
	p = Options.objects.all()

	cat = []
	sub = []
	loc = []
	stat = []
	loan = []
	serv = []

	for elem in p:
		test = elem.option
		if test == "inventoryCat":
			cat.append(elem.value)
		elif test == "inventorySub":
			sub.append(elem.value)
		elif test == "inventoryLoc":
			loc.append(elem.value)
		elif test == "inventoryPCStatus":
			stat.append(elem.value)
		elif test == "inventoryLoanable":
			loan.append(elem.value)
		elif test == "inventoryService":
			serv.append(elem.value)

	t = loader.get_template('loaning/addItem.html')
	c = Context({'categ':cat,'subcat':sub,'loc':loc,'stat':stat,'loan':loan,'serv':serv,})
	return HttpResponse(t.render(c))

	

def checkInput(val):
	"""Checks strings entered into the database, if blank returns N/A"""
	string = ""
	if val == "":
		string = "N/A"
	else:	
		string = val

	return string

def addPersonDB(request):
	"""Takes information from a form, performs checks and adds to the database"""
	fore = checkInput(request.POST['forename'])
	sur = checkInput(request.POST['surname'])
	schoolid = int(request.POST['schoolid'])
	stat = checkInput(request.POST['status'])
	note = checkInput(request.POST['notes'])

	p = Borrower(schoolidnum=schoolid,forename=fore,surname=sur,status=stat,notes=note)
	print p
	success = p.save()

	string = ""
	if success == None:
		string = "Success<br><a href='/loaning/'>Go Back</a>"
	else:
		string = "Unsuccessful<br><a href='/loaning/'>Go Back</a>"
	print success
	return HttpResponse(string)

def addItemDB(request):
	"""Takes information from a form, performs checks and adds to the database"""
	serial = checkInput(request.POST['serial'])
	cat = checkInput(request.POST['categ'])
	subcat = checkInput(request.POST['subcat'])
	make = checkInput(request.POST['make'])
	model = checkInput(request.POST['model'])
	location = checkInput(request.POST['location'])
	pcstatus = checkInput(request.POST['status'])
	loanable = checkInput(request.POST['loan'])
	inservice = checkInput(request.POST['serv'])
	notes = checkInput(request.POST['notes'])
	price = request.POST['price']
	purchaseday = request.POST['date']
	purchasemonth = request.POST['month']
	purchaseyear = request.POST['year']

	warranty = request.POST['warranty']

	print purchaseday, purchasemonth, purchaseyear

	success = ""

	#HANDLE THE CASE WHERE THE SERIAL NUMBER DOES NOT EXIST, BUT WHEN
	#THIS FIELD IS USED TO ENTER MULTIPLE ITEMS WITH THE SAME DETAILS

	if serial.split("=")[0].lower() == "quantity":
		purchasedate = datetime.datetime(int(purchaseyear),int(purchasemonth),int(purchaseday))
		for i in range(int(serial.split("=")[1])):
			p=Inventory(serial="N/A", category=cat, subcat = subcat, make=make, model=model, location=location,pcstatus=pcstatus,loanable=loanable, inservice=inservice,notes=notes,price=price,datepurchased = purchasedate, warrantylength = warranty)
			success = p.save()

	else:

		purchasedate = datetime.datetime(int(purchaseyear),int(purchasemonth),int(purchaseday))
		p=Inventory(serial=serial, category=cat, subcat = subcat, make=make, model=model, location=location, pcstatus=pcstatus, loanable=loanable, inservice=inservice, notes=notes,price=price,datepurchased = purchasedate, warrantylength = warranty)
		success = p.save()

	string = ""
	if success == None:
		string = "Success<br><a href='/loaning/'>Go Back</a>"
	else:
		string = "Unsuccessful<br><a href='/loaning/'>Go Back</a>"
	print success
	return HttpResponse(string)

def search(request):
	"""Loads HTML page to provide a portal to the search options"""
	t = loader.get_template('loaning/search.html')
	c = Context()
	return HttpResponse(t.render(c))

def search_people(request):
	"""Loads a form to provide searching for people"""
	t = loader.get_template('loaning/search_people.html')
	c = Context({'status':1,})
	return HttpResponse(t.render(c))

def search_items(request):
	"""Loads a form to provide searching for items"""
	t = loader.get_template('loaning/search_items.html')
	c = Context()
	return HttpResponse(t.render(c))

def execute_items(request):
	"""Executes a search for items in the database"""
	search1 = checkInput(request.POST['item1'])
	criteria1 = checkInput(request.POST['criteria1'])
	
	search2 = checkInput(request.POST['item2'])
	criteria2 = checkInput(request.POST['criteria2'])

	search3 = checkInput(request.POST['item3'])
	criteria3 = checkInput(request.POST['criteria3'])

	search4 = checkInput(request.POST['item4'])
	criteria4 = checkInput(request.POST['criteria4'])

	borrowerID = request.POST['borrowerID']

	print "Borrower ID, execute_items: ",borrowerID
#	loan_item = request.POST['loan']

	status = request.POST['status']

#	print loan_item, borrowerID

	#NO MATTER WHAT IS SELECTED PULL BACK ALL OBJECTS

	p = Inventory.objects.all()

	#NOW ADD TO THE FILTER FOR EACH BOX WHERE STUFF IS SELECTED
	if criteria1 != "" and search1 != "N/A":
		if search1 == "serial":
			p = p.filter(serial=criteria1)
		elif search1 == "cat":
			p = p.filter(category=criteria1)
		elif search1 == "subcat":
			p = p.filter(subcat=criteria1)
		elif search1 == "make":
			p = p.filter(make=criteria1)
		elif search1 == "model":
			p = p.filter(model=criteria1)
		elif search1 == "location":
			p = p.filter(location=criteria1)
		elif search1 == "pcstatus":
			p = p.filter(pcstatus=criteria1)
		elif search1 == "loanable":
			p = p.filter(loanable=criteria1)
		elif search1 == "inservice":
			p = p.filter(inservice=criteria1)
		elif search1 == "notes":
			p = p.filter(notes=criteria1)
		elif search1 == "price":
			p = p.filter(price=criteria1)
		elif search1 == "purchasedate":
			p = p.filter(datepurchased=criteria1)
		elif search1 == "warranty":
			p = p.filter(warrantylength=criteria1)


	if criteria2 != "" and search2 != "N/A":
		if search2 == "serial":
			p = p.filter(serial=criteria2)
		elif search2 == "cat":
			p = p.filter(category=criteria2)
		elif search2 == "subcat":
			p = p.filter(subcat=criteria2)
		elif search2 == "make":
			p = p.filter(make=criteria2)
		elif search2 == "model":
			p = p.filter(model=criteria2)
		elif search2 == "location":
			p = p.filter(location=criteria2)
		elif search2 == "pcstatus":
			p = p.filter(pcstatus=criteria2)
		elif search2 == "loanable":
			p = p.filter(loanable=criteria2)
		elif search2 == "inservice":
			p = p.filter(inservice=criteria2)
		elif search2 == "notes":
			p = p.filter(notes=criteria2)
		elif search2 == "price":
			p = p.filter(price=criteria2)
		elif search2 == "purchasedate":
			p = p.filter(datepurchased=criteria2)
		elif search2 == "warranty":
			p = p.filter(warrantylength=criteria2)


	if criteria3 != "" and search3 != "N/A":
		if search3 == "serial":
			p = p.filter(serial=criteria3)
		elif search3 == "cat":
			p = p.filter(category=criteria3)
		elif search3 == "subcat":
			p = p.filter(subcat=criteria3)
		elif search3 == "make":
			p = p.filter(make=criteria3)
		elif search3 == "model":
			p = p.filter(model=criteria3)
		elif search3 == "location":
			p = p.filter(location=criteria3)
		elif search3 == "pcstatus":
			p = p.filter(pcstatus=criteria3)
		elif search3 == "loanable":
			p = p.filter(loanable=criteria3)
		elif search3 == "inservice":
			p = p.filter(inservice=criteria3)
		elif search3 == "notes":
			p = p.filter(notes=criteria3)
		elif search3 == "price":
			p = p.filter(price=criteria3)
		elif search3 == "purchasedate":
			p = p.filter(datepurchased=criteria3)
		elif search3 == "warranty":
			p = p.filter(warrantylength=criteria3)

	if criteria4 != "" and search4 != "N/A":
		if search4 == "serial":
			p = p.filter(serial=criteria4)
		elif search4 == "cat":
			p = p.filter(category=criteria4)
		elif search4 == "subcat":
			p = p.filter(subcat=criteria4)
		elif search4 == "make":
			p = p.filter(make=criteria4)
		elif search4 == "model":
			p = p.filter(model=criteria4)
		elif search4 == "location":
			p = p.filter(location=criteria4)
		elif search4 == "pcstatus":
			p = p.filter(pcstatus=criteria4)
		elif search4 == "loanable":
			p = p.filter(loanable=criteria4)
		elif search4 == "inservice":
			p = p.filter(inservice=criteria4)
		elif search4 == "notes":
			p = p.filter(notes=criteria4)
		elif search4 == "price":
			p = p.filter(price=criteria4)
		elif search4 == "purchasedate":
			p = p.filter(datepurchased=criteria4)
		elif search4 == "warranty":
			p = p.filter(warrantylength=criteria4)

	a = ""
	if status == "0":
		a = view_display(p,"items",status)
	else:
		a = loan_display(p,"items",status,borrowerID)

	return HttpResponse(a)



def execute_people(request):
	"""Executes a search for people from the database"""
	search1 = checkInput(request.POST['person1'])
	criteria1 = checkInput(request.POST['criteria1'])

	search2 = checkInput(request.POST['person2'])
	criteria2 = checkInput(request.POST['criteria2'])

	search3 = checkInput(request.POST['person3'])
	criteria3 = checkInput(request.POST['criteria3'])

	search4 = checkInput(request.POST['person4'])
	criteria4 = checkInput(request.POST['criteria4'])

	status = request.POST['status']

	#loan_item = request.POST['loan']

	#NO MATTER WHAT IS SELECTED PULL BACK ALL OBJECTS

	p = Borrower.objects.all()

	#NOW ADD TO THE FILTER FOR EACH BOX WHERE STUFF IS SELECTED
	if criteria1 != "" and search1 != "N/A":
		if search1 == "id":
			p = p.filter(schoolidnum=criteria1)
		elif search1 == "forename":
			p = p.filter(forename=criteria1)
		elif search1 == "surname":
			p = p.filter(surname=criteria1)
		elif search1 == "status":
			p = p.filter(status=criteria1)

	if criteria2 != "" and search2 != "N/A":
		if search2 == "id":
			p = p.filter(schoolidnum=criteria2)
		elif search2 == "forename":
			p = p.filter(forename=criteria2)
		elif search2 == "surname":
			p = p.filter(surname=criteria2)
		elif search2 == "status":
			p = p.filter(status=criteria2)

	if criteria3 != "" and search3 != "N/A":
		if search3 == "id":
			p = p.filter(schoolidnum=criteria3)
		elif search3 == "forename":
			p = p.filter(forename=criteria3)
		elif search3 == "surname":
			p = p.filter(surname=criteria3)
		elif search3 == "status":
			p = p.filter(status=criteria3)

	if criteria4 != "" and search4 != "N/A":
		if search4 == "id":
			p = p.filter(schoolidnum=criteria4)
		elif search4 == "forename":
			p = p.filter(forename=criteria4)
		elif search4 == "surname":
			p = p.filter(surname=criteria4)
		elif search4 == "status":
			p = p.filter(status=criteria4)


	a = ""
	if status == "0":
		a = view_display(p,"people",status)
	else:
		a = loan_display(p,"people",status,0)
	return HttpResponse(a)

def view_display(filtered_data,type_data,status):
	"""Displays data returned when querying the database"""
	p = filtered_data

	#CREATE AN ARRAY OF TITLES
	title_type = ["people","items","loans","calllogs"]
	
	values = []
	title = []
	search_type = ""

	if type_data.lower() == "people":
		search_type = "borrower"
		title = ["School ID","Forename","Surname","Status","Notes"]
		search_type = "borrower"
		for elem in p:
			elements = []
			elements.append(elem.schoolidnum)
			elements.append(elem.forename)
			elements.append(elem.surname)
			elements.append(elem.status)
			elements.append(elem.notes)
			values.append(elements)
	elif type_data.lower() == "items":
		title = ["Serial Number","Category","Sub-Category","Make","Model","Location","PC Status","Loanable","In-Service","Notes","Price"]
		search_type = "inventory"
		for elem in p:
			elements = []
			elements.append(elem.serial)
			elements.append(elem.category)
			elements.append(elem.subcat)
			elements.append(elem.make)
			elements.append(elem.model)
			elements.append(elem.location)
			elements.append(elem.pcstatus)
			elements.append(elem.loanable)
			elements.append(elem.inservice)
			elements.append(elem.notes)
			elements.append(elem.price)
			values.append(elements)	
	elif type_data.lower() == "loans":
		title = ["Borrower","Item","Date Required","Date Loaned","Date Return By","Date Returned By","Returned By"]
		search_type = "loaning"	
	elif type_data.lower() == "calllogs":
		title = ["Fault Date","Fault Reported By","Fault Logged By","Faulty Item","Fault","Suspected Repair","Actual Repair","Repair Date","Internal / External Repair"]
		search_type = "call logging"
	else: 
		title = ["School ID","Forename","Surname","Status","Notes"]
		search_type = "borrower"
		for elem in p:
			elements = []
			elements.append(elem.schoolidnum)
			elements.append(elem.forename)
			elements.append(elem.surname)
			elements.append(elem.status)
			elements.append(elem.notes)
			values.append(elements)	

	t = loader.get_template('loaning/views.html')
	c = Context({'type':search_type,'title':title,'values':values,'status':status,})
	return HttpResponse(t.render(c))

def type_view(request,type_view):
	"""Takes a query and formats it so that it can be displayed"""
	#TAKE THE ADDRESS AND PROCESS DIFFERENTLY DEPENDING ON THE URL RESULT
	#SUITABLE QUERIES:
	#	PEOPLE
	#	ITEMS
	#	LOANS
	#	CALLLOGS
	status=0
	p = ""
	title= []
	values = []
	search_type = ""
	a=""

	if type_view.lower() == "people":
		p = Borrower.objects.all()
		a = view_display(p,"people",status)

	elif type_view.lower() == "items":
		p = Inventory.objects.all()
		a = view_display(p,"items",status)
	elif type_view.lower() == "loans":
		p = Loaning.objects.all()
		a = view_display(p,"loans",status)
	elif type_view.lower() == "calllogs":
		p = Logging.objects.all()
		a = view_display(p,"calllogs",status)	

	else: 
		p = Borrower.objects.all()
		a = view_display(p,"people",status)
	return a

def loan_display(filtered_data,type_data,status,borrower):
	"""Displays suitably formatted queried data and adds the ability to store the selected option"""
	p = filtered_data

	#CREATE AN ARRAY OF TITLES
	title_type = ["people","items","loans","calllogs"]
	
	values = []
	title = []
	search_type = ""

	if type_data.lower() == "people":
		search_type = "borrower"
		title = ["Select","School ID","Forename","Surname","Status","Notes"]
		search_type = "borrower"
		for elem in p:
			elements = []
			elements.append(elem.id)
			elements.append(elem.schoolidnum)
			elements.append(elem.forename)
			elements.append(elem.surname)
			elements.append(elem.status)
			elements.append(elem.notes)
			values.append(elements)
	elif type_data.lower() == "items":
		title = ["Select","Serial Number","Category","Sub-Category","Make","Model","Location","PC Status","Loanable","In-Service","Notes","Price"]
		search_type = "inventory"
		for elem in p:
			elements = []
			elements.append(elem.id)			
			elements.append(elem.serial)
			elements.append(elem.category)
			elements.append(elem.subcat)
			elements.append(elem.make)
			elements.append(elem.model)
			elements.append(elem.location)
			elements.append(elem.pcstatus)
			elements.append(elem.loanable)
			elements.append(elem.inservice)
			elements.append(elem.notes)
			elements.append(elem.price)
			values.append(elements)	
	elif type_data.lower() == "loans":
		title = ["Select","Borrower","Item","Date Required","Date Loaned","Date Return By","Date Returned By","Returned By"]
		search_type = "loaning"	
	elif type_data.lower() == "calllogs":
		title = ["Select","Fault Date","Fault Reported By","Fault Logged By","Faulty Item","Fault","Suspected Repair","Actual Repair","Repair Date","Internal / External Repair"]
		search_type = "call logging"
	else: 
		title = ["Select","School ID","Forename","Surname","Status","Notes"]
		search_type = "borrower"
		for elem in p:
			elements = []
			elements.append(elem.id)
			elements.append(elem.schoolidnum)
			elements.append(elem.forename)
			elements.append(elem.surname)
			elements.append(elem.status)
			elements.append(elem.notes)
			values.append(elements)	

	t = loader.get_template('loaning/loan_views.html')
	c = Context({'type':search_type,'title':title,'values':values,'status':status,'borrowerID':borrower,})
	return HttpResponse(t.render(c))

def test(request):
	t = loader.get_template('test.html')
	c = Context()
	return HttpResponse(t.render(c))

def loan_item_step1(request):
	"""Function used to take the entry for the borrower and pass this into the form used to select the item for loaning"""
	borrowerID = request.POST['borrower']
	status = int(request.POST['status'])
	status += 1
	print "Status: ", status
	print "Loan Item Step1: ", borrowerID
	t=loader.get_template('loaning/search_items.html')
	c = Context({'borrowerID':borrowerID,'status':status})
	return HttpResponse(t.render(c))

def loan_item_step2(request):
	"""Function used to complete the loaning procedure"""
	print "LOAN ITEM STEP 2"
	borrowerID = request.POST['borrowerID']
	borrower = request.POST['borrower']
	borrowerID = int(borrowerID)
	itemID = int(borrower)

	# GET THE ITEM FOR LOAN AND THE BORROWER INFORMATION
	borrower_obj = Borrower.objects.get(pk=borrowerID)
	item_obj = Inventory.objects.get(pk=itemID)

	# CONVERT TO AN ARRAY
	a = borrower_obj
	borrower_info=[a.schoolidnum,a.forename,a.surname,a.status,a.notes]
	b = item_obj
	item_info = [b.serial,b.category,b.subcat,b.make,b.model]

	#print borrower_info

	# LIST TO STORE THE TITLES
	borrower_title = ["Select","School ID","Forename","Surname","Status"]
	item_title = ["Serial Number","Category","Sub-Category","Make","Model"]

	# FROM THE DATABASE PULL THE INFORMATION ABOUT LOANING MEMBERS OF STAFF
	p = Options.objects.all().filter(option="loanedByUser")
	
	print "Len db",len(p)

	# LOOP AROUND THIS AND CONSTRUCT SOMETHING USEFUL TO SEND TO THE VIEW
	for elem in p:
		#DO A DATABASE LOOKUP FOR THE PERSON WITH THE DETAILS FOUND FROM THIS OPTION, THEN CAN USE TO SEND THE 
		#PERSON DATABASE ID WHEN SELECTING A NAME IN THE VIEW
		print		
		person = elem.value.split(":")

		q = Borrower.objects.all().filter(forename=person[0],surname=person[1],schoolidnum=person[2])
		if len(q) > 1:
			val = q[1]
		else:
			val = q

		temp = [val.id,person[0]+person[1]]
		print temp
	t=loader.get_template('loaning/loan_items.html')
	c = Context({'borrowerTitle':borrower_title,'itemTitle':item_title,'borrower':borrower_info,'item':item_info,'borrowerID':borrowerID,'itemID':itemID,})
	
	return HttpResponse(t.render(c))
