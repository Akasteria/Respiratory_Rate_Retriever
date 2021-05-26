import sqlite3
import hashlib
import time
import datetime
import random
from .Encryption import Encryption
class Database:
    __payload = "Les fleurs blanches dans le vent dansent comme des papillons."
    payloadName = "Payload"
    connection = None
    encryption = None
    cursor = None
    RRtableName = "RR"
    insertTable = "INSERT OR IGNORE INTO '{tableName}' VALUES({args})"
    createTable = "CREATE TABLE IF NOT EXISTS '{tableName}'({args}, UNIQUE('{unique}'))"
    selectTable = "SELECT * FROM sqlite_master WHERE type='table' AND name='{}'"
    selectFromTable = "SELECT * FROM {tableName} Where {query}"
    def LoadDB(self, name, password):
        sha = hashlib.sha1(name.encode())
        self.connection = sqlite3.connect(sha.hexdigest() + '.db')
        self.cursor = self.connection.cursor()
        self.encryption = Encryption(password)
        self.cursor.execute(self.selectTable.format('Payload'))
        a = self.cursor.fetchall()
        if (len(a) == 0 or a[0][0] == 0):
            #print('Incorrect password')
            #self.CreateDatabase()
            return False
        return True
    def CreateDatabase(self):
        self.CreateTable(self.payloadName, self.__payload)
        self.InsertIntoTable(self.payloadName, self.encryption.Encrypt(self.__payload))
        self.CreateTable(self.RRtableName, 'year', 'month', 'day', 'hour', 'minute', 'rate', 'abnormal', 'exercise', 'UID')
    def CreateTable(self, tableName, *args):
        rowTitles = ""
        for arg in args:
            rowTitles = rowTitles + "'" + arg + "'" + " text, "
        rowTitles = rowTitles[:-2] # Remove tailing ', '
        #print(self.createTable.format(tableName = tableName, args = rowTitles))
        self.cursor.execute(self.createTable.format(tableName = tableName, args = rowTitles, unique = args[-1]))
        self.connection.commit()
        
    def InsertIntoTable(self, tableName, *args):
        values = ""
        for i in range(len(args)):
            values = values + "?, "
        values = values[:-2]# Remove tailing ', '
        #print(self.insertTable.format(tableName = tableName, args = values))

        self.cursor.execute(self.insertTable.format(tableName = tableName, args = values), args)
        self.connection.commit()
        #self.cursor.execute("Select * FROM " + "'" + tableName + "'")
        #print(self.cursor.fetchall())
    def InsertEncryptedWithUID(self, tableName, *args):
        Uid = hashlib.sha256(",".join(args).encode()).hexdigest()
        encryptedValues = []
        for arg in args:
            encryptedValues.append(self.encryption.Encrypt(arg))
        encryptedValues.append(Uid)
        encryptedValues = tuple(encryptedValues)
        self.InsertIntoTable(tableName, *encryptedValues)
        
    def DropTable(self, tableName):
        try:
            self.cursor.execute("DROP TABLE " + "'" + tableName + "'")
            self.connection.commit()
        except:
            pass
    def EraseDatabase(self):
        self.DropTable(self.RRtableName)
        self.DropTable(self.payloadName)
    def SaveMinute(self, year, month, day, hour, minute, rate, abnormal, exercise):
        self.InsertEncryptedWithUID(self.RRtableName, year, month, day, hour, minute, rate, abnormal, exercise)
    def ReadMinute(self, year, month, day, hour, minute):
        condArr = ['year = ' + self.EncryptAndEnclose(str(year)), 'month = '+ self.EncryptAndEnclose(str(month)), 'day = '+ self.EncryptAndEnclose(str(day)), 'hour = '+ self.EncryptAndEnclose(str(hour)), 'minute = '+ self.EncryptAndEnclose(str(minute))]
        query = ' AND '.join(condArr)
        self.cursor.execute(self.selectFromTable.format(tableName = self.RRtableName, query = query))
        cur = self.cursor.fetchall()
        if (len(cur) == 0):
            return []
        return [self.DecryptAll([cur[0][5], cur[0][6], cur[0][7]])]
    def ReadHour(self, year, month, day, hour):
        condArr = ['year = ' + self.EncryptAndEnclose(str(year)), 'month = '+ self.EncryptAndEnclose(str(month)), 'day = '+ self.EncryptAndEnclose(str(day)), 'hour = '+ self.EncryptAndEnclose(str(hour))]
        query = ' AND '.join(condArr)
        self.cursor.execute(self.selectFromTable.format(tableName = self.RRtableName, query = query))
        cur = self.cursor.fetchall()
        if (len(cur) == 0):
            return []
        arr = []
        for row in cur:
            arr.append(self.DecryptAll([row[4], row[5], row[6], row[7]]))
        return arr
    def ReadDay(self, year, month, day):
        condArr = ['year = ' + self.EncryptAndEnclose(str(year)), 'month = '+ self.EncryptAndEnclose(str(month)), 'day = '+ self.EncryptAndEnclose(str(day))]
        query = ' AND '.join(condArr)
        self.cursor.execute(self.selectFromTable.format(tableName = self.RRtableName, query = query))
        cur = self.cursor.fetchall()
        if (len(cur) == 0):
            return []
        arr = []
        for row in cur:
            arr.append(self.DecryptAll([row[3], row[4], row[5], row[6], row[7]]))
        return arr
    def ReadMonth(self, year, month):
        condArr = ['year = ' + self.EncryptAndEnclose(str(year)), 'month = '+ self.EncryptAndEnclose(str(month))]
        query = ' AND '.join(condArr)
        self.cursor.execute(self.selectFromTable.format(tableName = self.RRtableName, query = query))
        cur = self.cursor.fetchall()
        if (len(cur) == 0):
            return []
        arr = []
        for row in cur:
            arr.append(self.DecryptAll([row[2], row[3], row[4], row[5], row[6], row[7]]))
        return arr
    def CloseDB(self):
        self.connection.close()
    def EncryptAndEnclose(self, string):
        newstr = self.encryption.Encrypt(str(string))
        newstr = "'"+newstr+"'"
        return newstr
    def DecryptAll(self, arr):
        plain = []
        for element in arr:
            plain.append(self.encryption.Decrypt(element))
        return tuple(plain)
    def GeneratePseudodata(self):
        self.EraseDatabase()
        self.CreateDatabase()
        t = datetime.datetime(time.gmtime()[0],time.gmtime()[1],time.gmtime()[2],time.gmtime()[3],time.gmtime()[4],time.gmtime()[5],time.gmtime()[6],None)
        for i in range (60):
            day = t - datetime.timedelta(days = i)
            if (random.randint(0,100)>95):
                print(str(day)+'missing')
                continue
            for h in range (10,18):
                if (random.randint(0,100)>95):
                    print(str(day)+'exercising')
                    for m in range(60):
                        self.SaveMinute(str(day.year), str(day.month),str(day.day),str(h),str(m),str(random.randint(30,33)),'0','1')
                    continue
                if (random.randint(0,100)>95):
                    print(str(day)+'abnormal')
                    for m in range(60):
                        self.SaveMinute(str(day.year), str(day.month),str(day.day),str(h),str(m),str(random.randint(25,30)),'1','0')
                    continue
                for m in range(60):
                    self.SaveMinute(str(day.year), str(day.month),str(day.day),str(h),str(m),str(random.randint(15,17)),'0','0')
        
if (__name__ == '__main__'):
    db = Database()
    db.LoadDB('test', 'pwd')
    #db.CreateDatabase()
    #db.GeneratePseudodata()
    #for i in range(60):
    #    db.SaveMinute('2021', '4', '1', '4', str(i), '20', '0', '0')
    #for i in range(60):
    #    db.SaveMinute('2021', '4', '1', '5', str(i), '20', '0', '0')
    #print(db.ReadDay(2021,4,1))
    #db.EraseDatabase()