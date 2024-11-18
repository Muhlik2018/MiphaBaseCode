
def getCharacter():
    f=open("./Resources/GPT/Character.txt",'r')
    api=f.readline()
    f.close()
    return api.strip()

def getKey():
    f=open("./Resources/GPT/GPTApi.txt",'r')
    api=f.readline()
    f.close()
    if api is None or api=="" or api==" ":
        f=open(".//Resources/GPT/QianfanApi.txt",'r')
        accessKey=f.readline()
        secretKey=f.readline()
        f.close()
        return [accessKey.strip(),secretKey.strip()]
    return [api.strip()]

def getLiveModel():
    f=open("./Resources/v3/ActiveModel.txt",'r')
    modelFile=f.readline()
    f.close()
    return modelFile.strip()

def getIdleWord():
    wordList=["Hey, I need my api key!"]
    f=open("./Resources/GPT/IdleWord.txt",'r')
    for line in f:
        wordList.append(line.strip())
    f.close()
    return wordList


