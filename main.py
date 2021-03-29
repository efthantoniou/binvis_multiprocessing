import multiprocessing
from time import sleep, time
import binvis
import os
from tqdm import tqdm
import glob
import math
import sys
import argparse




destination = '../images/'


def check_duplicates(folder, dst):
    target = set([ (folder + os.path.basename(file)) \
        for file in glob.iglob(folder + '*') if not os.path.isdir(file)])

    dest = set([ (folder + os.path.basename(file.rsplit(".", 1)[0]))\
        for file in glob.iglob(dst + '*') if not os.path.isdir(file)])

    continuation = list(target.symmetric_difference(dest))
    return continuation



def calc(name):
    
    temp1 = name.split('/')[-2]
    temp2 = name.split('/')[-1]
    
    if not os.path.exists(folder + destination + temp1):
        os.makedirs(folder + destination + temp1)

    dst = folder + destination + temp1 + '/' + temp2 + '.png'


    binvis.multi_folder(name, dst)

    pbar.update(args.cores)


def handler(folder):

    p = multiprocessing.Pool(args.cores)
    p.map(calc, [file for file in glob.iglob(folder + '**/*')])
    p.close()
    p.join()

"""def handler_continue(folder):

    p = multiprocessing.Pool(args.cores)
    p.map(calc, folder)
    p.close()
    p.join()"""

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-pf', '--profiling', type=str, help='Give full path name of file for profiling.')
    parser.add_argument('-s', '--source', type=str, help='Give folder with binaries to save images. Format(/folder/folder/)')
    parser.add_argument('-c', '--cores', type=int, default=1, help='Number of cores to utilize')
    args = parser.parse_args()

    if args.profiling:
        binvis.profiling(args.profiling, args.profiling + '.png')
        sys.exit(0)


    if args.source:
        folder = args.source
        print(folder)
    else:
        print("No input was provided. Check the help!")
        sys.exit(0)

    if os.path.isdir(folder + destination):

        check = check_duplicates(folder, folder + 'images/')
        pbar = tqdm(total=len(check), desc='Files: ',position=0, ascii=True )
        print('The function handler_continue is under maintenance.')
        #handler_continue(check)
    else:
        os.mkdir(folder + destination)

        pbar = tqdm(total=len([log for log in glob.iglob(folder + '**/*')\
            if not os.path.isdir(log)]), desc='Files: ',position=0,\
            ascii=True )

        handler(folder)



    pbar.close()
