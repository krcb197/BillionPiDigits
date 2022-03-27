
import os
from collections import Counter

import requests
import pandas as pd
from tqdm import tqdm

def download(url: str, fname: str) -> None:
    """
    Download a file with a progress bar code from
    https://stackoverflow.com/questions/15644964/python-progress-bar-and-downloads

    :param url: url to download
    :param fname: filename to store in
    :return: None
    """
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)

url = 'https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt'
fname = 'pi-billion.txt'

if __name__ == '__main__':

    # download the file if it wasn't already downloaded
    if not os.path.exists(fname):
        download(url=url, fname='pi-billion.txt')

    with open(fname, 'r', encoding='utf-8') as fid:
        digits = fid.read()

    digits = digits.replace('.', '')


    # generate a pandas series with the analysis of digit occurence data
    digit_analysis = pd.Series(Counter(digits))
    digit_analysis.sort_index(inplace=True)

    # plot the data
    ax = digit_analysis.plot.bar()
    ax.hlines(y=1e9 / 10, xmin=-1, xmax=10, colors='k', linestyles='dotted')
    ax.set_ylim([(1e9 / 10)-20000, (1e9 / 10)+20000])
    ax.set_xlabel('Digit')
    ax.set_ylabel('Occurrence')
    ax.set_title(f'Analysis of Digits of π to 1 Billion digits \ndata from {url}')


