Dry
===

Automate and enhance your web development workflow

## What does it mean?

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
3. Efficient - Your webserver should work with minified files. minification is each request is a bad thing.

working out-of-the-box in any directory with css/sass/js/html files. no configuration whatsover needed but fully customized (target folder, templating, minify, etc.)

    This project is in early development stages and not intended yet for production.

### Dynamic HTMLs
Most modern websites aren't just simple static HTMLs. most backends are using one or other html templating engine.
Dry philosophy says that you should use minified templates for you website without inheritance or any other costly feature.
You should use dry to build minified templates to use in your template engine.
Because Dry uses Jinja2 template engine (and other engines will be added later) - you can do all the inheritance before compiling your files - which mean you will work in organized structure and the final htmls you website will serve will be as simple as can be - preminified and compressed.
If your template engine syntax is different then Jinja2 syntax {{var}} you have no problem, but if they are similar you can use Jinja2 {{ '{{var}}' }} syntax to workaround this.

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

# Enabling templating will handle the .html files using Jinja2 templating engine,
# Which mean you can now write your code with more advanced tools like inheritance.
templating = True
```

### templating = True
By enabling templating in the settings Dry will pass the templates inside Jinja2 templating engine
which enables you to:
* Implement inheritence and other useful Jinja2 features.
* use the `{{ css('file') }}` and `{{ js('file') }}` inside the templates. this will embedded into the html the minified js or css file from the same project. for example let say you have 2 files `index.html` and `index.css`, by using `{{ css('index') }} inside `index.html` the result minified css of `index.css` will be embedded into the final minified html of `index.html`.

push commits and help creating documentation will be gratefully accepted.

by ET-CS (Etay Cohen-Solal)
