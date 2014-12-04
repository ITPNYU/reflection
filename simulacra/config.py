from ConfigParser import SafeConfigParser
from os.path import abspath, join, normpath

config = SafeConfigParser()
config_path = normpath(join(abspath(__file__), '..', '..', 'app.cfg'))
config.read(config_path)
