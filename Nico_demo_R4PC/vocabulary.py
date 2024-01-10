import numpy as np

def softmax(x):
    e_x = np.exp(x - np.max(x))
    return e_x / e_x.sum(axis=0)

def Attention(query,keys,values,d):
    keys_matrix = np.array(keys,np.float32)
    values_matrix = np.array(values,np.float32)
    cossim = query.dot(keys_matrix.T)
    c = softmax(cossim/d)
    output = c.dot(values_matrix)
    return output, np.max(cossim)/len(query)

class Vocabulary:
    
    keys = []
    indices = []
    names = {}
    
    dfi = 0.1

    def act(i):
        return [np.cos(i*Vocabulary.dfi), np.sin(i*Vocabulary.dfi)]

    def Load():
        Vocabulary.keys = list(np.loadtxt("keys.npy"))
        Vocabulary.indices = list(np.loadtxt("indices.npy"))
        Vocabulary.names = {}
        with open("names.txt", "rt", encoding='utf8') as f:
            names = f.read().rstrip('\n').split('\n')
            for i, name in enumerate(names):
                Vocabulary.names[i] = name
        if len(Vocabulary.keys) != len(Vocabulary.indices):
            print('learning from scratch')
            Vocabulary.keys = []
            Vocabulary.indices = []
            Vocabulary.names = {}
        else:
            print(len(Vocabulary.keys),'keys, values loaded for',len(Vocabulary.names.keys()),'names')

    def Save():
        np.savetxt("keys.npy",np.array(Vocabulary.keys))
        np.savetxt("indices.npy",np.array(Vocabulary.indices))
        with open("names.txt", "wt", encoding='utf8') as f:
            for i in range(len(Vocabulary.names.values())):
                if i in Vocabulary.names.keys():
                    f.write(Vocabulary.names[i]+'\n')    
                else:
                    f.write('\n')
    
    def Add3(key,i,name):
        Vocabulary.keys.append(key)
        Vocabulary.indices.append(i)
        Vocabulary.names[i] = name

    def Add(key,name):
        i = len(Vocabulary.indices)
        Vocabulary.Add3(key,i,name)
        
    def EraseAll(i):
        keys = []
        indices = []
        for key, index in zip(Vocabulary.keys,Vocabulary.indices):
            if index != i:
                keys.append(key)
                indices.append(index)
        Vocabulary.keys = keys
        Vocabulary.indices = indices
        del Vocabulary.names[i]
    
    def Query(query):
        if len(Vocabulary.keys) == 0:
            return None, 0
        values = [ Vocabulary.act(i) for i in Vocabulary.indices ] 
        act, confidence = Attention(query,Vocabulary.keys,values,len(query)**0.5)
        psi = np.arctan2(act[1],act[0])
        ind = int(np.round(psi/Vocabulary.dfi))
        if ind < 0 or ind >= len(Vocabulary.names):
            return None, 0
        if not ind in Vocabulary.names.keys():
            return None, 0
        name = Vocabulary.names[ind]
        if name == "":
            return None, 0
        return name, confidence 

    def getName(ind):
        if ind < 0 or ind >= len(Vocabulary.names):
            return ""
        return Vocabulary.names[ind]
        
    def getCount(ind):
        count = 0
        for index in Vocabulary.indices:
            if index == ind:
                count += 1
        return count
