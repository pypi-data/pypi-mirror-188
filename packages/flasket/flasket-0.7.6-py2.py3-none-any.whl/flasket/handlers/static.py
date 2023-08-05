import functools
import os

from attrs import define, field
from flask import Blueprint, Flask, send_from_directory

from ._utils import Handler, handler


@handler
@define(kw_only=True, slots=False)
class StaticHandler(Handler):
    _prefix: str = field(default="/")
    _static_rootpath: str = field(init=False, default=None)

    @staticmethod
    def name() -> str:
        """ """
        return "static"

    @property
    def prefix(self) -> str:
        return self._prefix

    def __attrs_post_init__(self) -> None:
        # Search for ./static, then for ./htdocs
        rootpath = self.rootpath
        if os.path.exists(os.path.join(rootpath, "static")):
            filepath = os.path.join(rootpath, "static")
            self._static_rootpath = filepath
            self.logger.info(f'Reading static files from "{filepath}" directory.')
        elif os.path.exists(os.path.join(rootpath, "htdocs")):
            filepath = os.path.join(rootpath, "htdocs")
            self._static_rootpath = filepath
            self.logger.info(f'Reading static files from "{filepath}" directory.')
        else:
            self._static_rootpath = os.path.join(rootpath, "static")
            self.logger.warning("Neither 'static' nor 'htdocs' directories in root path exist.")

        # Use None for static_folder to prevent adding a automatic "/<filename>" route
        self._flask = Flask(__name__, root_path=self._static_rootpath, static_folder=None, template_folder=None)
        blueprint = Blueprint(
            "static",
            __name__,
            root_path=self._static_rootpath,
            static_folder=None,
            template_folder=None,
        )
        blueprint.add_url_rule("/<path:path>", view_func=self.send_file)
        self.flask.register_blueprint(blueprint)

        # TODO: Allow a cfg option 'redirect' from '/' to x
        if self.prefix == "/":
            redirect_fn = functools.partial(self.redirect, location="/app/", code=308)
            redirect_fn.__name__ = "redirect"
            blueprint = Blueprint(
                "redirect",
                __name__,
                root_path=self.rootpath,
                static_folder=None,
                template_folder=None,
            )
            blueprint.add_url_rule("/", view_func=redirect_fn)
        self.flask.register_blueprint(blueprint)

    def send_file(self, path: str) -> object:
        return send_from_directory(path=path, directory=self._static_rootpath)
