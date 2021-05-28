import os
from pathlib import Path

path = Path('/home/example/upload.m4a')
print(path.stem, path.name, path.suffix, path.parents[0])

assets_folder = '/home/example/assets'
file = "acme.m4a"
path = Path() / assets_folder / file

target = Path() / path.parents[0] / f"{path.stem}.wav"
print(str(target))