# -*- coding: utf-8 -*-
from flask.ext.assets import Bundle, Environment

less = Bundle(
	"less/main.less",
    filters="less",
    output="public/css/common.css",
    depends=('*.less', '**/*.less')
)

js = Bundle(
    "libs/jQuery/dist/jquery.js",
    "libs/bootstrap/dist/js/bootstrap.min.js",
    "js/plugins.js",
    "js/script.js",
    output="public/js/common.js"
)

assets = Environment()

assets.register("js_all", js)
assets.register("css_all", less)
