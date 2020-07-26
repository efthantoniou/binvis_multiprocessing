import multiprocessing as mp
from time import sleep, time
import binvis
import os
from tqdm import tqdm
import glob
import math


USAGE = 2

def check_duplicates(folder, dst):
    target = set([ (folder + os.path.basename(file)) \
        for file in glob.iglob(folder + '*') if not os.path.isdir(file)])

    dest = set([ (folder + os.path.basename(file.rsplit(".", 1)[0]))\
        for file in glob.iglob(dst + '*') if not os.path.isdir(file)])

    continuation = list(target.symmetric_difference(dest))
    return continuation

def get_result(result):
    global results
    results.append(result)




def calc(i, name):

    dst= folder +'images/'+ os.path.basename(name) + '.png'


    binvis.multi_folder(name, dst)

    pbar.update(mp.cpu_count() / USAGE)

    return (i, name)


def handler(folder):

    pool = mp.Pool(mp.cpu_count() / USAGE)
    #p.map(calc, [file for file in glob.iglob(folder + '*')\
    #    if not os.path.isdir(file)])
    temp = [file for file in glob.iglob(folder + '*') if not os.path.isdir(file)]
    for i, name in enumerate(temp):
        pool.apply_async(calc, args=(i, name), callback=get_result)
    pool.close()
    pool.join()

def handler_continue(folder):

    pool = mp.Pool(mp.cpu_count() / USAGE)
    #p.map(calc, folder)
    for i, name in enumerate(folder):
        pool.apply_async(calc, args=(i, name), callback=get_result)
    pool.close()
    pool.join()

if __name__ == '__main__':

    folder = '/mnt/f/malware_backup/00322/'

    results = list()
    start = time()
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
    print("Elapsed time: ", time() - start)



    pbar.close()
