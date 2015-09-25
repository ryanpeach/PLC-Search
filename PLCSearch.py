import csv
import operator

class Graph:
    def __init__(self, BitStart):
        self.G = {BitStart: []}
        self.WorkingMemory = [BitStart]
        self.Crawlers = []

    def add(self, BitA, BitB):
        if BitB not in self.G[BitA]:
            self.G[BitA].append(BitB)
        if BitB not in self.G:
            self.G[BitB] = []
            self.WorkingMemory.append(BitB)

    def pop(self):
        return self.WorkingMemory.pop(0)

    def find_route(self,Start,Finish):
        global Successes
        Successes = 0
        newCrawler = Crawler(Start,Finish,self) #fix this [], make default
        self.Crawlers = [newCrawler]

        done = False
        successful = []
        while not done:
            done = True
            step = self.Crawlers[:]
            for c in step:
                if not c.end():
                    c.run_one()
                    done = False
                else:
                    if c.SUCCESS and c.P not in successful:
                        successful.append(c.P)
                    

        return successful

    def __str__(self):
        #Sort Bits
        gList = self.G.items()
        bits = []
        for b in gList:
            bits.append(b[0])
        list.sort(bits)

        #Create sorted string
        out = ''
        for i in bits:
            if len(self.G[i])>0 and not self.G[i] == [i]:
                out += str(i) + ': ' + str(self.G[i]) + '\n'
        return out

    def __repr__(self):
        return self.__str__()

##    def find_y(self,Start):
##        global Successes
##        Successes = 0
##        newCrawler = Crawler(Start, self, Crawler.FIND_Y)
##        self.Crawlers = [newCrawler]
##        newCrawler.run()
##        return self.Crawlers

    def addCrawler(self, newCrawler):
        self.Crawlers.append(newCrawler)

class Crawler:

        def __init__(self, Bit, END, Graph, Memory = []):
            if Memory == []:
                Memory = [Bit]
            self.P = Memory
            self.D = len(Memory)
            self.B = Bit
            self.G = Graph
            self.FINISH = END
            self.SUCCESS = False

        def copy(self):
            newCrawler = Crawler(self.B[:],self.FINISH[:],self.G,self.P[:])
            self.G.addCrawler(newCrawler)
            return newCrawler

        def __cmp__(self,CrawlerB):
            if self.D == CrawlerB.D:
                return 0
            elif self.D < CrawlerB.D:
                return self.D-CrawlerB.D
            elif self.D > CrawlerB.D:
                return CrawlerB.D-self.D

        def move(self, newBit):
            self.P.append(newBit)
            self.B = newBit
            self.D += 1
            self.test()


##        def run(self):
##            while not self.end():
##                self.run_one()
##            return self.SUCCESS
        
##        def run_one(self):
##            copy = False
##            nextBits = self.G.G[self.B]
##            cP = (self.B[:],self.FINISH,self.G,self.P[:])
##            for bit in nextBits:
##                if bit not in self.P:
##                    if copy:
##                        duplicate = Crawler(cP[0],cP[1],cP[2],cP[3])
##                        self.G.addCrawler(duplicate)
##                        duplicate.move(bit)
##                        if duplicate.SUCCESS:
##                            break
##                    else:
##                        self.move(bit)
##                        copy = True
##                        if self.SUCCESS:
##                            break

        def run_one(self):
            nextBits = self.G.G[self.B]
            for i in range(len(nextBits)):
                bit = nextBits[i]
                if bit not in self.P:
                    if i == len(nextBits)-1: #on last bit
                        self.move(bit)
                        if self.SUCCESS:
                            break
                    else:
                        duplicate = self.copy()
                        duplicate.move(bit)
                        if duplicate.SUCCESS: #duplicate.run() returns success, run that and break if true
                            break

        def test(self):
            global Successes
            if self.B == self.FINISH:
                self.SUCCESS = True
                Successes += 1
            return self.SUCCESS

        def end(self):
            global Successes, SuccessN, TerminationN
            if Successes >= SuccessN or self.D >= TerminationN:
                return True
            if not self.SUCCESS:
		#Check if this is the last bit availible without retracing
                paths = []
                nextBits = self.G.G[self.B]
                for bit in nextBits:
                    if bit not in self.P:
                        paths.append(bit)
                if len(paths)==0:
                    return True
                else:
                    return False
            else:
                return True

class Reader:
    
    OUT = ["OUT","SET","RST"]
    LD = "LD"
    
    def __init__(self, Start, Finish, Ladder):
        self.G = Graph(Start)
        self.START = Start
        self.END = Finish
        self.L = Ladder
        self.Finish = False
        self.N = 0

    def search_and_add(self, Bit):
        global SuccessN
        save = False
        out = False
        for rung in self.L:
            if self.LD in rung[0] and not rung[1] == Bit:
                if out:
                    save = False
                    out = False
            elif rung[0] not in self.OUT and rung[1] == Bit:
                save = True
            elif rung[0] in self.OUT:
                if save:
                    self.G.add(Bit,rung[1])
                    if rung[1] == self.END:
                        self.N += 1
                        if self.N >= SuccessN:
                            self.Finish = True
                            break
                out = True

    def run(self):
        while not self.Finish and not len(self.G.WorkingMemory)==0:
            pop = self.G.pop()
            self.search_and_add(pop)
        print "Done Reading..."
        return self.G

def qYN(query):
    while True:
        try:
            user_in = raw_input(query + " (Y/N): ")
            if user_in in ("Y","y","Yes","YES","yes"):
                return True
            if user_in in ("N","n","No","NO","no"):
                return False
        except:
            print "Please enter a valid response (Y/N, y/n)..."

if __name__ == '__main__':
    Ladder = []
    Path = raw_input("Please enter the full path (with double \"\\\\\"): ")

    f = open(Path, 'rb')
    csv_f = csv.reader(f,delimiter=',')

    for row in csv_f:
        Ladder.append(row)

    Continue = True
    while Continue:
        #Query
        try:
            tryagain = True
            while tryagain:
                Start = raw_input("Which Bit is your Input: ")
                Finish = raw_input("Which Bit is your Output: ")
                TerminationN = int(raw_input("How far is the max you would care to travel (# of bits): "))
                SuccessN = int(raw_input("How many outputs would you like to receive: "))
                tryagain = False
        except:
            print "Please try again..."
            tryagain = True
            
        #Run the Reader
        graph = Reader(Start,Finish,Ladder).run()
        #print graph
        
        Routes = graph.find_route(Start,Finish)
        Index = {Start: 0}
        print "\n"
        for route in Routes:
            print route
            print "\n"
            
            for bit in route:
                if bit in Index:
                    Index[bit] += 1
                else:
                    Index[bit] = 1


        sorted_Index = sorted(Index.items(), key=operator.itemgetter(1))
        for i in sorted_Index:
            print i

        Continue = qYN("Would you like to run another search?")

    try:
        k=input("Press enter to exit...")
    except:
        pass
