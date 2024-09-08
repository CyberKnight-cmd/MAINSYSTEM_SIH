# 5 digit User ID, 10 digit Hash code, 22.22925698, -33.45256587
# co-ordinates should have 8 digits atleast 


class Processor:
    mainString = ""
    #       User Id|Hash Code  |X co-ord  | Y co-ord
    NUM = " 0101011 0255656871 22.22956785 -33.45256587 "

    @classmethod
    def encode(cls):
        encodedString = ""
        for i in range(len(cls.NUM)):
            encodedString+=str(ord(cls.NUM[i]))
    
        return encodedString.encode('utf-8').hex()
    @classmethod
    def decode(cls,encoded):
        encoded = bytes.fromhex(encoded).decode('utf-8')
        decodedString = ""
        for i in range(2,len(encoded)+1,2):
            decodedString+=chr(int(encoded[i - 2:i]))
        return decodedString
        
def processedString(encodedString):
    processor = Processor
    return processor.decode(encodedString).split()

# if __name__ =="__main__":
#     print(processedString(Processor.encode()))
