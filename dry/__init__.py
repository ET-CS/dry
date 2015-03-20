#!/usr/bin/env python
"""Dry.

Usage:
  dry init
  dry build [--quiet | --verbose] [--c=<fn>]
  dry build <file> [--verbose]
  dry clean
  dry watch
  dry deploy
  dry (-h | --help)
  dry --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --c=<fn>      Configuration file name [default: dry.conf].
  --quiet       print less text
  --verbose     print more text

"""
from __future__ import print_function
__author__ = "Etay Cohen-Solal"
__copyright__ = "Copyright 2015, Etay Cohen-Solal"
__license__ = "GNU"
__maintainer__ = "Etay Cohen-Solal"
__status__ = "Development"

import sys
# don't write bytecode so config.pyc won't be created in each project dir
sys.dont_write_bytecode = True

import os

### -----------
### Directories
### -----------
# Dry path
script_path = os.path.dirname(os.path.abspath(__file__))
# Current working dir
current_working_dir = os.getcwd()
# Project path = current_working_dir
# TODO check parent(s) directory if it include .dry dir, then make it the project_dir instead
project_path = current_working_dir

# Get version from setup.py
package = "dry"
from pkg_resources import get_distribution, DistributionNotFound
try:
    _dist = get_distribution(package)
    # Normalize case for Windows systems
    dist_loc = os.path.normcase(_dist.location)
    here = os.path.normcase(__file__)
    if not here.startswith(os.path.join(dist_loc, package)):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = '(local)'
else:
    __version__ = _dist.version
version = __version__
# depreceated? both not used anymore.
#conf_file_name = "settings.py"
#conf_full_path = project_path + "/../" + conf_file_name
sys.path.append(project_path + "/.dry/")

###===--- Default settings
DEFAULT_VERBOSE = False
DEFAULT_TEMPLATING = False

###===--- Load Settings
# TODO create `config` dictionary instead of variables?

"""Verbose mode - generates more output"""
verbose = DEFAULT_VERBOSE
try:
    import config as settings
    verbose = settings.verbose
except:
    pass

"""HTML(s) are Templates"""
templating = DEFAULT_TEMPLATING
try:
    import config as settings
    templating = settings.templating
except:
    pass

"""Template engine to use for templates"""
template_engine = 'jinja2'
if templating:
    try:
	import config as settings
	template_engine = settings.template_engine
    except:
	pass

# import templates-engines as (needed)
if templating:
    if template_engine=='jinja2':
        import jinja2

"""Context to pass to all templates"""
template_context = {}
if templating:
    try:
	import config as settings
	template_context = settings.context
    except:
	pass

"""Where output files should be created. default: empty (current dir)"""
target_folder = ""
try:
    import config as settings
    target_folder = settings.target_folder
    if target_folder != '':
	if target_folder[-1:] != '/':
	    target_folder += '/'
    if not os.path.exists(target_folder):
	os.makedirs(target_folder)
except:
    pass

"""Where to save output css files"""
target_css_folder = target_folder
try:
    import config as settings
    target_css_folder = settings.target_css_folder
    if target_css_folder != '':
	if target_css_folder[-1:] != '/':
	    target_css_folder += '/'
    if not os.path.exists(target_css_folder):
	os.makedirs(target_css_folder)
except:
    pass

"""Where to save output js files"""
target_js_folder = target_folder
try:
    import config as settings
    target_js_folder = settings.target_js_folder
    if target_js_folder != '':
	if target_js_folder[-1:] != '/':
	    target_js_folder += '/'
    if not os.path.exists(target_js_folder):
	os.makedirs(target_js_folder)
except:
    pass

# Should dry minify html/css/js (default: True)
minify_html = True
minify_css = True
minify_js = True
# Import minification libraries (as needed)
if minify_html:
    from htmlmin.minify import html_minify
if minify_css:
    from rcssmin import cssmin

# What prefix and/or postfix to add to minified file name
minify_prefix = ''
minify_suffix = '.min'

# Jinja2 markup to inject css file
def css_import(filename):
    """Markup for Jinja2 template engine - allows the {{css}} markup to inject minified css file"""
    return jinja2.Markup(loader.get_source(env, filename+'.min.css')[0])

# Jinja2 markup to inject js file
def js_import(filename):
    """Markup for Jinja2 template engine - allows the {{css}} markup to inject minified js file"""
    return jinja2.Markup(loader.get_source(env, filename+'.min.js')[0])

flattensubs = True

###===--- Main part

import glob
from subprocess import call

