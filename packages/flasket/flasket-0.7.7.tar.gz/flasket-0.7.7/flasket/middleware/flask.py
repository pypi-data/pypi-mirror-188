r"""
Description
-----------

The :class:`flasket.middleware.flask.FlasketCLI` class will enable you to quickly create
and run a Flasket application through the Flask middleware.

It is composed of a :class:`~flasket.middleware.flask.FlasketCmdline` and a
:class:`~flasket.cli.FlasketSettings`. This will enable the following default command line
arguments to be proposed:

.. program:: flasket-dev

.. option:: -l HOST, --listen HOST

   The ip to listen on (default: localhost)

.. option:: -p PORT, --port PORT

   The port to listen on (default: 8080)

.. option:: -c CFGFILE, --cfgfile CFGFILE

   Use CFGFILE as configuration file, otherwise first file found in
   search path is used. (default search path: (...))

.. option:: --ui, --no-ui

   Enable the OpenAPI UI. Disable with :option:`--no-ui`. (default: enabled)

.. option:: --debug, --no-debug

  Enable debug mode. Disable with :option:`--no-debug`. (default: disabled)

A configuration dictionary will be built from the command line arguments, the configuration
file if specified and found, and the Flasket defaults for missing parameters. This
configuration dictionary will be fed to the Flasket application on startup.


Functions
---------

FlasketCLIHelper
^^^^^^^^^^^^^^^^

.. autofunction:: FlasketCLIHelper


Classes
-------

FlasketCmdline
^^^^^^^^^^^^^^

.. autoclass:: FlasketCmdline
  :show-inheritance:
  :members: __call__, add_arguments, transform

FlasketCLI
^^^^^^^^^^

.. autoclass:: FlasketCLI
  :show-inheritance:
  :members: run

Example\s
---------

Refer to the :ref:`Quickstart` section for usage example.

"""
import argparse
import os
import typing as t

from attr import define, field
from torxtools.ctxtools import suppress_traceback

from .. import Flasket, cli

__all__: t.List[str] = [
    "FlasketCLI",
    "FlasketCLIHelper",
    "FlasketCmdline",
]


class FlasketCmdline(cli.FlasketCmdline):
    """
    Class that defines and parses the command line arguments for Flask middleware FlasketCLI.

    Parameters
    ----------

    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments.
        Passed value will be merged with the default factory configuration.
    """

    def add_arguments(self, parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
        """
        Adds Flask middleware specific command line arguments :option:`--debug`, :option:`--no-debug`
        to the ArgumentParser.

        Parameters
        ----------
        parser: argparse.ArgumentParser

            a parser on which `add_argument` will be called

        Returns
        -------
        argparse.ArgumentParser
        """
        defaults = self._default_cfg
        debug = {True: "enabled", False: "disabled"}[defaults["server"]["debug"]]

        # fmt: off
        parser.add_argument(
            "--debug", action="store_true", default=None,
            help=f"Enable debug mode. Disable with --no-debug. (default: {debug})",
        )
        parser.add_argument(
            "--no-debug", action="store_false", default=None, dest="debug",
            help=argparse.SUPPRESS,
        )
        # fmt: on
        return parser


@define(kw_only=True, slots=False)
class FlasketCLI(cli.ABCFlasketCLI):
    """
    Flask middleware client class.

    Parameters
    ----------
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments and configuration.
        Passed value will be merged with the default factory configuration.

    settings_cfg: any, default: :class:`flasket.cli.FlasketSettings`

        Dictionary, or Callable that returns a dictionary for the settings arguments.
        Defaults to :class:`flasket.cli.FlasketSettings`

    cmdline_cfg: any, default: :class:`flasket.middleware.flask.FlasketCmdline`

        Dictionary, or Callable that returns a dictionary for the command line arguments.
    """

    # fmt: off
    _cmdline_cfg: t.Any = field(default=FlasketCmdline)
    _forced_cfg: t.Dict[str,t.Any] = field(default={"server": {"production": False, "flask": True}}, init=False)
    # fmt: on

    def _run(self, *args: t.Any, cfg: t.Dict[str, t.Any], rootpath: str = None, test:bool=False, **kwargs: t.Any) -> None:
        """
        Runs the middleware

        Parameters
        ----------
        cfg: dict

            dictionary containing configuration for the application

        rootpath: str, default: None

            path of root location: where the 'api', 'htdocs' and 'app' directories will be served
        """
        app = Flasket(*args, cfg=cfg, rootpath=rootpath, options=self._options, **kwargs)
        if not test:
            app.run(host=app.host, port=app.port, debug=app.debug, use_reloader=False, **kwargs)
        return app


def FlasketCLIHelper(*, cfgname: str = None, description: str = None, options: t.Dict[str, t.Any] = None) -> t.Any:
    """
    Flask middleware client helper class

    Parameters
    ----------
    cfgname: str

        Name of the configuration file

    description: str

        Description to be used in argparse

    options: str

        Dictionnary of options

    Example
    -------

    Refer to the :ref:`Quickstart` section for usage example.

    """
    return cli.FlasketCLIHelper(
        FlasketCLI,
        cfgname=cfgname,
        description=description,
        options=options,
    )
