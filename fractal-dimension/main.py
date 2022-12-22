from utilities import data, config as cfg
from pathlib import Path

def main():
    print(data.get_np_from_path(Path(cfg.image_path)))

if __name__ == "__main__":
    main()
