#!/usr/bin/env python3

import os
import sys

from idpyoidc.client.configure import Configuration
from idpyoidc.client.configure import RPHConfiguration
from idpyoidc.configure import create_from_config_file
from idpyoidc.ssl_context import create_context

from werkzeug.middleware.proxy_fix import ProxyFix

try:
    from . import application
except ImportError:
    import application

dir_path = os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    conf = sys.argv[1]
    name = 'oidc_rp'
    template_dir = os.path.join(dir_path, 'templates')

    _config = create_from_config_file(Configuration,
                                      entity_conf=[{"class": RPHConfiguration, "attr": "rp"}],
                                      filename=conf)

    app = application.oidc_provider_init_app(_config.rp, name, template_folder=template_dir)
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    
    _web_conf = _config.web_conf
    context = create_context(dir_path, _web_conf)

    debug = _web_conf.get('debug', True)
    app.run(host=_web_conf["domain"], port=_web_conf["port"],
            debug=_web_conf.get("debug", False), ssl_context=context)
