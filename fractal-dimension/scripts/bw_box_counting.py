import logging
from tqdm import tqdm
import math
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
'''
box counting for images with only 2 colours
'''
def box_count(img_arr: np.ndarray, calibre: int, plot = False):
    '''
    perform a box count pass.

    Args:
        calibre (int): the size of the boxes in pixels

    Returns:
        nparray of counts, in this case representing if the box contains any detail.
    '''
    size = img_arr.shape
    h_blocks = size[0] // calibre
    v_blocks = size[1] // calibre
    #logging.info(f"splitting image of shape {size} into h: {h_blocks} x v: {v_blocks} blocks of calibre {calibre}")
    # count is the number of boxes that contained any foreground detail
    count = 0
    for h in range(0, h_blocks):
        hblock_idx = h * calibre
        for v in range(0, v_blocks):
            vblock_idx = v * calibre
            #logging.info(f"block h: {hblock_idx}:{hblock_idx+calibre}, v: {vblock_idx}:{vblock_idx+calibre}")
            subarr = img_arr[vblock_idx:vblock_idx + calibre, hblock_idx:hblock_idx+calibre]
            if 255 in subarr:
                count += 1
            if plot:
                plt.imshow(subarr, cmap='gray')
                plt.title(count)
                plt.savefig(f"{hblock_idx}{vblock_idx}")
    return count
    
def lin(x, a, b):
    y = a * x + b
    return y

def black_white_box_count(img_arr: np.ndarray):
    size = img_arr.shape
    logging.info(f"starting black-white box counting for image of shape {size}")
    min_dim = min(size)
    max_idx = math.floor(math.log(min_dim, 2))
    calibres = np.asarray([2**i for i in range(2, max_idx)])
    scales = calibres / min_dim
    logging.info(f"using calibres {calibres}")
    logging.info(f"corresponding to scales {scales}")
    results = []
    for i in tqdm(calibres):
        results.append(box_count(img_arr, i))
    logging.info(results)
    # use least squares linear regression to calculate the fractal dimension
    plt.plot(np.log(1/ scales), np.log(results), 'b.')
    plt.xlabel('r')
    plt.ylabel('count')
    alpha = optimize.curve_fit(lin, xdata=np.log(scales), ydata=np.log(results))[0]
    logging.info(f"calculated regression to be {alpha}")
    plt.plot(np.log(scales), alpha[0]*np.log(scales) + alpha[1], 'r')
    D = alpha[1]/alpha[0]
    plt.title(D)
    plt.savefig('results')
