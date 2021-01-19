from pydub import AudioSegment
import os.path
folder = "/home/jan/workspace/snapsnare/snapsnare/static/b3a62cff-0c58-4514-966a-a4925331d828"

files = os.listdir(folder)
print(files)
for file in files:
    source = os.path.join(folder, file)
    track = AudioSegment.from_file(source, 'm4a')
    path, extension = os.path.splitext(source)
    print(path)
    print(extension)
    track.export("{}.{}".format(path, 'wav'), format='wav')
