import sys
from aubio import tempo, source

fft_size = 512
hop_size = fft_size // 2

filename = "pinda.wav"

samplerate = 0

s = source(filename, samplerate, hop_size)
samplerate = s.samplerate
o = tempo("default", fft_size, hop_size, samplerate)

# tempo detection delay, in samples
# default to 4 blocks delay to catch up with
delay = 4. * hop_size

# list of beats, in samples
beats = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    is_beat = o(samples)
    if is_beat:
        this_beat = int(total_frames - delay + is_beat[0] * hop_size)
        print("%f" % (this_beat / float(samplerate)))
        beats.append(this_beat)
    total_frames += read
    if read < hop_size: break
#print len(beats)