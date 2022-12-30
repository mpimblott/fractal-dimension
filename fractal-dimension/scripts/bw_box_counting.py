import logging
from tqdm import tqdm
import math
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
'''
box counting for images with only 2 colours
'''
def box_count(img_arr: np.ndarray, calibre: int, offset = np.asarray([0,0]), plot = False):
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
        hblock_idx = h * calibre - offset[0]
        for v in range(0, v_blocks):
            vblock_idx = v * calibre - offset[1]
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

def process_img(arr, plot = True):
    arr = np.nan_to_num(arr)
    uniques = np.unique(arr)
    white = np.amax(uniques)
    black = np.amin(uniques)
    logging.info(f"black value is {black}, white value is {white}")
    range = white - black
    midpoint = int(range/2)
    logging.info(f"midpoint is {midpoint}")
    arr[arr<midpoint] = black
    arr[arr>=midpoint] = white
    uniques, counts = np.unique(arr, return_counts=True)
    logging.info(f"rescaled data to classes {uniques}, {counts}")
    if plot:
        plt.imshow(arr, cmap='gray')
        plt.title('rescaled img')
        plt.savefig('rescaled img')
    return arr

def generate_offset_series(num, calibre):
    if num == 1:
        return np.asarray([0])
    sample = np.random.randint(1, calibre - 1, (num-1,2), int)
    offsets = np.insert(sample , 0, np.asarray([0,0]),0)
    logging.info(f"using offsets {offsets}")
    return offsets

def black_white_box_count(img_arr: np.ndarray, offsets = 5):
    img_arr = process_img(img_arr)
    size = img_arr.shape
    logging.info(f"starting black-white box counting for image of shape {size}")
    min_dim = min(size)
    # calculate the maximum base to use when calculating box sizes
    max_idx = math.floor(math.log(min_dim,2))
    calibres = np.asarray([2**i for i in range(2, max_idx)]).astype(int)
    scales = calibres / min_dim # r = s/M
    logging.info(f"using calibres {calibres}")
    logging.info(f"corresponding to scales {scales}")
    results = [] # n_{r}
    # calculate a series of offsets to use
    biggest_block = np.amax(calibres)
    offsets = generate_offset_series(offsets, biggest_block)
    for offset in offsets:
        r = []
        for i in tqdm(calibres):
            r.append(box_count(img_arr, i, offset))
        alpha = optimize.curve_fit(lin, xdata=np.log(1/scales), ydata=np.log(r))[0]
        logging.info(f"calculated regression {alpha} for offset {offset}")
        results.append(alpha)
        # plot regression
        log_plt = plt.figure()
        ax = log_plt.add_subplot(1,1,1)
        ax.plot(np.log(1/scales), np.log(r), 'b.')
        ax.plot(np.log(1/scales), alpha[0]*np.log(1/scales) + alpha[1], 'r')
        ax.set_xlabel('log(M/calibre)')
        ax.set_ylabel('log(count)')
        ax.set_title(f"offset = {offset}, D = {alpha[0]}")
        log_plt.savefig(f'offset:{offset}')

    logging.info(f"calculated linear regressions: {results}")
    # use least squares linear regression to calculate the fractal dimension

    # data_plt = plt.figure()
    # ax1 = data_plt.add_subplot(1,1,1)
    # ax1.plot(calibres, results, 'b.')
    # ax1.set_xlabel('calibre')
    # ax1.set_ylabel('count')
    # data_plt.savefig('data')