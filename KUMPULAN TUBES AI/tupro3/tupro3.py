import numpy as np
import pandas as pd

class Datafuzzy():
    def __init__(self, score, decission):
        self.score = float(score)
        self.decission = decission

# FOLLOWER=========================================
# membership function

def fuzzyFollower(countFol):

    follower = []
    # STABLE GRAPH
    if (0 <= countFol and countFol <=20000):
        scoreFuzzy = 1
        follower.append(Datafuzzy(scoreFuzzy, "NANO"))
      
    # GRAPH DOWN
    elif (20000 < countFol and countFol <= 30000):
        scoreFuzzy = np.absolute((countFol - 20000) / (30000 - 20000))
        follower.append(Datafuzzy("%.2f" % scoreFuzzy, "NANO"))
      
    # MICRO
    # THE GRAPH GOES UP
    if (20000 <= countFol and countFol <= 30000):
        scoreFuzzy = 1 - scoreFuzzy #np.absolute((countFol - 30000) / (30000 - 20000) )
        follower.append(Datafuzzy("%.2f" % scoreFuzzy, "MICRO"))
      
    # STABLE GRAPH
    elif (30000 < countFol and countFol < 55000):
        scoreFuzzy = 1
        follower.append(Datafuzzy(scoreFuzzy, "MICRO"))
      
    # GRAPH DOWN
    elif (55000 <= countFol and countFol <= 75000):
        scoreFuzzy = np.absolute((countFol - 55000) / (75000 - 55000))
        follower.append(Datafuzzy("%.2f" % scoreFuzzy, "MICRO"))

    # MEDIUM
    # THE GRAPH GOES UP
    if (55000 <= countFol and countFol <= 75000):
        scoreFuzzy = 1 - scoreFuzzy
        follower.append(Datafuzzy("%.2f" % scoreFuzzy, "MEDIUM"))
      
  # STABLE GRAPH
    elif (75000 < countFol and countFol <= 80000):
        scoreFuzzy = 1
        follower.append(Datafuzzy(scoreFuzzy, "MEDIUM"))
        
    elif (countFol > 80000):
        scoreFuzzy = np.absolute((countFol - 80000) / (100000 - 80000))
        follower.append(Datafuzzy(scoreFuzzy, "MEDIUM"))
    
    return follower
    
# ENGAGEMENT RATE =========================================
# membership function
def fuzzyEngagement(countEng):

    engagement = []
    # STABLE GRAPH
    if (0 <= countEng and countEng <= 0.3):
        scoreFuzzy = 1
        engagement.append(Datafuzzy(scoreFuzzy, "NANO"))
      
    # GRAPH DOWN
    elif (0.3 < countEng and countEng <= 1.7):
        scoreFuzzy = np.absolute((countEng - 0.31) / (1.7 - 0.31))
        engagement.append(Datafuzzy("%.2f" % scoreFuzzy, "NANO"))
      
    # MICRO
    # THE GRAPH GOES UP
    if (0.3 < countEng and countEng <= 1.7):
        scoreFuzzy =  1 - scoreFuzzy # np.absolute((countEng - 0.3) / (1.7 - 0.3))
        engagement.append(Datafuzzy("%.2f" % scoreFuzzy, "MICRO"))

    # GRAPH DOWN
    elif (1.7 < countEng and countEng <= 5.7):
        scoreFuzzy = np.absolute((countEng - 1.71) / (5.7 - 1.71))
        engagement.append(Datafuzzy("%.2f" % scoreFuzzy, "MICRO"))

    # MEDIUM
    # THE GRAPH GOES UP
    if (1.7 < countEng and countEng <= 5.7):
        scoreFuzzy = 1 - np.absolute((countEng - 1.71) / (5.7 - 1.71))
        engagement.append(Datafuzzy("%.2f" % scoreFuzzy, "MEDIUM"))
      
    # STABLE GRAPH
    elif (5.71 < countEng and countEng <= 10.0):
        scoreFuzzy = 1
        engagement.append(Datafuzzy(scoreFuzzy, "MEDIUM"))
        
    return engagement

