Dry
===

Automate and enhance your web development workflow

Dry will do for you in one command line `dry build`:

* compile & minify coffee scripts
* compile & minify sass & css
* minify js
* inject minified css/js into html
* minify html

working out-of-the-box in any directory with css/sass/cs/js/html files. no configuration whatsover needed but fully customized (target folder, templating, minify, etc.)

    This project is in early development stages and not intended yet for production.

## Install

```bash
pip install dry
```

## What can Dry do?

If you want to experiment with Dry: create an empty directory and add one .html file inside that folder. then run in your bash: `dry build` and see how Dry will minify that (and every) html in that folder. Now try adding some css or maybe js files and see how they are all minified too.
Dry supports also .scss/.sass files.

you can watch folder for changes using:
```bash
dry watch
```

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
You can create a settings.py file inside that folder with key=value pairs of settings.
Those are the settings available:
```python
# set target directory for output files
# you can also use something like: "../../public"
target_folder = "public"

# Enabling templating will handle the .html files as they were Jinja2 templating.
templating = True
```

### templating = True
By enabling templating in the settings Dry will pass the templates inside Jinja2 templating engine
which enables you to:
* Implement inheritence and other useful Jinja2 features.
* use the `{{ css('file') }}` and `{{ js('file') }}` inside the templates. this will embedded into the html the minified js or css file from the same project. for example let say you have 2 files `index.html` and `index.css`, by using `{{ css('index') }} inside `index.html` the result minified css of `index.css` will be embedded into the final minified html of `index.html`.

push commits and help creating documentation will be gratefully accepted.

by ET-CS (Etay Cohen-Solal)