if templating:
    if template_engine=='jinja2':
        from jinja2 import Environment, FileSystemLoader
	if verbose:
	    print(os.path.normpath(os.path.join(project_path,target_folder)))
        loader = FileSystemLoader([
    	    '.', 
	    #os.path.normpath( os.path.join(os.path.dirname(__file__),target_folder) )
	    target_folder,
        ])
	env = Environment(loader=loader)
        env.globals['css'] = css_import
        env.globals['js'] = js_import
    elif template_engine=='mako':
	from mako.template import Template
	from mako.lookup import TemplateLookup
	mylookup = TemplateLookup(directories=[project_path])

def compileCSS(rootdir = ""):
    types = ('.css', '.scss', '.less')
    for ftype in types:
        for filename in glob.glob(rootdir + "*" + ftype) :
	    if filename[:1]!='_':
	        index = filename.find(ftype)
	        output_filename = filename[:index] + '.min.css'
	        if target_css_folder != '':
		    output_filename = target_css_folder + output_filename
		if flattensubs:
		    output_filename = output_filename.replace(rootdir, '')
	        if ftype==".scss":
	    	    buildSCSSFile(filename, output_filename)
	    	if ftype==".less":
	    	    buildLESSFile(filename, output_filename)
	    	if ftype==".css":
	    	    buildCSSFile(filename, output_filename)
    #return_code  = call(["compass", "compile"])
    #return_code  = call(["scss", "-t", "compressed", "index.css", "index.min.css"])
    #if return_code != 0:
    #    sys.exit("failed.");

def buildJSFile(filename, output_filename):
    if verbose:
	print("compiling " + filename + " to " + output_filename)
    return call(["minifyjs -m --level=1 -i "+filename+" -o "+output_filename], shell=True)

def buildHTMLFile(filename, output_filename):
    if verbose:
	print("compiling " + filename + " to " + output_filename)
    if templating:
	if template_engine == 'jinja2':
	    html = env.get_template(filename).render(**template_context)
	elif template_engine == 'mako':
	    html = Template(filename=filename, lookup=mylookup).render(**template_context)
    else:
        with open (filename, "r") as myfile:
	    html=myfile.read()
    # TODO encode setting to allow user choose
    minified_html = html_minify(unicode(html).encode('utf-8'))
    #minified_html = html_minify(html)
    with open(output_filename, "w") as text_file:
        text_file.write(minified_html.encode('utf8'))
    return 0

def buildCSSFile(filename, output_filename):
    if verbose:
	print("compiling " + filename + " to " + output_filename)
    with open (filename, "r") as myfile:
        css=myfile.read()
	minified_css = cssmin(css)
	with open(output_filename, "w") as text_file:
	    text_file.write(minified_css)
    return 0

def buildSCSSFile(filename, output_filename):
    if verbose:
	print("compiling " + filename + " to " + output_filename)
    return call(["scss", "-t", "compressed", filename, output_filename])

def buildLESSFile(filename, output_filename):
    if verbose:
	print("compiling " + filename + " to " + output_filename)
    return call(["lessc", filename, '-x', '--clean-css', output_filename, " > " + output_filename])

def compileJS(rootdir = ""):
    for filename in glob.glob(rootdir + '*.js') :
	if filename[:1]!='_':
	    index = filename.find('.js')
	    output_filename = filename[:index] + '.min.js'
	    output_filename = target_js_folder + output_filename
	    if flattensubs:
		output_filename = output_filename.replace(rootdir, '')
	    return_code = buildJSFile(filename, output_filename)
	    if return_code != 0:
		sys.exit("failed.");

def compileHTML(rootdir = ""):
    for filename in glob.glob(rootdir + '*.html') :
	if filename[:1]!='_':
	    index = filename.find('.html')
	    output_filename = filename[:index] + '.min.html'
	    output_filename = target_folder + output_filename
	    if flattensubs:
	        output_filename = output_filename.replace(rootdir, '')
	    buildHTMLFile(filename, output_filename)

def buildFile(file):
    if file[-5:]=='.html':
	buildHTMLFile(file, file.replace('.html', '.min.html'))
	return
    if file[-4:]=='.css':
	buildCSSFile(file, file.replace('.css', '.min.css'))
    	return
    if file[-5:]=='.less':
	buildLESSFile(file, file.replace('.less', '.min.css'))
    	return
    if file[-5:]=='.scss':
	buildSCSSFile(file, file.replace('.scss', '.min.css'))
    	return
    if file[-3:]=='.js':
	buildJSFile(file, file.replace('.js', '.min.js'))
    	return

