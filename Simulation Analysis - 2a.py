
# Call Center HW Project 
# Current SMP Call Center
# Import needed modules
import VBASimR3 as VBASim
import RNG
import Basic_ClassesR2 as Basic_Classes
import pandas
import numpy

#myfile = open('Callcenter.txt', 'w')
#myfile.write("Call Center Simulation Results")

# Initialize RNG and Event Calendar
ZRNG = RNG.InitializeRNSeed()
Calendar = Basic_Classes.EventCalendar()

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

FQueue = Basic_Classes.FIFOQueue()
CQueue = Basic_Classes.FIFOQueue()
FAgents = Basic_Classes.Resource()
CAgents = Basic_Classes.Resource()
QueueTimeF = Basic_Classes.DTStat()
QueueTimeC = Basic_Classes.DTStat()
Lost = Basic_Classes.DTStat()
FAgents.SetUnits(4)
CAgents.SetUnits(3)

# These lists collect the across-rep data
QTF = []
QTC = []
QNF = []
QNC = []
DLost = []

TheDTStats.append(QueueTimeF)
TheDTStats.append(QueueTimeC)
TheDTStats.append(Lost)
TheQueues.append(FQueue)
TheQueues.append(CQueue)
TheResources.append(FAgents)
TheResources.append(CAgents)

def Arrival():
    Interarrival = RNG.Expon(1.0,1)
    if Clock + Interarrival < 480.0:
        VBASim.Schedule(Calendar, "Arrival", Interarrival, Clock)

    NewCustomer = Basic_Classes.Entity(Clock)
    if RNG.Uniform(0.0,1.0,2) < 0.59:
#   Financial Customer
        if FAgents.Busy == FAgents.NumberOfUnits:
            if RNG.Uniform(0.0,1.0,5) < 0.06:
                Lost.Record(1)
            else:
                FQueue.Add(NewCustomer, Clock)
        else:
            FAgents.Seize(1, Clock)
            VBASim.SchedulePlus(Calendar,"EOSF",RNG.Erlang(2,5.0,3), NewCustomer, Clock)
            QueueTimeF.Record(0.0)
    else:
#   Contact Management Customer
        if CAgents.Busy == CAgents.NumberOfUnits:
            if RNG.Uniform(0.0,1.0,5) < 0.06:
                Lost.Record(1)
            else:
                CQueue.Add(NewCustomer, Clock)
        else:
            CAgents.Seize(1, Clock)
            VBASim.SchedulePlus(Calendar,"EOSC",RNG.Erlang(3,5.0,4), NewCustomer, Clock)
            QueueTimeC.Record(0.0)
    
def EOSF(DepartingCustomer):
    if FQueue.NumQueue() > 0:
        NextCustomer = FQueue.Remove(Clock)
        QueueTimeF.Record(Clock - NextCustomer.CreateTime)
        VBASim.SchedulePlus(Calendar,"EOSF",RNG.Erlang(2,5.0,3), NextCustomer, Clock)
    else:
        FAgents.Free(1, Clock)
        

def EOSC(DepartingCustomer):
    if CQueue.NumQueue() > 0:
        NextCustomer = CQueue.Remove(Clock)
        QueueTimeC.Record(Clock - NextCustomer.CreateTime)       
        VBASim.SchedulePlus(Calendar,"EOSC",RNG.Erlang(3,5.0,4), NextCustomer, Clock)
    else:
        CAgents.Free(1, Clock)

# main program starts here
for Reps in range(0,500,1):
    Clock = 0.0
    VBASim.VBASimInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources, Clock)
    VBASim.Schedule(Calendar, "Arrival", RNG.Expon(1.0, 1), Clock)

    
    while Calendar.N() != 0:
        NextEvent = Calendar.Remove()
        Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "EOSF":
            EOSF(NextEvent.WhichObject)    
        elif NextEvent.EventType == "EOSC":
            EOSC(NextEvent.WhichObject)
            

# Collect across-rep data
    QTF.append(QueueTimeF.Mean())
    QTC.append(QueueTimeC.Mean())
    QNF.append(FQueue.Mean(Clock))
    QNC.append(CQueue.Mean(Clock))
    DLost.append(Lost.N())


thedata = {'FWait': QTF, 'CWait': QTC, 'FNum': QNF, 'CNum': QNC, 'Lost': DLost}
mydata = pandas.DataFrame(data=thedata)


print("Means")
print(mydata.mean())
print("+/- 95% CI")
print(1.96*mydata.std()/numpy.sqrt(mydata.count()))
print("Relative error")
print(1.96*mydata.std()/numpy.sqrt(mydata.count())/mydata.mean())
print("Number of reps =", mydata['FWait'].count())


print("\nQueue Time F =" , QueueTimeF.Mean(), "\tQueue Time C =", QueueTimeC.Mean())
print("Queue F = ", FQueue.Mean(Clock), "\tQueue C = ", CQueue.Mean(Clock))
print("F Agents = ", FAgents.Mean(Clock), "\tC Agents = ", CAgents.Mean(Clock))
print("Lost =", Lost.N(), "\tClock =", Clock)
    