import wave , getopt , sys
from struct import  *


def cook(wavName):
    global sound , numberOfFrames , parameter , format , mask
    sound = wave.open(wavName, "r")
    parameter = sound.getparams()
    numberOfChannels = sound.getnchannels()
    numberOfFrames = sound.getnframes()  # to how many pieces audio file is splat
    sampleWidth = sound.getsampwidth()
    numberOfSamples = numberOfFrames * numberOfChannels

    if (sampleWidth == 1):
        format = "{}B".format(numberOfSamples)  # changes into string

        mask = (1 << 8) - (1 << 2)

    elif (sampleWidth == 2):
        format = "{}h".format(numberOfSamples)  # format is to tell me how i ll unpack audio file
        mask = (1 << 15) - (1 << 2)
    else:
        raise ValueError("audio width is too high")


def hide(wavName, text, resultFile):
    cook(wavName)
    maxByteToHide = (numberOfFrames * 2) // 8  # max bytes to hide

    rawData = list(unpack(format, sound.readframes(numberOfFrames)))  # frames in binary
    sound.close()
    textRawData = memoryview(open(text, "rb").read())  ## read text into tytes
    print(len(textRawData))

    firstVaues = []
    indexOfText = 0
    buferLen = 0
    bufer = 0
    soundindex = 0

    while (indexOfText < len(textRawData)):  # incrementing lists index of the text

        while (buferLen < 2):  # every time bufer len drops below 2 move to the next letter
            bufer = textRawData[indexOfText]
            indexOfText += 1
            buferLen += 8

        currentData = bufer % (1 << 2)  # bytes from text file extracted backwards for each letter
        bufer >>= 2
        buferLen -= 2

        currentSample = rawData[soundindex]
        soundindex += 1

        sign = 1
        if (currentSample < 0):
            currentSample = - currentSample
            sign = -1

        changedSample = sign * (currentSample & mask) | currentData

        tempValue = pack(format[-1], changedSample)
        firstVaues.append(tempValue)

    while (indexOfText < len(rawData)):
        tempValue = pack(format[-1], rawData[indexOfText])
        firstVaues.append(tempValue)
        indexOfText += 1

    resultAudio = wave.open(resultFile, "w")
    resultAudio.setparams(parameter)
    resultAudio.writeframesraw(b"".join(firstVaues))
    resultAudio.close()
    print("data hidden")


def unhide(wavName,outputFile, recoverByte):
    cook(wavName)
    rawSoundData = list(unpack(format, sound.readframes(numberOfFrames)))
    mask = (1 << 2) - 1
    output = open(outputFile, "wb+")
    sound.close()

    data = []
    buffer = 0
    index = 0
    bufferLen = 0

    while (recoverByte > 0):

        buffer += (rawSoundData[index] & mask) << bufferLen
        bufferLen += 2
        index += 1

        while (bufferLen >= 8 and recoverByte > 0):
            bufferLen -= 8
            data += pack('1B', buffer)
            buffer >>= 8
            recoverByte -= 1

    output.write(bytes(data))
    output.close()
    print("Data recovered")



print("enter h to set application to hide mode  and  u to set it to unhide mode")
flag = input()
if flag=="h":
    print("1.audio file  2.text file 3.result audio file")
    try:
        x , y , z = input().split(" ")
        hide(x, y, z)
    except: print("u did something wrong try again")
elif flag=="u":
    print("1.audio file  2.text file 3.number of bytes to recover")
    try:
        x , y , z = input().split(" ")
        unhide(x, y, int(z))
    except: print(" you did something wrong")