def buildAll():
    if verbose:
        print("building... ("+ project_path + ")")

    compileCSS()
    compileJS()
    compileHTML()

    exclude = set(['.sass-cache'])
    for subdir, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude]
        for dir in dirs:
	    if dir + "/" != target_folder:
	        if verbose:
	    	    print("directory: " + dir)
	        compileCSS(dir + "/")
    	        compileJS(dir + "/")
	        compileHTML(dir + "/")
    #print "compiling coffeescript"
    #return_code = call(["coyote -c index.coffee:javascripts/index.min.js"], shell=True)
    #if return_code != 0:
    #    sys.exit("failed.");
    if verbose:
        print("Done")

from watchdog.events import FileSystemEventHandler

class MyWatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
	if verbose:
	    print("Event on: " + event.src_path)
	if event.src_path[-5:]==".html":
    	    compileHTML()
	    for subdir, dirs, files in os.walk("."):
    		for dir in dirs:
		    if dir + "/" != target_folder:
	    		compileHTML(dir + "/")
	if event.src_path[-5:]==".scss" or event.src_path[-4:]==".css":
    	    compileCSS()
    	    compileHTML()
    	    for subdir, dirs, files in os.walk("."):
    		for dir in dirs:
		    if dir + "/" != target_folder:
			compileCSS(dir + "/")
	    		compileHTML(dir + "/")
	if event.src_path[-3:]==".js":
    	    compileJS()
    	    compileHTML()
    	    for subdir, dirs, files in os.walk("."):
    		for dir in dirs:
		    if dir + "/" != target_folder:
			compileJS(dir + "/")
	    		compileHTML(dir + "/")

sample_config_file = """# set target directory for output files
# you can also use something like: "../../static"
#target_folder = "static"
# Override target directory for css files
#target_css_folder = "../static/css"
# Override target directory for js files
#target_js_folder = "../static/js"

# Enabling templating will handle the .html files using Jinja2 templating engine,
# Which mean you can now write your code with more advanced tools like inheritance.
#templating = True

# Choose template engine to render templates. `jinja2` (default) or `mako`. applicable only when templating = True
#template_engine = 'mako'

# pass context into template engine. create as dict and dry will extract it when passing it to template engine,
# so you could use it with ${config['production']} in mako or {{ config.production }} in jinja2.
#context = { 'config': { 'PRODUCTION': True } }

# Be more Verbose
#verbose = True
"""

def init_current_directory():
    """Initialize and create dry config file(s) inside current directory"""
    settings_directory=project_path+'/.dry'
    settings_file=settings_directory+'/config.py'
    if os.path.isdir(settings_directory):
	# already initialized
	print("directory already initialized.")
	return
    # init
    os.makedirs(settings_directory)
    f = open(settings_file,'w')
    print(sample_config_file, file=f)
    f.close()

def main():
    """Entry point for the application script"""
    from docopt import docopt; arguments = docopt(__doc__, version=package.title() + " v" + version)
    global verbose
    verbose = arguments['--verbose']

    if verbose:
	print("target folder: " + target_folder + " (" + project_path +"/" + target_folder + ")")

    if arguments['init']:
	init_current_directory()

    if arguments['build']:
	if arguments['<file>']:
	    buildFile(arguments['<file>'])
	else:
	    buildAll()

    if arguments['watch']:
	if verbose:
	    print("Watching " + project_path)
        import time
	from watchdog.observers import Observer
	event_handler = MyWatchHandler()
	observer = Observer()
	observer.schedule(event_handler, project_path, recursive=True)
	observer.start()
	try:
	    while True:
	        time.sleep(1)
	except KeyboardInterrupt:
	    observer.stop()
	observer.join()

    if arguments['clean']:
	import shutil
	try:
	    shutil.rmtree('.sass-cache')
    	except:
    	    pass
	try:
	    for filename in glob.glob(target_folder+'*.min.html') :
    		os.remove( filename )
    	except:
    	    pass
	try:
	    for filename in glob.glob(target_css_folder+'*.min.css') :
    		os.remove( filename )
    	except:
    	    pass
	try:
	    for filename in glob.glob(target_css_folder+'*.min.css.map') :
    		os.remove( filename )
    	except:
    	    pass
    	try:
	    for filename in glob.glob(target_js_folder+'*.min.js') :
    		os.remove( filename )
    	except:
    	    pass
    	if target_folder != '':
	    if os.listdir(target_folder) == []:
		shutil.rmtree(target_folder)
    	if target_css_folder != '' and target_css_folder != target_folder:
	    if os.listdir(target_css_folder) == []:
		shutil.rmtree(target_css_folder)
    	if target_js_folder != '' and target_js_folder != target_folder and target_css_folder != target_js_folder:
	    if os.listdir(target_js_folder) == []:
		shutil.rmtree(target_js_folder)

if __name__ == "__main__":
    main()