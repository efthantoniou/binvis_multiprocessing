import multiprocessing
from time import sleep, time
import binvis
import os
from tqdm import tqdm
import glob
import math


USAGE = 2

def check_duplicates(folder, dst):
    target = set([ (folder + os.path.basename(file)) \
        for file in glob.iglob(folder + '*') if not os.path.isdir(file)]) #

    dest = set([ (folder + os.path.basename(file.rsplit(".", 1)[0]))\
        for file in glob.iglob(dst + '*') if not os.path.isdir(file)]) #images

    continuation = list(target.symmetric_difference(dest))
    #continuation = [(folder + item) for item in continuation]

    return continuation



def calc(name):

    dst= folder +'images/'+ os.path.basename(name) + '.png'


    binvis.multi_folder(name, dst)

    pbar.update(multiprocessing.cpu_count() / USAGE)


def handler(folder):

    p = multiprocessing.Pool(multiprocessing.cpu_count() / USAGE)
    # with multiprocessing.Pool(multiprocessing.cpu_count() / USAGE) as p:
    #   temp = [file for file in glob.iglob(folder + '*') if not os.path.isdir(file)]
    #   r = list(tqdm( p.map(calc, ), total=len(temp)))
    p.map(calc, [file for file in glob.iglob(folder + '*')\
        if not os.path.isdir(file)])

def handler_continue(folder):

    p = multiprocessing.Pool(multiprocessing.cpu_count() / USAGE)
    p.map(calc, folder)

if __name__ == '__main__':

    folder = '/mnt/f/malware_backup/00320/'

    if os.path.isdir(folder + 'images/'):

        check = check_duplicates(folder, folder + 'images/')
        pbar = tqdm(total=len(check), desc='Files: ',position=0, ascii=True )
        handler_continue(check)
    else:
        os.mkdir(folder + 'images/')

        pbar = tqdm(total=len([log for log in glob.iglob(folder + '*')\
            if not os.path.isdir(log)]), desc='Files: ',position=0,\
            ascii=True )

        handler(folder)



    pbar.close()