# Fuzzy Rules
def fuzzyRules(follower, engagement):
    temp_yes = []
    temp_no = []
    
    # First decision Follower test is Nano
    if (follower[0].decission == "NANO"):
        # Get minimal score fuzzy every decision NO or YES
        temp_yes.append(min(follower[0].score,engagement[0].score))
        
        # if get 2 data fuzzy Engagement
        if (len(engagement) > 1):
            temp_yes.append(min(follower[0].score,engagement[1].score))
            
    # First decision of Follower is Micro or Medium                     
    else:
        if (engagement[0].decission == "NANO"):
            temp_no.append(min(follower[0].score, engagement[0].score))
            
        elif (engagement[0].decission == "MICRO"):
            if (follower[0].decission == "MICRO"):
                temp_yes.append(min(follower[0].score, engagement[0].score))
            else:
                temp_no.append(min(follower[0].score,engagement[0].score))
                
        else:
            temp_yes.append(min(follower[0].score, engagement[0].score))
            
        # if get 2 data fuzzy engagement 
        if (len(engagement) > 1):
            if (engagement[1].decission == "NANO"):
                temp_no.append(min(follower[0].score, engagement[1].score))
                
            elif (engagement[0].decission == "MICRO"):
                if (follower[0].decission == "MICRO"):
                    temp_yes.append(min(follower[0].score, engagement[1].score))
                else:
                    temp_no.append(min(follower[0].score,engagement[1].score))
                    
            else:
                temp_yes.append(min(follower[0].score, engagement[1].score))
                
    # if get 2 data fuzzy Follower                    
    if (len(follower) > 1):
        # Second decision Follower is Nano
        if (follower[1].decission == "NANO"):
            temp_yes.append(min(engagement[0].score,follower[1].score))  
            
            if (len(engagement) > 1):
                temp_yes.append(min(engagement[1].score,follower[1].score))
                
        # Second decision follower is Micro or Medium
        else:
            if (engagement[0].decission == "NANO"):
                temp_no.append(min(follower[1].score, engagement[0].score))
                
            elif (engagement[0].decission == "MICRO"):
                if (follower[1].decission == "MICRO"):
                    temp_yes.append(min(follower[1].score, engagement[0].score))
                else:
                    temp_no.append(min(follower[1].score,engagement[0].score))
                    
            #if get 2 data fuzzy Engagement 
            if (len(engagement) > 1):
                if (engagement[1].decission == "NANO"):
                    temp_no.append(min(follower[1].score, engagement[1].score))
                    
                elif (engagement[1].decission == "MICRO"):
                    if (follower[1].decission == "MICRO"):
                        temp_yes.append(min(follower[1].score, engagement[1].score))
                    else:
                        temp_no.append(min(follower[1].score,engagement[1].score))
    
    return temp_yes, temp_no

# Result
def getResult(resultYes, resultNo):
    yes = 0
    no = 0
    if(not resultYes and not resultNo):
        print("NO and YES is Error")
    else:
        if(resultNo):
            if (len(resultNo) > 1):
                no = max(resultNo)
            else:
                no = float(resultNo[0])

        if(resultYes):
            if(len(resultYes) > 1):
                yes = max(resultYes)
            else:
                yes = float(resultYes[0])
    return yes, no

def finalDecission(yes, no):
    sugeno = ((no * 60) + (yes * 80)) / (no + yes)
    return sugeno

def mainFunction(followerCount, engagementRate):
    follower = fuzzyFollower(followerCount)
    engagement = fuzzyEngagement(engagementRate)
    
    resultYes, resultNo = fuzzyRules(follower, engagement)
    yes, no = getResult(resultYes, resultNo)
    
    return finalDecission(yes, no)

data = pd.read_csv('influencers.csv')
 # MAIN
hasil = []
for i in range (len(data)):
    hasil.append([data.loc[i, 'id'], mainFunction(data.loc[i, 'followerCount'], data.loc[i, 'engagementRate'])])
hasil.sort(key=lambda x:x[1], reverse=True)
print("HASIL")
print(*hasil, sep='\n')

chosen = pd.DataFrame(hasil[:20], columns=['ID', 'Score'])
chosen.to_csv('choosen.csv')