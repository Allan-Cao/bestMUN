import asyncio
import time
import os
import numpy as np
from tinyDB import TinyDB, Query
#import matplotlib.pyplot as plt
db = TinyDB('delegateDatabase.json') # might want to upgrade to sql in the future

flagFolder = "resources/flags" # may need to change
customFlags = "resouces/customFlags" # may need to change
statuses = {0: "Absent",1: "Present",2: "Present & Voting", 3: "Other"}
class delegate():
    def __init__(self, name, delegation, flagName, spokenTime, status):
        self.name = name # delegate name
        self.delegation = delegation # country delegate_names
        self.present = 0 # 0,1,2 absent, present, present and voting
        self.flagName = flagName # standard 4 letter country name
        self.spokenTime = spokenTime # delegate speaking time
        self.status = status # maps to the statuses
        db.insert({'name': name, 'delegation': delegation, 'present': 0, 'flagName': flagName, 'spokenTime': spokenTime, 'status': status})
    def findFlag(self, flagName):
        if os.path.isfile(flagFolder+flagName):
            return(flagFolder + flagName)
        else:
            if os.path.isfile(customFlags+flagName):
                return(customFlags + flagName)
            else:
                raise ValueError("Flag not found")

class motion():
    def __init__(self, title, sessionTime, speakingTime, delegate):
        self.title, self.sessionTime, self.speakingTime = title, sessionTime, speakingTime
        self.motioning_delegate = delegate
        self.clock = time.time()
        self.speak_last = False
    def speech(self, delegate):
        print(delegate,"you have the floor for",self.speakingTime,"seconds.")
        time.sleep(int(self.speakingTime)-10)
        print("You have 10 seconds left.")
        time.sleep(10)
        print("Thank you delegate.")
    def first_last_speech(self):
        fl = input("Would the delegate of",self.motioning_delegate,"like to speak first or last?")
        if fl.lower == 'first':
            self.speech(self.motioning_delegate)
        else: self.speak_last = True

class committeeSession():
    def __init__(self,topics, committeeLength, delegate_names): # topic (1,2,3), total time, delegates in committee
        self.committeeLength, self.topics, self.delegate_names= committeeLength, topics, delegate_names
        self.clock = time.time()
    def rollcall(self):
        self.delegates = [delegate(delegate_name[0], delegate_name[1], int(input("Voting Status of %d:"%(delegate_name[1]))), delegate_name[2]) for delegate_name in self.delegatenames]
        self.quorum = (len([t for t in delegates if t.present != 0])//2)+1
        print("Delegates Present:")
        [print(dele.delegation,'\n') for dele in self.delegates if dele.present != 0]
        print("Quorum is set to",self.quorum)
    def setTopic(self):
        if len(self.topics) == 1: self.topic = self.topics
        else:
            topic_order = [int(i) for i in input("Working topic order: ").split(',')]
            self.topic = topic_order[0]
        print("Current topic: ",self.topic)
    def set_motion(self):
        title, sessionTime, speakingTime, delegate = input("Motion title: "), input("Session Time (minutes): "), input("Speaking Time (seconds): "), input("Delegate motioning: ")
        current_motion = motion(title, sessionTime, speakingTime, delegate)
        print(delegate, 'motioned for a discussion of\n', title,'with a total time of',sessionTime,'and a speaking time of',speakingTime,'.')
        return current_motion
    def timeSession(self):
        # define some timer function
        return None
