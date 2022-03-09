class Brain:
    def __init__(self):
        self.knowledge = {}
        
    def learn(self, fileName):
        objectName = ""
        with open(fileName, 'r') as fin:

            for i,line in enumerate(fin.readlines()):
                key = line.split(':')[0]
                info = " ".join(line.split(':')[1:])
                if i == 0:
                    objectName = info.strip()
                    self.knowledge[objectName] = {}
                else:
                    self.knowledge[objectName][key] = info
        print(self.knowledge)