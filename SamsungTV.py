import sys
import os
import logging

sys.path.append('../')

from samsungtvws import SamsungTVWS

# Increase debug level
logging.basicConfig(level=logging.INFO)



# Normal constructor
tv = SamsungTVWS('192.168.1.42')

# Autosave token to file
token_file = os.path.dirname(os.path.realpath(__file__)) + '/tv-token.txt'
tv = SamsungTVWS(host='192.168.1.42', port=8002, token_file=token_file)




# tv.open_browser('www.google.com')

def openPlex():
	# tv.rest_app_run('3201512006963')
	tv.run_app('3201512006963')

# tv.shortcuts().power()
# tv.shortcuts().up()
# tv.shortcuts().right()
# tv.shortcuts().enter()


# apps = tv.app_list()
# logging.info(apps)

if __name__ == '__main__':
	openPlex()