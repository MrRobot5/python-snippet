
#Import the urlopen factory function from the urllib module
from urllib import urlopen
#Fetch a module that will help you install other packages
data = urlopen('http://peak.telecommunity.com/dist/ez_setup.py')
#Write the downloaded module to a file on disk
open('ez_setup.py', 'wb').write(data.read())
