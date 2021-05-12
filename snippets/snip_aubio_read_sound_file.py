import aubio

samplerate = 0 # use original source samplerate
hop_size = 256  # number of frames to read in one block
src = aubio.source("pinda.wav", samplerate, hop_size)

total_frames = 0
while True:
    samples, read = src()  # read hop_size new samples from source
    total_frames += read  # increment total number of frames
    if read < hop_size:  # end of file reached
        break

print(f"read {total_frames} frames at {src.samplerate}Hz from {src.uri}")
