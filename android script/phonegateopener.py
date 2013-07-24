import android
import urllib
import urllib2

droid = android.Android
gate_ip = 192.168.1.64:8080 #change this to your web server obv
password = 1111 #I suggest changing password here and in the web server

try:
	pi = urllib2.urlopen(gate_ip + "/gate?password=" + password)
	response = pi.read()
except  IOError:
	response = "Can't connect to gate, try again later."
finally:	
	droid.makeToast(response)
