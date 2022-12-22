from PIL import Image
import numpy as np
from pathlib import Path
import config as cfg

def main():
    im = Image.open(cfg.image_path).convert('L')
    print(np.asarray(im))

if __name__ == "__main__":
    main()
