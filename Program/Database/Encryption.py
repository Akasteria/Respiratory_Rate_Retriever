import hashlib
class Encryption:
    __cipher = None
    __cipherIndex = []
    def __init__(self, password):
        self.CreateCipher(password)
    def Encrypt(self, string):
        arr = bytearray(string, 'utf-8')
        for i in range(len(arr)):
            arr[i] = self.LoopedAdd(arr[i], self.Cipher(i))
        return arr.decode()
    def Decrypt(self, string):
        arr = bytearray(string, 'utf-8')
        for i in range(len(arr)):
            arr[i] = self.LoopedAdd(arr[i], -self.Cipher(i))
        return arr.decode()
    def CreateCipher(self, password):
        sha = hashlib.sha256(password.encode())
        ba = bytearray(sha.hexdigest(), 'utf-8')
        self.__cipher = ""
        self.__cipherIndex = []
        for byte in ba:
            self.__cipher = self.__cipher + str(int(byte))
            self.__cipherIndex.append(int(byte))
    def Cipher(self, index):
        return int(self.__cipher[int(self.__cipherIndex[index%len(self.__cipherIndex)])%len(self.__cipher)]) # Recursive indexing encryption
    
    @staticmethod
    def LoopedAdd(a, b):
        a = a + b
        if (a >= 256):
            a = a - 256
        if (a < 0):
            a = a + 256
        return a
if (__name__ == "__main__"):
    pw = "xcasdadwdasdaw"
    edb = Encryption(pw)
    original = "Les fleurs blanches dans le vent dansent comme des papillons."
    string = edb.Encrypt(original)
    print("Password: " + pw)
    print("Original string:  " + original)
    print("Encrypted string: " + string)
    print("Decrypted string: " + edb.Decrypt(string))
    print("Decryption successful: " + str(edb.Decrypt(string) == original))