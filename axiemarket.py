import requests
import csv
import codecs
import time
import smtplib
import datetime
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Running axiemarket.py")
### GET AXIE TRADE DATA ###cled
def getAxieTradeData(axieID):

    baseURL = "https://axieinfinity.com/graphql-server-v2/graphql"
    y = requests.post(
        baseURL,
        headers =
        {
            "User-Agent" : "Mozilla/5.0"
        },
        data = {
            "operationName":"GetAxieTransferHistory",
            "variables":'{"axieId":"' + axieID + '","from":0,"size":10}',
            "query":"query GetAxieTransferHistory($axieId: ID!, $from: Int!, $size: Int!) {\n  axie(axieId: $axieId) {\n    id\n    transferHistory(from: $from, size: $size) {\n      ...TransferRecords\n      __typename\n    }\n    ethereumTransferHistory(from: $from, size: $size) {\n      ...TransferRecords\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment TransferRecords on TransferRecords {\n  total\n  results {\n    from\n    to\n    timestamp\n    txHash\n    withPrice\n    __typename\n  }\n  __typename\n}\n"}
    )

    axieTrades = y.json()

    axieTrades = axieTrades["data"]["axie"]["transferHistory"]

    if axieTrades["total"] != 0:
        axieRecentTrade = axieTrades["results"][0]["timestamp"]
    else:
        axieRecentTrade = 600

    if y.status_code != 200:
        print("ERROR! " + str(y.status_code))
        print(y.content.decode())
        exit()
    
    return axieRecentTrade

### PING AXIE INDIV DATA ###
def getAxieData(axieID):

    baseURL = "https://axieinfinity.com/graphql-server-v2/graphql"
    y = requests.post(
        baseURL,
        headers =
        {
            "User-Agent" : "Mozilla/5.0"
        },
        data = {"operationName":"GetAxieDetail",  "variables" :'{ "axieId" : ' + axieID + '}' ,"query":"query GetAxieDetail($axieId: ID!) {\n  axie(axieId: $axieId) {\n    ...AxieDetail\n    __typename\n  }\n}\n\nfragment AxieDetail on Axie {\n  id\n  image\n  class\n  chain\n  name\n  genes\n  owner\n  birthDate\n  bodyShape\n  class\n  sireId\n  sireClass\n  matronId\n  matronClass\n  stage\n  title\n  breedCount\n  level\n  figure {\n    atlas\n    model\n    image\n    __typename\n  }\n  parts {\n    ...AxiePart\n    __typename\n  }\n  stats {\n    ...AxieStats\n    __typename\n  }\n  auction {\n    ...AxieAuction\n    __typename\n  }\n  ownerProfile {\n    name\n    __typename\n  }\n  battleInfo {\n    ...AxieBattleInfo\n    __typename\n  }\n  children {\n    id\n    name\n    class\n    image\n    title\n    stage\n    __typename\n  }\n  __typename\n}\n\nfragment AxieBattleInfo on AxieBattleInfo {\n  banned\n  banUntil\n  level\n  __typename\n}\n\nfragment AxiePart on AxiePart {\n  id\n  name\n  class\n  type\n  specialGenes\n  stage\n  abilities {\n    ...AxieCardAbility\n    __typename\n  }\n  __typename\n}\n\nfragment AxieCardAbility on AxieCardAbility {\n  id\n  name\n  attack\n  defense\n  energy\n  description\n  backgroundUrl\n  effectIconUrl\n  __typename\n}\n\nfragment AxieStats on AxieStats {\n  hp\n  speed\n  skill\n  morale\n  __typename\n}\n\nfragment AxieAuction on Auction {\n  startingPrice\n  endingPrice\n  startingTimestamp\n  endingTimestamp\n  duration\n  timeLeft\n  currentPrice\n  currentPriceUSD\n  suggestedPrice\n  seller\n  listingIndex\n  state\n  __typename\n}\n"}
    )

    if y.status_code != 200:
        print("ERROR! " + str(y.status_code))
        print(y.content.decode())
        exit()

    axieData = y.json()

    return axieData

