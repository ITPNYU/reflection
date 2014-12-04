import sys

activate_this = '/var/www/dev/simulacra/venv/simulacra-v1/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/dev/simulacra/simulacra')

from simulacra import app as application
