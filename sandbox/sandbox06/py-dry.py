#!/usr/bin/env python
import dry

# build `index.html` file in this directory
dry.build('index.html')
print "index.min.html file created"

# clean all minified files
dry.clean()
print "build cleaned"

# minify html using dry
#print dry.htmlmin('<html>   <head></head>   <body>    </body>   </html>')