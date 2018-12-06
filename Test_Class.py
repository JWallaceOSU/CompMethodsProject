import numpy as np
class Result:
    def __init__(self):
        self.modulus = None
        self.tandelta = None
        self.freqreal = None
        self.temp = None
        self.rtime = None
        self.stime = None
        self.delta = None
        self.storage = None
        self.loss = None
        self.sigAmp = None
        self.epsAmp = None
        self.rawData = None
class Data:
    def __init__(self):
        self.space = None
        self.data = []
        self.stepTime = []
        self.strain = []
        self.stress = []
        self.temp = []
        self.force = []
        self.gap = []
        self.realTime = []
        self.stepStorage = []
        self.stepLoss = []
        self.cols = None
        self.steps = []
        self.stepIndices = [0]
    def sortData(self):

        if len(self.data) != 0:
            i = 0
            # Find which chunk indices go with which data points
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
            # Put each point in the chunk into its correct array
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
        # Convert the lists to numpy arrays (necessary for matplotlib)
        self.stepTime = np.asarray(self.stepTime,dtype=np.float32)
        self.stress = np.asarray(self.stress,dtype=np.float32)
        self.strain = np.asarray(self.strain,dtype=np.float32)
        self.temp = np.asarray(self.temp,dtype=np.float32)
        self.force = np.asarray(self.force,np.float32)
        self.gap = np.asarray(self.gap,np.float32)
        self.realTime = np.asarray(self.realTime,np.float32)
class Test:

    def __init__(self,path):
        # Initialize all class variables
        self.path = path
        self.data = None
        self.stepData = []
        self.stepResult = []
        self.storagePts = []
        self.lossPts = []
        self.tandeltaPts = []
        self.tempPts = []
        self.fileData = None
        self.results = None
        self.title = self.path.strip().split('\\')
        self.title = self.title[len(self.title)-1]
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
        # Strip file name for useful info
        dimarr = self.title.strip().split('_')
        for dim in dimarr:
            if ".txt" in dim:
                dim = dim.strip(".txt")
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
    # Read data
    def readData(self):
        # Open file to get lines
        f1 = open(self.path,'r')
        self.fileData = f1.readlines()
        f1.close()
        self.data = Data()
        # Set counter to 0
        i = 0
        for line in self.fileData:
            # "[step]" is our key to finding when a data stream begins
            if "[step]" in line:
                # Add the step to the step list
                self.data.steps.append(self.fileData[i + 1].strip())
                if self.units is None:
                    # Get units and column names
                    self.data.cols = self.fileData[i + 2].strip().split("\t")
                    self.units = self.fileData[i + 3].strip().split("\t")
                # We create a new index j to collect all of the data in the step
                j = i + 3
                stepData = Data()
                stepData.cols = self.data.cols
                while True:
                    j+=1
                    # Since the data for the step ends at the next [step] marker or empty line, we check
                    # to see that the line is not an empty line or step indicator
                    if "[step]" not in self.fileData[j].strip() and len(self.fileData[j].strip()) > 0:
                        # Split the line data by tabs, since it is tab-delimited
                        lineData = self.fileData[j].split("\t")
                        # We are going to call all of the data in each line a chunk and sort it later
                        chunk = []
                        # For each data point in the line we add it to the chunk
                        for point in lineData:
                            chunk.append(float(point.strip()))
                        # We add the chunk to the data stream
                        self.data.data.append(chunk)
                        stepData.data.append(chunk)
                    else:
                        break
                self.data.stepIndices.append(len(self.data.data))
                stepData.sortData()
                self.stepData.append(stepData)

            i+=1
        self.data.sortData()
    def processStepData(self):
        for stepData in self.stepData:
            stepResult = self.processData(stepData,1)
            self.storagePts.append(stepResult.storage)
            self.lossPts.append(stepResult.loss)
            self.tempPts.append(stepResult.temp)
            self.tandeltaPts.append(stepResult.tandelta)
            self.stepResult.append(stepResult)







    def processData(self, data, frqTrg,s=1000):
        def nextPow2(x):
            y = np.ceil(np.log2(x))
            return y
        try:
            N = len(data.realTime)
            dt = np.mean(np.diff(data.realTime))
            fs = 1/dt
            shift0 = np.pi
            eps0 = np.mean(data.strain)
            sig0 = np.mean(data.stress)
            eps = data.strain - eps0
            sig = data.stress - sig0
            if data.space is None:
                n = 2**(nextPow2(N))
            else:
                n = (2**nextPow2(N))+data.space
            EPS = np.fft.fft(eps,n)/N
            SIG = np.fft.fft(sig,n)/N
            fspace = fs*np.linspace(0,1,n)
            epsAmp = np.abs(EPS)
            sigAmp = np.abs(SIG)
            ind = int((np.mean(np.where(abs(frqTrg-fspace)<.05*frqTrg))))
            shift = SIG[ind]/EPS[ind]
            shift = np.angle(shift,False)
            modulus1 = np.sum(sigAmp)/np.sum(epsAmp)
            #modulus1 = sigAmp[ind]/epsAmp[ind]
            result = Result()
            result.fspace = fspace
            result.temp = np.mean(data.temp)
            result.rtime = np.mean(data.realTime)
            result.stime = np.mean(data.stepTime)
            result.delta = shift
            result.tandelta = np.tan(shift)
            result.freqreal = fspace[ind]
            result.modulus = modulus1
            result.storage = (modulus1**2)/(1+result.tandelta**2)
            result.loss = result.storage*result.tandelta
            result.rawData = data
            result.sigAmp = sigAmp
            result.epsAmp = epsAmp
            return result

        except:
            print("failure in data processing, oops!")
            raise






