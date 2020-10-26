
import SimFunctions
import SimRNG 
import SimClasses
import pandas
import numpy as np

ZSimRNG = SimRNG.InitializeRNSeed()

Queue = SimClasses.FIFOQueue()
Wait = SimClasses.DTStat()
Server = SimClasses.Resource()
Calendar = SimClasses.EventCalendar()

TheCTStats = []
TheDTStats = []
TheQueues = []
TheResources = []

TheDTStats.append(Wait)
TheQueues.append(Queue)
TheResources.append(Server)

Server.SetUnits (1) 
MeanTBA = 1.0
MeanST = 0.8
Phases = 3
RunLength = 55000.0
WarmUp = 5000.0

AllWaitMean = []
AllQueueMean = []
AllQueueNum = []
AllServerMean = []
print ("Rep", "Average Wait", "Average Number in Queue", "Number Remaining in Queue", "Server Utilization")

def Arrival():
    SimFunctions.Schedule(Calendar,"Arrival",SimRNG.Expon(MeanTBA, 1))
    Customer = SimClasses.Entity()
    Queue.Add(Customer)
    
    if Server.Busy == 0:
        Server.Seize(1)
        SimFunctions.Schedule(Calendar,"EndOfService",SimRNG.Erlang(Phases,MeanST,2))

def EndOfService():
    DepartingCustomer = Queue.Remove()
    Wait.Record(SimClasses.Clock - DepartingCustomer.CreateTime)
    if Queue.NumQueue() > 0:
        SimFunctions.Schedule(Calendar,"EndOfService",SimRNG.Erlang(Phases,MeanST,2))
    else:
        Server.Free(1)

for reps in range(0,10,1):

    SimFunctions.SimFunctionsInit(Calendar,TheQueues,TheCTStats,TheDTStats,TheResources)
    SimFunctions.Schedule(Calendar,"Arrival",SimRNG.Expon(MeanTBA, 1))
    SimFunctions.Schedule(Calendar,"EndSimulation",RunLength)
    SimFunctions.Schedule(Calendar,"ClearIt",WarmUp)
    
    NextEvent = Calendar.Remove()
    SimClasses.Clock = NextEvent.EventTime
    if NextEvent.EventType == "Arrival":
        Arrival()
    elif NextEvent.EventType == "EndOfService":
        EndOfService() 
    elif NextEvent.EventType == "ClearIt":
        SimFunctions.ClearStats(TheCTStats,TheDTStats)
    
    while NextEvent.EventType != "EndSimulation":
        NextEvent = Calendar.Remove()
        SimClasses.Clock = NextEvent.EventTime
        if NextEvent.EventType == "Arrival":
            Arrival()
        elif NextEvent.EventType == "EndOfService":
            EndOfService()
        elif NextEvent.EventType == "ClearIt":
            SimFunctions.ClearStats(TheCTStats,TheDTStats)

    
    AllWaitMean.append(Wait.Mean())
    AllQueueMean.append(Queue.Mean())
    AllQueueNum.append(Queue.NumQueue())
    AllServerMean.append(Server.Mean())
    print (reps+1, Wait.Mean(), Queue.Mean(), Queue.NumQueue(), Server.Mean())

output = {"AllWaitMean" : AllWaitMean, "AllQueueMean": AllQueueMean, "AllQueueNum" : AllQueueNum, "AllServerMean": AllServerMean}
output = pandas.DataFrame(output)
output.to_csv("MG1_output.csv", sep=",")

# some optional code that shows how to save all the data
# and do analysis with the pandas module
AllWaitMean = pandas.DataFrame(AllWaitMean)
AllQueueMean = pandas.DataFrame(AllQueueMean)
AllQueueNum = pandas.DataFrame(AllQueueNum)
AllServerMean = pandas.DataFrame(AllServerMean)

print (AllWaitMean.mean()[0])
print (AllWaitMean.std())
print (AllQueueMean.mean())
print (AllQueueMean.std())
print (AllQueueNum.mean())
print (AllQueueNum.std())
print (AllServerMean.mean())
print (AllServerMean.std())