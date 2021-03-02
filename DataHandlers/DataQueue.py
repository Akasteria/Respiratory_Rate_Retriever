class DataQueue:
    def __init__(self):
        self.data = []

    def Add(self, unitData):
        self.Enqueue(unitData)
        self.Dequeue()

    def Enqueue(self, unitData):
        self.data.append(unitData)

    def Dequeue(self):
        self.data.pop(0)