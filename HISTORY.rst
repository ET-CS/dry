.. :changelog:

Release History
---------------

X.X.X (Future)
++++++++++++++

**Improvements**

- Verbose setting in config (like --verbose)

0.1.1 (2015-03-14)
++++++++++++++++++

**Improvements**

- New command: `dry init` which creates `/.dry` folder with sample `config.py` file inside.
- New command: `dry build <filename> will build only that file.

0.1.0 (2015-02-22)
++++++++++++++++++

**Behavioural Changes**

- Dry will no more search for `settings.py` file, but instead for `config.py` file inside `.dry` directory.

**Improvements**

- Supporting Mako template engine and new `template_engine` setting.
- New `target_css_folder` and `target_js_folder` settings to set output directory for rendered .js and .css files.
- New `context` setting to pass variables into templates.

0.0.5 (2015-02-21)
++++++++++++++++++

**Improvements**

- Supporting .less files using `lessc` command.

0.0.4 (2015-02-07)
++++++++++++++++++

- Birth!

0.0.1 - 0.0.3
+++++++++++++

- Frustration
- Conception