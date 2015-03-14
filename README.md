Dry
===

Automate and enhance your web development workflow

[![Build Status](https://travis-ci.org/ET-CS/dry.svg?branch=master)](https://travis-ci.org/ET-CS/dry)

## Try it!

Create one HTML file (or js file, or css file, or sass file, or less file...) inside empty directory,
then run the command `dry build` and see how it's minified in seconds. no matter what file. no matter how many files.

## What Dry knows to do?

To efficiently serve your website, you need to create some workflow where you minify and compress your js/css/html parts.
Dry will do for you in one command line `dry build`:

* compile & minify js
* compile & minify sass & css stylesheets
* can inject minified css/js into html
* minify html or html template

## Dry philosophy

There's a lot of Task Runners out there like Grunt or Gulp. Dry philosophy is:

1. Automate the automation - Enough with long configuration files full of code - Environment should be be set-up in minimum effort and time.
2. Watch my back and do it fast! - files should be compiled again as touched in background. `dry watch` should compile only touched files (and files dependent on that file) and not the entire project.
3. Efficient - Your webserver should work with minified files. minification in each request is a bad practice.

working out-of-the-box in any directory with css/sass/js/html files. no configuration whatsover needed but fully customized (target folder, templating, minify, etc.)

    This project is in early development stages and not intended yet for production.

## What special about Dry.

It's EASY!

Easy to install (pip install dry), easy to configure (just works!) and easy to use (rememberable three digits command - dry)

with just one simple command: `dry build` you will make your app PRODUCTION READY!

no more with writing long .configuration files like in grunt or gulp. config your environment with config in .ini style (but only better - a .py file!).
your configuration file should be look like something like this:

config.py
```
target_folder = "public"
target_css_folder = "/public/css"
target_js_folder = "../static/js"
```

That's it! no pipeline, no plugins to install and configure - everything bundled in. you can build .css, .less, .sass, .scss, .js, .html, jinja2 templates and mako templates OUT-OF-THE-BOX (and many more file types will follow soon - maybe you'll push the commit for some of them!)

### Compile only one file

Whenever you need to minify or compile any file: .SCSS, .LESS, .JS just use the:
```
dry build myfile.scss
```

### Dynamic HTMLs
Today most modern applications aren't just simple static HTML files. most backends are using one or other html templating engine.
Dry philosophy is to automate your assets managment so you could go for production with your website in just one simple command (`dry build`). 
In production your website should use minified templates (without inheritance or any other costly feature) and not minify the result in each request.
You can even use dry to build minified templates to use in your template engine.
Because Dry uses Jinja2 template engine and Mako template engine (and others will be added later) - you could do all templating inheritance before compiling your files - which mean you will work in organized structure and the final htmls that your website will serve will be simple static, preminified and compressed.

#### Conflict between template engines

If your final template engine (which you use in your application) syntax is similar to Jinja2 syntax {{var}}, and you wish to use the `templating` feature of dry to preminify and remove inheritance from your templates - you'll have to use mako templating or use Jinja2 {{ '{{var}}' }} syntax as a workaround.

so for example, if you use mustache as your website templating engine, let's take 2 files:

index.html:
```
{% extends "_site.html" %}

{% block main %}
    <h1>Hello, world!</h1>
{% endblock %}
```

_site.html:
```
<!DOCTYPE HTML>
<html>
    <head>
	<title>{{ '{{title}}' }}</title>
    </head>
    <body>
	<main>
	    {% block main %}{% endblock %}
	</main>
    </body>
</html>
```

after running the `dry build` command you will get the result minified html:

index.min.html:
```
<!DOCTYPE HTML><html><head><title>{{title}}</title></head><body><main><h1>Hello, world!</h1></main></body></html>
```
with the included {{title}} so you could pass data to your template engine from your controller.

## Install

```bash
pip install dry
```

or clone and install from source to enjoy latest commits:
```bash
git clone https://github.com/ET-CS/dry.git
cd dry
python setup.py install
```

## What can Dry do?

If you want to experiment with Dry: create an empty directory and add one .html file inside that folder. then run in your bash: `dry build` and see how Dry will minify that (and every) html in that folder. Now try adding some css or maybe js files and see how they are all minified too.
Dry supports also .scss/.sass files.

you can watch folder for changes using:
```bash
dry watch
```

Check also the examples in the `/sandbox` directory try, see and learn how Dry build your source.

## Usage

Help on `dry` cli commands:
```bash
dry
```
or
```bash
dry -h
```

## Settings
Although Dry works out-of-the-box, You can (and should) create a settings.py file inside your project folder with key=value pairs of settings.
Currently those are the available settings for dry:
```python
# set target directory for output files
# you can also use something like: "../../public"
target_folder = "public"
# Override target directory for css files
target_css_folder = "../static/css"
# Override target directory for js files
target_js_folder = "../static/js"

# Enabling templating will handle the .html files using Jinja2 templating engine,
# Which mean you can now write your code with more advanced tools like inheritance.
templating = True

# Choose template engine to render templates. `jinja2` (default) or `mako`. applicable only when templating = True
template_engine = 'mako'

# pass context into template engine. create as dict and dry will extract it when passing it to template engine,
# so you could use it with ${config['production']} in mako or {{ config.production }} in jinja2.
context = { 'config': { 'PRODUCTION': True } }

```

### templating = True
By enabling templating in the settings Dry will pass the templates through Jinja2/Mako templating engine
which enables you to:
* Implement inheritence and other useful Jinja2/Mako features.
* use the `{{ css('file') }}` and `{{ js('file') }}` inside the templates. this will embedded into the html the minified js or css file from the same project. for example let say you have 2 files `index.html` and `index.css`, by using `{{ css('index') }}` inside `index.html` the result minified css of `index.css` will be embedded into the final minified html of `index.html`.

NOTE: {{ css() }} and {{ js() }} directives currently available only using `jinja2` template_engine.

push commits and help creating documentation will be gratefully accepted.

by ET-CS (Etay Cohen-Solal)
