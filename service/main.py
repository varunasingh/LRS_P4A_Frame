import os
from os.path import dirname, abspath
import shutil

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adl_lrs.settings")
from colors import add_markup
from django.core.servers.basehttp import WSGIServer, WSGIRequestHandler, get_internal_wsgi_application

from django.core.management import call_command

#Add get request for /umapi/forward/
import threading
import urllib
import urllib2
import httplib
import thread
import time

SETTINGSDIR = dirname(abspath(__file__))
PROJECTROOT = dirname(SETTINGSDIR)
LOG_FOLDER_NAME="logs"
LOG_FOLDER_PATH=os.path.join(PROJECTROOT, LOG_FOLDER_NAME)
LOG_FILES = ['celery_tasks.log','django_request.log', 'lrs.log']
SYNC_DB_FILE_FOLDER = os.path.join(PROJECTROOT, "service")
LRS_SYNC_DB_FILE_PATH = os.path.join(SYNC_DB_FILE_FOLDER, "lrs_db.sqlite3")
NEW_SYNC_DB_FILE_PATH = os.path.join(SYNC_DB_FILE_FOLDER, "db.sqlite3")
STATEMENT_FORWARD_INTERVAL=15
RUN_PORT = 8425
#LOCALHOST_NAME = "http://localhost"
LOCALHOST_NAME = "http://127.0.0.1"
FORWARDING_URL = "umapi/forward/"


if __name__ == "__main__":

    if not os.path.exists(LOG_FOLDER_PATH):
        os.mkdir(LOG_FOLDER_PATH)
    for log_file in LOG_FILES:
        LOG_PATH=os.path.join(LOG_FOLDER_PATH, log_file)
        if not os.path.exists(LOG_PATH):
            os.mknod(LOG_PATH)
    if not os.path.exists(NEW_SYNC_DB_FILE_PATH):
	shutil.copy(LRS_SYNC_DB_FILE_PATH, NEW_SYNC_DB_FILE_PATH)

    
logpath = os.getenv('PYTHON_SERVICE_ARGUMENT')



def statement_forward():
    #thread.start_new_thread(statement_forward)

    timer = threading.Timer(STATEMENT_FORWARD_INTERVAL, statement_forward)
    timer.daemon = True
    timer.start()
   
    url=LOCALHOST_NAME + ":" + str(RUN_PORT) + "/" + FORWARDING_URL

    try:
	print("statement_forward(): Making Statement Forwarding request ( " + str(url) + ")")
        response = urllib2.urlopen(url)

    except urllib2.HTTPError, e:
	print("statement_forward(): HTTPError = " + str(e) )
	try:
		print("statement_forward(): Code: " + str(e.code))
		print("statement_forward(): Response code: " + str(e.code))
	except:
		print("statement_forward(): Cannot get response code after HTTP Error.")
	try:
		response.close()
	except:
		print("statement_forward(): Cannot close non existing response.")
    except urllib2.URLError, e:
        print('statement_forward(): URLError = ' + str(e.reason) + " (Maybe it JUST started)")
	try:
                response.close()
        except:
                print("statement_forward(): Cannot close non existing response.")

    except httplib.HTTPException, e:
        print('statement_forward(): HTTPException ' + str(e) )
	try:
                response.close()
        except:
                print("statement_forward(): Cannot close non existing response.")
    except Exception, e:
        print('statement_forward(): generic exception: ' + str(e) )
	try:
                response.close()
        except:
                print("statement_forward(): Cannot close non existing response.")
    else:
	try:
		print("statement_forward(): No exception. Response: " + str(response.code))
        except:
                print("statement_forward(): Something non exception went wrong in resposne")


    try:
        resposne_code = response.code;
        print(response_code)
    except Exception, re:
	#print("resposne code exception: " + str(re))
	pass
    
    try:
    	response.close()
    except:
        print("statement_forward(): Cannot close non existing response.")

    """
    timer = threading.Timer(10.0, statement_forward)
    timer.start()
    timer.join()
    """



class RequestHandler(WSGIRequestHandler):
    def log_message(self, format, *args):
        # Don't bother logging requests for admin images, or the favicon.
        if (self.path.startswith(self.admin_static_prefix)
                or self.path == '/favicon.ico'):
            return

        msg = "[%s] %s" % (self.log_date_time_string(), format % args)
        kivymarkup = add_markup(msg, args)
	try:
        	with open(logpath, 'a') as fh:
            		fh.write(kivymarkup + '\n')
            		fh.flush()
	except Exception, lp:
		#print("Cannot open logpath. Exception: " + str(lp))
		pass #Not interested in logging requests at the moment

#Trying this
#call_command('syncdb', interactive=False)


print("Main: Starting statement_forward() to run every " + str(STATEMENT_FORWARD_INTERVAL) + " seconds.")
statement_forward()
server_address = ('0.0.0.0', RUN_PORT)
wsgi_handler = get_internal_wsgi_application()
httpd = WSGIServer(server_address, RequestHandler)
httpd.set_app(wsgi_handler)
httpd.serve_forever()

#statement_forward()
