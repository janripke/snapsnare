import os.path
import snapsnare
from pathlib import Path
from snapsnare.system.folderlib import Folder

properties = {
    'current.dir': os.path.abspath(os.getcwd()),
    'package.dir': os.path.dirname(snapsnare.__file__),
    'home.dir': str(Path.home()),
    'app.name': 'snapsnare'
}





# # package_dir =
#
# print(properties['package.dir'])
#
# folder = os.path.join(properties['package.dir'], 'static', '992e5b88-ea97-423b-be99-8603d96e6879')
# results = []
# files = os.listdir(folder)
# for file in files:
#     filename, extension = os.path.splitext(os.path.join(folder, file))
#     if extension == '.mp4':
#         results.append(os.path.join(folder, file))

# print(results)
# files = os.listdir('*.png')
'4c8ec135-1182-4951-8838-7036f245e324'
folder = os.path.join(properties['package.dir'], 'static', '4c8ec135-1182-4951-8838-7036f245e324')
print(os.listdir(folder))

folder = os.path.join(properties['package.dir'], 'static', '88d8e1a3-b41a-406d-a2fd-9ecf67eda146')
image_folder = Folder(folder)
print(image_folder.listdir(filters='.png;.jpg;.gif;.bmp'))

