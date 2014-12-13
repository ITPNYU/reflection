import sys

activate_this = '/var/www/dev/reflection/venv/reflection-v1/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, '/var/www/dev/reflection/reflection')

from reflection import app as application
