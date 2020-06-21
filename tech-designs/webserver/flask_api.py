#!/usr/bin/env python3
from flask import Flask, send_from_directory
from flask_expects_json import expects_json
from gunicorn.app.base import BaseApplication

app = Flask(__name__)


@app.route("/health", methods=["GET"])
def health():
    return "OK", 200


schema = {
    "type": "object",
    "properties": {
        "addr": {"type": "string"},
        "login": {"type": "string"},
        "password": {"type": "string"},
    },
    "required": ["addr", "login"],
}


@app.route("/validate", methods=["POST"])
@expects_json(schema)
def validate_json():
    return "OK", 200


@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory("static", path)


class App(BaseApplication):
    def __init__(self, app, options, *args, **kwargs):
        self.app = app
        self.options = options
        super().__init__(*args, **kwargs)

    def load_config(self):
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.app


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.DEBUG)

    options = {
        "bind": "%s:%s" % ("127.0.0.1", "5000"),
        "workers": 1,
        "threads": 4,
        "worker_class": "gthread",
    }
    App(app, options).run()
