import argparse
from . import config as cfg

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'Fractal Dimension',
        description = 'Provides methods for estimating the fractal dimension of image data.'
    )
    parser.add_argument(
        'filepath',
    )
    parser.add_argument(
        "-m", "--method",
        choices = cfg.methods,
        default= cfg.default_method,
        nargs='?',
        required = False,
        help = f"select a method to use from {cfg.methods}, defaults to {cfg.default_method}",
        dest = 'method'
    )
    return parser