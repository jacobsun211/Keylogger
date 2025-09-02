class EncryptionsInformatio:
    def __init__(self):
        self.key = int(input("enter your key number"))

    def encryption(self, data:str):
        # self.encrypted_data = ""
        # for x in data:
        #     num = ord(x) ^ self.key
        #     ch = str(num)
        #     self.encrypted_data += ch
        # return self.encrypted_data

        return "".join((chr(ord(x) ^ self.key) for x in data))
    #
    # def decryption(self, data:str):
    #     return

a1 = EncryptionsInformatio()
print(a1.encryption(5, "israel yarbloom"))
