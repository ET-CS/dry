#!/usr/bin/env python
"""Dry.

Usage:
  dry build [--quiet | --verbose] [--c=<fn>]
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
from docopt import docopt
import os, sys, glob
sys.dont_write_bytecode = True
from subprocess import call

script_path = os.path.dirname(os.path.abspath(__file__))
project_path = os.getcwd()

verbose = False

# Get version from setup.py
package = "dry"
from pkg_resources import get_distribution, DistributionNotFound
import os.path
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

templating = False
try:
    import config as settings
    templating = settings.templating
except:
    pass

template_engine = 'jinja2'
if templating:
    try:
	import config as settings
	template_engine = settings.template_engine
    except:
	pass

template_context = {}
if templating:
    try:
	import config as settings
	template_context = settings.context
    except:
	pass

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

def css_import(filename):
    import jinja2
    return jinja2.Markup(loader.get_source(env, filename+'.min.css')[0])

def js_import(filename):
    import jinja2
    return jinja2.Markup(loader.get_source(env, filename+'.min.js')[0])

flattensubs = True



if templating:
    if template_engine=='jinja2':
        from jinja2 import Environment, FileSystemLoader
	if verbose:
	    print os.path.normpath(os.path.join(project_path,target_folder))
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
    if verbose:
	print "compiling css..."
    from rcssmin import cssmin
    types = ('.css', '.scss', '.less')
    for ftype in types:
        for filename in glob.glob(rootdir + "*" + ftype) :
	    if filename[:1]!='_':
	        if verbose:
	    	    print "compiling " + filename
	        index = filename.find(ftype)
	        output_filename = filename[:index] + '.min.css'
	        if target_css_folder != '':
		    output_filename = target_css_folder + output_filename
		if flattensubs:
		    output_filename = output_filename.replace(rootdir, '')
	        if ftype==".scss":
	    	    call(["scss", "-t", "compressed", filename, output_filename])
	    	if ftype==".less":
	    	    call(["lessc", filename, '-x', '--clean-css', output_filename, " > " + output_filename])
	    	if ftype==".css":
	    	    with open (filename, "r") as myfile:
		        css=myfile.read()
		    minified_css = cssmin(css)
		    with open(output_filename, "w") as text_file:
			text_file.write(minified_css)
    #return_code  = call(["compass", "compile"])
    #return_code  = call(["scss", "-t", "compressed", "index.css", "index.min.css"])
    #if return_code != 0:
    #    sys.exit("failed.");

def compileJS(rootdir = ""):
    if verbose:
	print "minifying js..."
    for filename in glob.glob(rootdir + '*.js') :
	if filename[:1]!='_':
	    index = filename.find('.js')
	    output_filename = filename[:index] + '.min.js'
	    output_filename = target_js_folder + output_filename
	    if flattensubs:
		output_filename = output_filename.replace(rootdir, '')
	    return_code = call(["minifyjs -m --level=1 -i "+filename+" -o "+output_filename], shell=True)
	    if return_code != 0:
		sys.exit("failed.");

def compileHTML(rootdir = ""):
    if verbose:
	print "minifying html..."
    from htmlmin.minify import html_minify
    for filename in glob.glob(rootdir + '*.html') :
	if filename[:1]!='_':
	    index = filename.find('.html')
	    output_filename = filename[:index] + '.min.html'
	    output_filename = target_folder + output_filename
	    if templating:
		if template_engine == 'jinja2':
		    html = env.get_template(filename).render(**template_context)
		elif template_engine == 'mako':
		    html = Template(filename=filename, lookup=mylookup).render(**template_context)
	    else:
	        with open (filename, "r") as myfile:
		    html=myfile.read()
	    minified_html = html_minify(unicode(html).encode('utf-8'))
	    #minified_html = html_minify(html)
	    if flattensubs:
	        output_filename = output_filename.replace(rootdir, '')
	    with open(output_filename, "w") as text_file:
	        text_file.write(minified_html.encode('utf8'))
	    if verbose:
		print output_filename + " filename written."

def buildAll():
    if verbose:
        print "Building project... ("+ project_path + ")"

    compileCSS()
    compileJS()
    compileHTML()

    exclude = set(['.sass-cache'])
    for subdir, dirs, files in os.walk("."):
        dirs[:] = [d for d in dirs if d not in exclude]
        for dir in dirs:
	    if dir + "/" != target_folder:
	        if verbose:
	    	    print "directory: " + dir
	        compileCSS(dir + "/")
    	        compileJS(dir + "/")
	        compileHTML(dir + "/")
    #print "compiling coffeescript"
    #return_code = call(["coyote -c index.coffee:javascripts/index.min.js"], shell=True)
    #if return_code != 0:
    #    sys.exit("failed.");
    if verbose:
        print "Done"

from watchdog.events import FileSystemEventHandler

class MyWatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
	if verbose:
	    print "Event on: " + event.src_path
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

def main():
    """Entry point for the application script"""
    arguments = docopt(__doc__, version=package.title() + " v" + version)
    verbose = arguments['--verbose']

    if verbose:
	print "Target Folder: " + target_folder + " (" + project_path +"/" + target_folder + ")"

    if arguments['build']:
	buildAll()

    if arguments['watch']:
	if verbose:
	    print "Watching " + project_path
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