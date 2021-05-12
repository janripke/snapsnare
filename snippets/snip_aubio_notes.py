from aubio import source, notes, midi2note

downsample = 1
hop_size = 256 // downsample
samplerate = 0

s = source("pinda.wav", samplerate, hop_size)
samplerate = s.samplerate


win_s = 512 // downsample  # fft size
print(f"{samplerate=}")
print(f"{win_s=}")
print(f"{hop_size=}")

notes_ = notes("default", win_s, hop_size, samplerate)

print("%8s" % "time","[ start","vel","last ]")
total_frames = 0
while True:
    samples, read = s()
    new_note = notes_(samples)
    if (new_note[0] != 0):
        note_str = ' '.join(["%.2f" % i for i in new_note])
        print("%.6f" % (total_frames/float(samplerate)), note_str, new_note)
        print("%.6f" % (total_frames/float(samplerate)),new_note[0], midi2note(int(new_note[1])))
        # print(new_note)


    total_frames += read
    if read < hop_size:
        break
