r"""
Description
-----------

A binary helper for both flask and gunicorn middleware are proposed as :program:`flasket-dev` and :program:`flasket`. They can serve content from this repository.

Example\s
---------

Refer to the :ref:`Quickstart` section for usage example.

"""
import argparse
import os
import sys
import typing as t

from torxtools import xdgtools
from torxtools.cfgtools import which
from torxtools.pathtools import expandpath
from yaml import safe_load

from ._utils import deepmerge
from .defaults import CFGFILE_SEARCH_PATHS, default_configuration
from .middleware import FlaskFlasketCreator, GunicornFlasketCreator

__all__: t.List[str] = [
    "create",
]


def _read(cfgfile: str) -> t.Dict:
    """
    Convenience function in order to be mocked.

    Parameters
    ----------
    cfgfile: str

        a single path representing a yaml file.

    Returns
    -------
    dict:

        a dictionary
    """
    with open(cfgfile, encoding="UTF-8") as fd:
        data = safe_load(fd)
    return data or {}


def _create_arguments(
    *,
    argv,
    cfgfile,
    creator_class,
    defaults,
    description,
    cfgfilepaths,
):
    """ """
    if not argv:
        return {}

    # argument_default=None does not set the default to None for boolean options,
    # so we'll specifically set default=None for those values
    #
    # Default values aren't actually added/set here, but in the FlasketSettings,
    # We only care about values that were specified.
    parser = argparse.ArgumentParser(
        description=description,
        argument_default=None,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # Create helptext for UI option
    b_ui = {True: "enabled", False: "disabled"}[defaults["server"]["ui"]]
    if cfgfilepaths:
        # Keep on two lines, otherwise line continuation will make
        # an obsure argparse bug appear
        helpmsg_cfgfile = "Use CFGFILE as configuration file, "
        helpmsg_cfgfile += f"otherwise first file found in search path is used. (default search path: {cfgfilepaths})"
    else:
        helpmsg_cfgfile = "Use CFGFILE as configuration file."

    # fmt: off
    parser.add_argument(
        "-l", "--listen", metavar="HOST",
        help=f'The ip to listen on (default: {defaults["server"]["listen"]})',
    )
    parser.add_argument(
        "-p", "--port", metavar="PORT", type=int,
        help=f'The port to listen on (default: {defaults["server"]["port"]})',
    )
    if not cfgfile:
        parser.add_argument(
        "-c", "--cfgfile", metavar="CFGFILE",
        help=helpmsg_cfgfile,
        )
    parser.add_argument(
        "--ui", action="store_true", default=None,
        help=f"Enable the OpenAPI UI. Disable with --no-ui. (default: {b_ui})",
    )
    parser.add_argument(
        "--no-ui", action="store_false", default=None, dest="ui",
        help=argparse.SUPPRESS,
    )
    # fmt: on
    creator_class.add_arguments(defaults["server"], parser)
    args = parser.parse_args(argv)
    return vars(args)


def create(
    rootpath: str,
    middleware: str = "gunicorn",
    *,
    argv: t.List[str] = None,
    cfgfile=None,
    cfgfilename="flasket.yml",
    cfgfilepaths=None,
    default_cfg: t.Dict[str, t.Any] = None,
    description="Flasket server",
):
    """
    Parameters
    ----------
    argv: list[str], default: None

        Uses :code:`sys.argv[1:]` if None
    default_cfg: dict, default: :meth:`flasket.defaults.default_configuration`

        Dictionary containing the defaults for the command line arguments and configuration.
        Passed value will be merged with the default factory configuration, command line arguments
        and the configuration file that was read.

    rootpath: str, default: None

        path of root location: where the 'api', 'htdocs' and 'app' directories will be served.

    """
    # rootpath was probably passed by "__file__"
    if rootpath and os.path.isfile(rootpath):
        rootpath = os.path.dirname(rootpath)

    # Sets environment variables for XDG paths
    xdgtools.setenv()

    # Verify middleware exists
    middleware = middleware.lower().strip()
    if middleware not in ["flask", "gunicorn"]:
        raise ValueError('middleware argument must be in ["flask", "gunicorn", "test"]')
    if middleware == "flask":
        creator_class = FlaskFlasketCreator()
    if middleware == "gunicorn":
        creator_class = GunicornFlasketCreator()

    # Prepare search path for configuration file. Disable it if we're looking
    # for a impossible (None) file name
    if cfgfilepaths is None:
        cfgfilepaths = CFGFILE_SEARCH_PATHS
    cfgfilepaths = [e.format(cfgfilename=cfgfilename) for e in cfgfilepaths]

    # Create a default configuration from what was passed
    # and what we set. Other values are filtered
    defaults = default_configuration(default_cfg)

    # Parse arguments if they exist
    if argv is None:
        argv = sys.argv[1:]

    arguments = _create_arguments(
        argv=argv,
        cfgfile=cfgfile,
        cfgfilepaths=cfgfilepaths,
        creator_class=creator_class,
        defaults=defaults,
        description=description,
    )

    # Copy arguments over to an dict with server
    arguments = {k: v for k, v in arguments.items() if v is not None}
    cfgfile = arguments.pop("cfgfile", cfgfile)
    arguments = {"server": arguments}

    # Search for the configuration file
    if not cfgfile and cfgfilepaths:
        # Search for cfgfile
        cfgfilepaths = [e.format(cfgfilename=cfgfilename) for e in cfgfilepaths]
        cfgfile = which(cfgfile, expandpath(cfgfilepaths))

    filedata = _read(cfgfile) or {}

    # Merge in the reverse order of priority
    cfg = defaults
    cfg = deepmerge(cfg, filedata)
    cfg = deepmerge(cfg, arguments)
    creator_class.force_cfg(defaults["server"])

    return creator_class.flasket(rootpath=rootpath, cfg=cfg)
