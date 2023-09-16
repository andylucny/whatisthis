import PySimpleGUI as sg
from agentspace import Agent, space
import numpy as np
import time
import os
from vocabulary import Vocabulary

class GuiAgent(Agent):

    def __init__(self, nameFeatures, nameIt, nameKey):
        self.nameFeatures = nameFeatures
        self.nameIt = nameIt
        self.nameKey = nameKey
        super().__init__()
        
    def init(self):
        #GUI
        MaxN = 16
        Vocabulary.Load()
        layout = []
        for i in range(MaxN):
            name =  Vocabulary.getName(i)
            count = Vocabulary.getCount(i)
            layout.append([
                sg.Text(f"{i:2d}", size=(4, 1)), 
                sg.Input(f"{name}", size=(25, 1), key=f"Name{i}"), 
                sg.Text(f"{count:2d}", key=f"Count{i}", size=(4, 1)), 
                sg.Button("Add", key=f"Add{i}", size=(7, 1)),
                sg.Button("Erase", key=f"Erase{i}", size=(7, 1)),
                sg.Button("Fix", key=f"Fix{i}", size=(7, 1)),
            ])
        layout.append([
            sg.Button("Name it", size=(10, 1)),
            sg.Button("Save", size=(10, 1)),
            sg.Button("Reload", size=(10, 1)),
            sg.Button("Exit", size=(10, 1)),
        ])
        window = sg.Window("What is what", layout, finalize=True)
        window.bind("<Return>", "Name it")
        while True:
            event, values = window.read(timeout=1)
#            if event != "__TIMEOUT__":
#                print(event)
            if event == "Exit" or event == sg.WIN_CLOSED:
                break
            elif event == "Name it":
                time.sleep(0.4)
                space[self.nameIt] = True
            elif event == "Reload":
                Vocabulary.Load()
                for i in range(MaxN):
                    name =  Vocabulary.getName(i)
                    count = Vocabulary.getCount(i)
                    window[f"Name{i}"].update(value=f"{name}")
                    window[f"Count{i}"].update(value=f"{count:2d}")
            elif event == "Save":
                Vocabulary.Save()
            elif event.startswith("Add"):
                i = int(event[len("Add"):])
                key = space[self.nameFeatures]
                name = values[f"Name{i}"].strip()
                if key is not None and name != "":
                    Vocabulary.Add(key,i,name)
                    count = Vocabulary.getCount(i)
                    window[f'Count{i}'].update(value=f"{count:2d}")
            elif event.startswith("Fix"):
                i = int(event[len("Fix"):])
                key = space[self.nameKey]
                name = values[f"Name{i}"]
                if key is not None:
                    Vocabulary.Add(key,i,name)
                count = Vocabulary.getCount(i)
                window[f'Count{i}'].update(value=f"{count:2d}")
            elif event.startswith("Erase"):
                i = int(event[len("Erase"):])
                Vocabulary.EraseAll(i)
                count = Vocabulary.getCount(i)
                window[f'Name{i}'].update(value="")
                window[f'Count{i}'].update(value=f"{count:2d}")
            
        window.close()
        self.stop()
        os._exit(0)
               
    def senseSelectAct(self):
        pass