def csv_writer_preserve(data, path):
    with open(path, "a+", newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(data)
        # for line in data:
        #     writer.writerow(line)            

numRounds = 0
csvRows = []
lastXHash = ["","","","","","","","","",""]

while numRounds < 5:
    baseURL = "https://axieinfinity.com/graphql-server-v2/graphql"
    y = requests.post(
        baseURL,
        headers =
        {
            "User-Agent" : "Mozilla/5.0"
        },
        data = {
        "operationName":"GetRecentlyAxiesSold",
        "variables": {
                "from":0,"size":1,
                "sort":"Latest",
                "auctionType":"Sale"},
                "query":"query GetRecentlyAxiesSold($from: Int, $size: Int = 10) {\n  settledAuctions {\n    axies(from: $from, size: $size) {\n      total\n      results {\n        ...AxieSettledBrief\n        transferHistory {\n          ...TransferHistoryInSettledAuction\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieSettledBrief on Axie {\n  id\n  name\n  image\n  class\n  breedCount\n  __typename\n}\n\nfragment TransferHistoryInSettledAuction on TransferRecords {\n  total\n  results {\n    ...TransferRecordInSettledAuction\n    __typename\n  }\n  __typename\n}\n\nfragment TransferRecordInSettledAuction on TransferRecord {\n  from\n  to\n  txHash\n  timestamp\n  withPrice\n  withPriceUsd\n  fromProfile {\n    name\n    __typename\n  }\n  toProfile {\n    name\n    __typename\n  }\n  __typename\n}\n"}
    )

    axieMarketData = y.json()

    print(str(y) + " " + str(len(axieMarketData["data"]["settledAuctions"]["axies"])) + " " + str(len(axieMarketData["data"]["settledAuctions"])))

    axieMarketData = axieMarketData["data"]["settledAuctions"]["axies"]["results"]
    numTx = len(axieMarketData)
    print(numTx)

    duplicate="n"
    x = 0
    while x < numTx:
        currentAxie = axieMarketData[x]
        if currentAxie["id"] is not None:
            axieID = currentAxie["id"]
        else:
            axieID = "None"
        if currentAxie["name"] is not None:
            axieName = currentAxie["name"]
        else:
            axieID = "None"
        axieImage = currentAxie["image"]

        axieMostRecentTransfer = currentAxie["transferHistory"]["results"][0]

        txHash = axieMostRecentTransfer["txHash"]

        x1 = 0
        while x1 < len(lastXHash):
            if txHash == lastXHash[x1]:
                lastXHash[x1] = txHash
                duplicate = "y"
                #print(x1)
                #print(txHash)
                #print(lastXHash[x1])
                break
            else:
                duplicate = "n"
            x1+=1
        
        if duplicate != "y":
            lastXHash[x] = txHash
        else:
            break

        #print(str(x) +  " " + str(numTx))
        #print(lastXHash)

        if axieMostRecentTransfer["timestamp"] is None:
            timestamp = str(int(time.time()))
        else:
            timestamp = axieMostRecentTransfer["timestamp"]
        txPrice = axieMostRecentTransfer["withPriceUsd"]
        txPriceEth = int(axieMostRecentTransfer["withPrice"])/1000000000000000000
        txPriceEth = str(txPriceEth)

        sellerName = axieMostRecentTransfer['fromProfile']['name']
        buyerName = axieMostRecentTransfer['toProfile']['name']

        axieData = getAxieData(axieID)
        print("axieData")
        print(axieData)

        axieData = axieData["data"]["axie"]
        axieName = axieData["name"]
        axieBody = axieData["bodyShape"]
        if axieName is None:
            axieName = axieID
        axieClass = axieData["class"]
        if axieClass is None:
            axieClass = "Egg"

        axieHP = axieData["stats"]["hp"]
        axieSpeed = axieData["stats"]["speed"]
        axieSkill = axieData["stats"]["skill"]
        axieMorale = axieData["stats"]["morale"]
        
        axieHP = str(axieData["stats"]["hp"])
        axieSpeed = str(axieData["stats"]["speed"])
        axieSkill = str(axieData["stats"]["skill"])
        axieMorale = str(axieData["stats"]["morale"])

        partsList = ["","","","","",""]
        extrasList = ["","","","","",""]
        partClassList = ["","","","","",""]
        purity = 0
        
        partNum = 0
        for part in axieData["parts"]:
            partName = part["name"]
            partsList[partNum] = partName

            partClass = part["class"]
            partType = part["type"]
            specialGenes = part["specialGenes"]
            if specialGenes is None:
                specialGenes = "None"
            stage = part["stage"]
            extraAppend = str(partClass + " " + partType + " " + specialGenes + " " + str(stage))

            extrasList[partNum] = extraAppend
            partClassList[partNum] = partClass
            partNum+=1
        
        x = 0
        while x < len(partClassList):
            if partClassList[x] == axieClass:
                purity+=1
            x+=1
        print(purity)

        csvRow = [axieID,axieName,timestamp,txPrice,txPriceEth,sellerName,buyerName,txHash,axieClass,axieBody,axieHP,axieSpeed,axieSkill,axieMorale,partsList[0],partsList[1],partsList[2],partsList[3],partsList[4],partsList[5],extrasList[0],extrasList[1],extrasList[2],extrasList[3],extrasList[4],extrasList[5],purity]
        path = "outputMarket.csv"
        csv_writer_preserve(csvRow, path)
        #print(csvRows)

        x+=1

    if y.status_code != 200:
        print(y)
        print("ERROR! " + str(y.status_code))
        print(y.content.decode())
        exit()

    numRounds += 1
    time.sleep(3)

print("Program axiemarket.py Complete!")
     







