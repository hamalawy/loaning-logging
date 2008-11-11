from django.db import models

# Create your models here.

class Borrower(models.Model):

	schoolidnum = models.IntegerField('school ID number')
	forename = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)	
	status = models.CharField(max_length=100)
	notes = models.CharField(max_length=1000)

class Inventory(models.Model):
	serial = models.CharField(max_length=100) #, 'serial number'
	category = models.CharField(max_length=100) #,'category'
	subcat = models.CharField(max_length=100) #,'sub-category'
	make = models.CharField(max_length=100) #,'make'
	model = models.CharField(max_length=100) #,'model'
	location = models.CharField(max_length=100) #,'location'
	pcstatus = models.CharField(max_length=100) #,'status if PC (eg, RM Managed)'
	loanable = models.BooleanField('if loanable')
	inservice = models.BooleanField('if in-service')
	notes = models.CharField(max_length=1000) #,'notes'
	price = models.FloatField()
	datepurchased = models.DateTimeField('Date Purchased')
	warrantylength = models.FloatField()

class Loaning(models.Model):
	borrower = models.ForeignKey(Borrower,related_name="Borrower")
	item = models.ForeignKey(Inventory,related_name="Loaning_item")
	datereq = models.DateTimeField('date required')
	dateloan = models.DateTimeField('date loaned')
	dateret = models.DateTimeField('date returned')
	dateretby = models.DateTimeField('date to return by')
	retby = models.ForeignKey(Borrower,related_name="Returned_by")

class Logging(models.Model):
	faultdate = models.DateTimeField('date fault occured')
	faultrep = models.ForeignKey(Borrower,related_name="Fault_reported_by")
	faultlog = models.ForeignKey(Borrower,related_name="Fault_logged_by")
	faultitem = models.ForeignKey(Inventory,related_name="Faulty_item")
	fault = models.CharField(max_length=10000) #,'fault'
	susrep = models.CharField(max_length=10000) #,'suspected repair'
	actrep = models.CharField(max_length=10000) #,'actual repair'
	repdate = models.DateTimeField('date repair carried out')
	internal = models.CharField(max_length=30) #,'repair carried out by school, RM, other'


class Options(models.Model):
	option = models.CharField(max_length=50)
	value = models.CharField(max_length=50)

