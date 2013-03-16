import os
import yaml

def get(name):
	try:
		fname = "{0}/{1}.yaml".format(os.path.dirname(__file__), name)
		return yaml.load(file(fname, 'r'))
	except (IOError, yaml.YAMLError):
		return {}
