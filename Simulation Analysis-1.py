#!/usr/bin/env python
# coding: utf-8

# In[258]:


import random
import math
Infinity = 10000000
#random.seed(1234) # set the seed
#random.random
NextFailure=math.ceil (6*random.random())
NextRepair= Infinity
S = 3.0
Slast= 3.0
Clock = 0.0
Tlast= 0.0
Area = 0.0
while S > 0:
    
    b=NextRepair
    NextEvent= Timer()
    if NextEvent == "Failure":
                        
        Failure()
    else:
        Repair()
print (Clock,Area/Clock )


# In[171]:


def Failure(): # function routine for failure event.
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    S = S-1 # number of functional component decreases by 1
    if S == 2:
        # schedule the failure time of the spare component
        NextFailure= Clock + math.ceil (6*random.random())
        # schedule the repair completion
        NextRepair= Clock + 3.5
        
    elif S==1:
        if NextRepair==Infinity:
            NextFailure= Clock + math.ceil (6*random.random())
            NextRepair= Clock + 3.5
        else:
            NextFailure= Clock + math.ceil (6*random.random())
            NextRepair= b
            
            
            
    # update the statistics for average number of functional components,
    Area = Area + Slast * (Clock-Tlast)
    Tlast= Clock
    Slast= S


# In[172]:


def Repair():
    global S
    global Slast
    global Tlast
    global Area
    global NextFailure
    global NextRepair
    S = S + 1
    if S == 2:
        NextRepair= Clock + 3.5
        NextFailure= Clock + math.ceil (6*random.random())
    elif S==1:
        if NextRepair==Infinity:
            NextFailure= Clock + math.ceil (6*random.random())
            NextRepair= Clock + 3.5
        else:
            NextFailure= Clock + math.ceil (6*random.random())
            NextRepair= b
    Area = Area +Slast * (Clock-Tlast)
    Tlast= Clock
    Slast= S


# In[173]:


def Timer(): # Advance the simulation from event to event
    global Clock
    global NextFailure
    global NextRepair
    if NextFailure < NextRepair:
        result = "Failure"
        Clock =NextFailure # advance the simulation clock
        # take the triggering event off the event calendar
        NextFailure= Infinity
        
    else:
        result = "Repair"
        Clock = NextRepair
        NextRepair = Infinity
        
    return result


# In[291]:


import pandas as pd
df=pd.DataFrame()
Yi=[]
for i in range(1,101):
    a="Y"+str(i)
    Yi.append(a)
Si=[]
for i in range(1,101):
    a="S"+str(i)
    Si.append(a)   
Yii=[]
Sii=[]
for i in range(1,101):
    import random
    import math
    Infinity = 10000000
    #random.seed(1234) # set the seed
    #random.random
    NextFailure=math.ceil (6*random.random())
    NextRepair= Infinity
    S = 3.0
    Slast= 3.0
    Clock = 0.0
    Tlast= 0.0
    Area = 0.0
    while S > 0:

        b=NextRepair
        NextEvent= Timer()
        if NextEvent == "Failure":

            Failure()
        else:
            Repair()
    Y=Clock
    S=Area/Clock
    Yii.append(Y)
    Sii.append(S)
Y_df=pd.DataFrame(Yi,Yii)
S_df=pd.DataFrame(Si,Sii) 

Y_df=Y_df.reset_index()
S_df=S_df.reset_index()


# In[301]:


# 95 % Confidence Interval for Expected Time of System Failure

from scipy.stats import sem, t
from scipy import mean
confidence = 0.95
data = Y_df[["index"]]

n = len(data)
m = mean(data)
std_err = sem(data)
h = std_err * t.ppf((1 + confidence) / 2, n - 1)

start = m - h

end = m + h
print("Lower Limit: ",float(start))
print("Upper Limit: ",float(end))


# In[302]:


# 95 % Confidence Interval for Average Number of Functional Components

from scipy.stats import sem, t
from scipy import mean
confidence = 0.95
data = S_df[["index"]]

n = len(data)
m = mean(data)
std_err = sem(data)
h = std_err * t.ppf((1 + confidence) / 2, n - 1)

start = m - h

end = m + h
print("Lower Limit: ",float(start))
print("Upper Limit: ",float(end))

