from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{'document_root':'/home/matt/school/django/media'}),
    (r'^loaning/$', 'Earls_Admin.loaning.views.index'),
    (r'^loaning/addPerson/$', 'Earls_Admin.loaning.views.addPerson'),
    (r'^loaning/addPerson/addDB/$', 'Earls_Admin.loaning.views.addPersonDB'),
    (r'^loaning/addItem/$', 'Earls_Admin.loaning.views.addItem'),
    (r'^loaning/addItem/addDB/$', 'Earls_Admin.loaning.views.addItemDB'),
    (r'^loaning/addOption/$','Earls_Admin.loaning.views.addOption'),
    (r'^loaning/addOption/addDB$','Earls_Admin.loaning.views.addOptionDB'),
    (r'^loaning/search/$', 'Earls_Admin.loaning.views.search'),
    (r'^loaning/search/people/$', 'Earls_Admin.loaning.views.search_people'),
    (r'^loaning/search/people/execute/$','Earls_Admin.loaning.views.execute_people'),
    (r'^loaning/search/execute/$', 'Earls_Admin.loaning.views.search_execute'),
    (r'^loaning/search/items/$', 'Earls_Admin.loaning.views.search_items'),
    (r'^loaning/search/items/execute/$','Earls_Admin.loaning.views.execute_items'),

    (r'^loaning/loanItem/step1/$','Earls_Admin.loaning.views.loan_item_step1'),
    (r'^loaning/loanItem/step2/$','Earls_Admin.loaning.views.loan_item_step2'),

    (r'^loaning/view/(?P<type_view>\w+)/$', 'Earls_Admin.loaning.views.type_view'),
    (r'^test/$','Earls_Admin.loaning.views.test'), 


    (r'^printers/$', 'Earls_Admin.printer_admin.views.index'),
    #(r'^printers/view/$', 'Earls_Admin.printer_admin.views.printer_view'),
    (r'^printers/all/$', 'Earls_Admin.printer_admin.views.all_jobs'),
    (r'^printers/room/(?P<room>[a-z,A-Z]{1}[0-9]{1,2})/$', 'Earls_Admin.printer_admin.views.room'),
    (r'^printers/room/(?P<room>[a-z,A-Z]{1}[0-9]{1,2})/(?P<printer>\w+)/','Earls_Admin.printer_admin.views.printer_vals'),
    # Example: (?P<room>\d+)
    # (r'^Earls_Admin/', include('Earls_Admin.foo.urls')),

    # Uncomment this for admin:
#     (r'^admin/', include('django.contrib.admin.urls')),
)
