import wave ,struct
from struct import  *

class Steg():


    def __init__(self,wavName):
        self.sound = wave.open(wavName,"r")
        self.parameter = self.sound.getparams()
        self.numberOfChannels = self.sound.getnchannels()
        self.numberOfFrames = self.sound.getnframes()  # to how many pieces audio file is splat
        self.sampleWidth = self.sound.getsampwidth()
        self.numberOfSamples = self.numberOfFrames*self.numberOfChannels

        if(self.sampleWidth==1):
            self.fmt = "{}B".format(self.numberOfSamples)  # changes into string

            self.mask = (1<<8) - (1<<2)

        elif(self.sampleWidth==2):
            self.fmt = "{}h".format(self.numberOfSamples)   # fmt is to tell me how i ll unpack audio file
            self.mask = (1<<15) - (1<<2)
        else:
            raise ValueError("audio width is too high")




    def hide(self,text,resultFile):
        self.maxByteToHide = (self.numberOfFrames*2)//8   # max bytes to hide
        # print(self.sound.readframes(self.numberOfFrames))
        self.rawData  = list(unpack(self.fmt,self.sound.readframes(self.numberOfFrames)))   # frames in binary
        self.sound.close()
        self.textRawData = memoryview(open(text,"rb").read())  ## read text into tytes
        print(len(self.textRawData))

        firstVaues = []
        indexOfText = 0
        buferLen = 0
        bufer = 0
        soundindex =0

        while (indexOfText<len(self.textRawData)): # incrementing lists index of the text


           while(buferLen<2):  # every time bufer len drops below 2 move to the next letter
               bufer = self.textRawData[indexOfText]
               indexOfText +=1
               buferLen+=8

           self.currentData = bufer % (1 << 2)
           bufer >>= 2
           buferLen -= 2

           self.currentSample = self.rawData[soundindex]
           soundindex += 1

           sign = 1
           if (self.currentSample < 0):
               self.currentSample = - self.currentSample
               sign = -1

           changedSample = sign * (self.currentSample & self.mask) | self.currentData

           tempValue = pack(self.fmt[-1], changedSample)
           firstVaues.append(tempValue)







        while(indexOfText<len(self.rawData)):
            tempValue = pack(self.fmt[-1],self.rawData[indexOfText])
            firstVaues.append(tempValue)
            indexOfText+=1

        resultAudio = wave.open(resultFile,"w")
        resultAudio.setparams(self.parameter)
        resultAudio.writeframesraw(b"".join(firstVaues))
        resultAudio.close()
        print("data hidden")















s = Steg("muz1.wav")
s.hide("data.txt","f1.wav")




