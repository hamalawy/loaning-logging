import popen2
import os
import sys
from datetime import datetime

def setup_environment():
    pathname = os.path.dirname(sys.argv[0])
    sys.path.append(os.path.abspath(pathname))
    sys.path.append(os.path.normpath(os.path.join(os.path.abspath(pathname), '../')))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# Must set up environment before imports.
setup_environment()

from django.core.mail import send_mail

EMAIL_HOST = "post.earls.dudley.gov.uk"

EMAIL_PORT = 25

send_mail("Test subject","Body message","mholder@earls.dudley.gov.uk",["mholder@earls.dudley.gov.uk"], fail_silently=False)
