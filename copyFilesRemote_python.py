from hashlib import md5
import argparse
from mmap import ACCESS_READ, mmap
import os
import re
import csv
import shutil
import logging

logging.basicConfig(filename='copy.log', filemode='w',
                    format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# set a format which is simpler for console use
formatter = logging.Formatter(
    '%(asctime)s - %(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)


def calMD5(path):
    # print(f"path3:{path}")
    with open(path) as file, mmap(file.fileno(), 0, access=ACCESS_READ) as file:
        return md5(file).hexdigest()


def getMD5(path):
    """
    input:  MD5sum filename
    ba8cbc11b4d4772da1819de2aa77c26f *RB10162_101_R1.fastq.gz
    4b8eb426bf2e1f95c9efa306bd6db4a4 *RB10162_101_R2.fastq.gz
    e059ec60e3b51f6a010b9d751dcb21d3 *RB10162_102_R1.fastq.gz
    f228c619a5c6cb3c364f92179b26be33 *RB10162_102_R2.fastq.gz
    return a dict of key:=filename, value:= MD5sum
    """
    dict_md5 = {}
    if os.path.isfile(path):
        with open(path) as tsv:
            for line in csv.reader(tsv, delimiter=' '):
                # print(line)
                md5, fname = line[0], line[-1]
                if fname[0] == '*':
                    fname = fname[1:]
                dict_md5[fname] = md5
    return dict_md5


def filterFiles(filelist, pattern: str = None):
    # Filtering only the files.
    flist = [f for f in filelist if os.path.isfile(f)]
    if not (pattern is None):
        # print(f"pattern before: {pattern}")
        # print(f"pattern type before: {type(pattern)}")
        pattern2 = re.compile(pattern)
        # print(f"patten: {pattern2}")
        # Filtering only the files.
        flist = [f for f in filelist if bool(re.search(pattern2, f))]
    return flist


def copyfiles(sourcefiles, targetDir, sourceMD5files=None, targetMD5files=None, dry_run=True):
    if sourceMD5files is not None:
        dict_sources = getMD5(sourceMD5files)
    if targetMD5files is not None:
        dict_targets = getMD5(targetMD5files)
    # print(dict_sources)
    # print(f"target:{dict_targets}")
    flist_toCopy = []
    for f in sourcefiles:
        # .split('/')
        fname = os.path.basename(f)
        # os.path.exists()
        path_t = os.path.join(targetDir, fname)
        copytag = False
        if not os.path.exists(path_t):
            # if target file not exist, then copy
            print(f"{path_t} does not exists.")
            logging.info(f"{path_t} does not exists.")
            copytag = True
        elif os.path.getsize(f) != os.path.getsize(path_t):
            print(f"{fname} file size does not match!")
            logging.info(f"{fname} file size does not match!")
            copytag = True
        else:
            if fname in dict_sources:
                md5_source = dict_sources[fname]
            else:
                md5_source = calMD5(f)
                str_source = f"md5 of newly calculated source file {f}:{md5_source}"
                print(f"{str_source}")
                logging.info(str_source)

            if fname in dict_targets:
                md5_target = dict_targets[fname]
            else:
                md5_target = calMD5(path_t)
                str_target = f"md5 of newly calculated target file {path_t}:{md5_target}"
                print(f"{str_target}")
                logging.info(str_target)

            if md5_source != md5_target:
                print(f"{fname} MD5 does not match!")
                logging.info(f"{fname} MD5 does not match!")
                copytag = True

        if copytag:  # and (not dry_run)
            flist_toCopy.append(f)
            print(f"Ready to copy:{f} ----> {path_t}\n")
            logging.info(f"Ready to copy:{f} ----> {path_t}\n")
            # print(f"dry_run: {dry_run}")
            # if dry_run == 'False' or dry_run == 'F':
            if not dry_run:
                print(f"copying {fname}....")
                logging.info(f"copying {fname}....")
                # print("aaaa")
                shutil.copyfile(f, path_t)
                print(f"{fname} Done\n")
                logging.info(f"{fname} Done\n")
        else:
            print(f"File {fname} are identical in both directories!\n")
            logging.info(f"File {fname} are identical in both directories!\n")

    return flist_toCopy


if __name__ == "__main__":
    # dir_current = os.getcwd()
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="The directory or files of the source")
    parser.add_argument("target", help="The directory or files of the target")
    parser.add_argument(
        "--p", nargs='?', help="The pattern of the copied files", default=None)
    parser.add_argument(
        "--md5a", nargs='?', help="files that contain MD5 of the source files", default=None)
    parser.add_argument(
        "--md5b", nargs='?', help="files that contain MD5 of the target files", default=None)
    # parser.add_argument("--dryRun", nargs='?', help="Dry run or nor?", default=True)
    parser.add_argument("--dryRun", nargs='?',
                        help="Dry run or nor?", default='T', type=lambda x: x.lower() not in ['false', 'f', 'no', '0', 'none', 'not'])
    args = parser.parse_args()
    p = args.p
    # if args.p is not None:
    #    p = str(args.p)
    # else:
    #    p=None
    print(f"file pattern: {p}")
    sourcefiles = os.listdir(args.source)
    sourcefiles = filterFiles(sourcefiles, p)  # Filtering only the files.
    sourcefiles = [os.path.join(args.source, f) for f in sourcefiles]
    print("files to be copied:")
    print(*sourcefiles, sep="\n")
    print("======================================\n")
    # print(type(args.dryRun))
    flistToCopy = copyfiles(sourcefiles=sourcefiles, targetDir=args.target,
                            sourceMD5files=f"{args.md5a}", targetMD5files=f"{args.md5b}", dry_run=args.dryRun)
    print("==============summmary================")
    for f in flistToCopy:
        print(f)
    print("==============  end  =================")
