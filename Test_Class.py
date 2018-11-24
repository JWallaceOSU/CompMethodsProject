import numpy as np

class Test:

    def __init__(self,path):
        self.path = path
        self.filedata = None
        self.data = []
        self.stepTime = []
        self.strain = []
        self.stress = []
        self.temp = []
        self.force = []
        self.gap = []
        self.realTime = []
        self.results = None
        self.title = self.path.strip().split('\\')
        self.title = self.title[len(self.title)-1]
        self.steps = []
        self.stepIndices = [0]
        self.units = None
        self.thick = None
        self.width = None
        self.length = None
        self.inputFreq = None
        self.rampRate = None
        self.T1 = None
        self.T2 = None
        self.strainAmp = None
        self.extGap = None
        dimarr = self.title.strip().split('_')
        for dim in dimarr:
            if ".txt" in dim:
                dim = dim.strip(".txt")
            first = dim[0]
            if dim[0] == 't':
                self.thick = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 'w':
                self.width = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 'l':
                self.length = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 'f':
                self.inputFreq = float(dim[1:].strip().replace("p", '.'))
            if dim[0] == 'd':
                self.rampRate = float(dim[1:].strip().replace("p", '.'))
            if dim[0] == 'b':
                self.T1 = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 'e':
                self.T2 = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 's':
                self.strainAmp = float(dim[1:].strip().replace("p",'.'))
            if dim[0] == 'g':
                self.extGap = float(dim[1:].strip().replace("p", '.'))


    def readData(self):
        f1 = open(self.path,'r')
        self.filedata = f1.readlines()
        f1.close()
        i = 0
        for line in self.filedata:
            if "[step]" in line:
                self.steps.append(self.filedata[i+1].strip())
                if self.units is None:
                    self.cols = self.filedata[i+2].strip().split("\t")
                    self.units = self.filedata[i+3].strip().split("\t")
                j = i + 3
                while True:
                    j+=1
                    if "[step]" not in self.filedata[j].strip() and len(self.filedata[j].strip()) > 0:
                        lineData = self.filedata[j].split("\t")
                        chunk = []
                        for point in lineData:
                            chunk.append(float(point.strip("\n")))
                        self.data.append(chunk)

                    else:
                        break
                self.stepIndices.append(len(self.data))




            i+=1


    def sortData(self):
        if len(self.data) != 0:
            i = 0
            for name in self.cols:
                if name.lower() == "step time":
                    stepTimeCol = i
                if name.lower() == "stress":
                    stressCol = i
                if name.lower() == "strain":
                    strainCol = i
                if name.lower() == "temperature":
                    tempCol = i
                if name.lower() == "force":
                    forceCol = i
                if name.lower() == "gap":
                    gapCol = i
                if name.lower() == "time":
                    realTimeCol = i
                i += 1
            for row in self.data:
                try:
                    self.stepTime.append(row[stepTimeCol])
                    self.stress.append(row[stressCol])
                    self.strain.append(row[strainCol])
                    self.temp.append(row[tempCol])
                    self.force.append(row[forceCol])
                    self.gap.append(row[gapCol])
                    self.realTime.append(row[realTimeCol])

                except:
                    print("Error in Data Collection")
                    raise











