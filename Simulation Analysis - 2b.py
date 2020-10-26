
# Call Center HW Project 
# Cross-Trained SMP Call Center
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

Queue = Basic_Classes.FIFOQueue()
Agents = Basic_Classes.Resource()
QueueTime = Basic_Classes.DTStat()
Lost = Basic_Classes.DTStat()
Agents.SetUnits(6)

# These lists collect the across-rep data
QT = []
QN = []
DLost = []

TheDTStats.append(QueueTime)
TheDTStats.append(Lost)
TheQueues.append(Queue)
TheResources.append(Agents)

def Arrival():
    Interarrival = RNG.Expon(1.0,1)
    if Clock + Interarrival < 480.0:
        VBASim.Schedule(Calendar, "Arrival", Interarrival, Clock)

    NewCustomer = Basic_Classes.Entity(Clock)
    if RNG.Uniform(0.0,1.0,2) < 0.59:
#   Financial Customer
        if Agents.Busy == Agents.NumberOfUnits:
            if RNG.Uniform(0.0,1.0,5) < 0.06:
                Lost.Record(1)
            else:
                Queue.Add(NewCustomer, Clock)
        else:
            Agents.Seize(1, Clock)
            VBASim.SchedulePlus(Calendar,"EOS",RNG.Erlang(2,1.1*5.0,3), NewCustomer, Clock)
            QueueTime.Record(0.0)
    else:
#   Contact Management Customer
        if Agents.Busy == Agents.NumberOfUnits:
            if RNG.Uniform(0.0,1.0,5) < 0.06:
                Lost.Record(1)
            else:
                Queue.Add(NewCustomer, Clock)
        else:
            Agents.Seize(1, Clock)
            VBASim.SchedulePlus(Calendar,"EOS",RNG.Erlang(3,1.1*5.0,4), NewCustomer, Clock)
            QueueTime.Record(0.0)
    
def EOS(DepartingCustomer):
    if Queue.NumQueue() > 0:
        NextCustomer = Queue.Remove(Clock)
        QueueTime.Record(Clock - NextCustomer.CreateTime)
        if RNG.Uniform(0.0,1.0,2) < 0.59:
            VBASim.SchedulePlus(Calendar,"EOS",RNG.Erlang(2,1.1*5.0,3), NextCustomer, Clock)
        else:
            VBASim.SchedulePlus(Calendar,"EOS",RNG.Erlang(3,1.1*5.0,3), NextCustomer, Clock)
    else:
        Agents.Free(1, Clock)
        


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
        elif NextEvent.EventType == "EOS":
            EOS(NextEvent.WhichObject)    
            

# Collect across-rep data
    QT.append(QueueTime.Mean())
    QN.append(Queue.Mean(Clock))
    DLost.append(Lost.N())


thedata = {'Wait': QT, 'Num': QN, 'Lost': DLost}
mydata = pandas.DataFrame(data=thedata)


print("Means")
print(mydata.mean())
print("+/- 95% CI")
print(1.96*mydata.std()/numpy.sqrt(mydata.count()))
print("Relative error")
print(1.96*mydata.std()/numpy.sqrt(mydata.count())/mydata.mean())
print("Number of reps =", mydata['Wait'].count())
print("Number of agents =", Agents.NumberOfUnits)


print("\nQueue Time F =" , QueueTimeF.Mean(), "\tQueue Time C =", QueueTimeC.Mean())
print("Queue F = ", FQueue.Mean(Clock), "\tQueue C = ", CQueue.Mean(Clock))
print("F Agents = ", FAgents.Mean(Clock), "\tC Agents = ", CAgents.Mean(Clock))
print("Lost =", Lost.N(), "\tClock =", Clock)
    