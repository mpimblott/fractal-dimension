import logging
from utilities import arg_parsing, data_utils, config as cfg
from pathlib import Path
import numpy as np

from scripts.bw_box_counting import black_white_box_count

def main():
    logging.basicConfig(
        level=logging.INFO
    )
    parser = arg_parsing.get_parser()
    args = parser.parse_args()
    method = args.method
    data_path = args.filepath
    print(data_path)
    data = data_utils.get_np_from_path(data_path)
    black_white_box_count(data)

if __name__ == "__main__":
    main()
