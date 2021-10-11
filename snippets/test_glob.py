import glob
from pathlib import Path


def listing(path: Path, recursive=False):
    return [Path(_) for _ in glob.glob(str(path), recursive=recursive)]


def folders(path: Path, recursive=False):
    return [_ for _ in listing(path, recursive=recursive) if _.is_dir()]


path = Path('/home/jan/*.*')
path = Path('/home/jan/sandbox/car-for-marketing/**')
print(folders(path))





find_sources(path)
files = glob.glob(str(path), recursive=True)
for file in files:
    print(Path(file).is_dir())
print(files)


# car-for-marketing/DMC_BLA_BLA/data/