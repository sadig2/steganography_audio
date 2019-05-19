import os
import sys
import wave
import getopt
import math
from  struct import *

def dopenfile(s,f):
    sound = wave.open(s,"r")
    params = sound.getparams()
    numchannnel = sound.getnchannels()
    samplewtih = sound.getsampwidth()
    nframes = sound.getnframes()
    nsamples = nframes*numchannnel
    filesize = os.stat(f).st_size
    smallest_byte = -(1 << 15)
    mask = (1 << 15) - (1 << 2)



    lsb = 1

    if(samplewtih==2):
        fmt = "{}h".format(nsamples)
        maxByte = (lsb*nsamples) // 8

    if filesize>maxByte:
        raise ValueError("input file is too large")

    print("Using {} B out of {} B".format(filesize, maxByte))
    raw_data = list(unpack(fmt, sound.readframes(nframes)))  # unpacks to real numbers fmt
    sound.close()
    input_data = memoryview(open(f, "rb").read())
    inp = open(f,"rb").read()

    #####################################################################################
    data_index = 0
    sound_index = 0

    # values will hold the altered sound data
    values = []
    buffer = 0
    buffer_length = 0
    done = False

    while (not done):
        while (buffer_length < 2 and data_index // 8 < len(input_data)):
            # If we don't have enough data in the buffer, add the
            # rest of the next byte from the file to it.
            buffer += (input_data[data_index // 8] >> (data_index % 8)) << buffer_length
            bits_added = 8 - (data_index % 8)
            buffer_length += bits_added
            data_index += bits_added


        # Retrieve the next 2 bits from the buffer for use later
        current_data = buffer % (1 << 2)

        buffer >>= 2
        buffer_length -= 2

        while (sound_index < len(raw_data) and raw_data[sound_index] == smallest_byte):
            # If the next sample from the sound file is the smallest possible
            # value, we skip it. Changing the LSB of such a value could cause
            # an overflow and drastically change the sample in the output.
            print("i am here")
            values.append(pack(fmt[-1], raw_data[sound_index]))
            sound_index += 1

        if (sound_index < len(raw_data)):
            current_sample = raw_data[sound_index]
            sound_index += 1

            sign = 1
            if (current_sample < 0):
                # We alter the LSBs of the absolute value of the sample to
                # avoid problems with two's complement. This also avoids
                # changing a sample to the smallest possible value, which we
                # would skip when attempting to recover data.
                current_sample = -current_sample
                sign = -1

            # Bitwise AND with mask turns the 2 least significant bits
            # of current_sample to zero. Bitwise OR with current_data replaces
            # these least significant bits with the next 2 bits of data.
            altered_sample = sign * ((current_sample & mask) | current_data)

            values.append(pack(fmt[-1], altered_sample))

        if (data_index // 8 >= len(input_data) and buffer_length <= 0):
            done = True

    while (sound_index < len(raw_data)):
        # At this point, there's no more data to hide. So we append the rest of
        # the samples from the original sound file.
        values.append(pack(fmt[-1], raw_data[sound_index]))
        sound_index += 1



try:
    opts , args = getopt.getopt(sys.argv[1:],'s:f:')

except:
        print("no file assigned")

for opt ,arg  in opts:
    if opt in "-s":
        soundfile = arg
    elif opt in "-f":
      filename = arg

try:
    dopenfile(soundfile,filename)
except:
    print("no such file")



