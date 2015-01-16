# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

less = Bundle(
	"less/*.less",
    "less/**/*.less",
    filters="less",
    output="public/css/common.css"
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.min.js",
    "js/plugins.js",
    "js/script.js",
    filters='jsmin',
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", less)
