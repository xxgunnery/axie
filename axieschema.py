import requests
import csv
import time
import smtplib
import datetime
import webbrowser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

print("Running axielowest.py")

### GET AXIE TRADE DATA ###
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
            "variables":'{"axieId":"' + axieID + '","from":0,"size":5}',
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

def csv_writer(data, path):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)            

####
#### GET CHEAPEST AXIE STARTING FROM X ####
####

numRounds = 0

axieQueueTimes = []
axiePrices = []
axieIDs = []
axieStatSums = []
recentAxieID = ""

while numRounds < 1:
    startIndex = 0
    while startIndex < 1:
        startIndex =  str(startIndex)
        
        baseURL = "https://axieinfinity.com/graphql-server-v2/graphql"
        y = requests.post(
            baseURL,
            headers =
            {
                "User-Agent" : "Mozilla/5.0"
            },
            data = 
            { 
                "operationName" :"GetAxieBriefList",
                "variables" : 
                    {
                    "from" : 0,
                    "size" : 24,
                    "sort" : "PriceAsc",
                    "auctionType" : "Sale",
                    "owner" : "null",
                    "criteria" :
                        {
                        "region" : "null",
                        "parts" : "null",
                        "bodyShapes" : "null",
                        "classes" : "null",
                        "stages" : "null",
                        "numMystic" : "null",
                        "pureness" : "null",
                        "title" : "null",
                        "breedable" : "null",
                        "breedCount" : "null",
                        "hp" : [49,61],
                        "skill" : [],
                        "speed" : [],
                        "morale" : []
                        }
                    },
                "query":
                    {'query GetAxieBriefList($auctionType: AuctionType = Sale, $criteria: AxieSearchCriteria, $from: Int = ' + startIndex + ', $sort : SortBy = PriceAsc, $size: Int = 1, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n'}
            }
        )

        axieMarketData = y.json()
        axieMarketData = axieMarketData["data"]["axies"]["results"][0]

        axieQueueTime = time.time()
        
        axiePrice = axieMarketData["auction"]["currentPriceUSD"]
        axieBreedCount = axieMarketData["breedCount"]

        axieID = axieMarketData["id"]
        axieID = "1595030"

        if y.status_code != 200:
            print("ERROR! " + str(y.status_code))
            print(y.content.decode())
            exit()

        startIndex = int(startIndex) + 1

        if int(axieBreedCount) < 3 and float(axiePrice) < 500:
            axieData = getAxieData(axieID)

            print(axieData)

            axieData = axieData["data"]["axie"]
            axieName = axieData["name"]
            if axieName is None:
                axieName = axieID
            axieClass = axieData["class"]
            if axieClass is None:
                axieClass = "Egg"
            axieHP = axieData["stats"]["hp"]
            axieSpeed = axieData["stats"]["speed"]
            axieSkill = axieData["stats"]["skill"]
            axieMorale = axieData["stats"]["morale"]
            axiePic = axieData["image"]

            axieStatSum = str(axieHP + axieSpeed + axieSkill + axieMorale)
            
            axieHP = str(axieData["stats"]["hp"])
            axieSpeed = str(axieData["stats"]["speed"])
            axieSkill = str(axieData["stats"]["skill"])
            axieMorale = str(axieData["stats"]["morale"])

            axieMove1 = ""
            axieMove1Attack = ""
            axieMove1Defense = ""
            axieMove1Energy = ""
            axieMove1Desc = ""
            axieMove2 = ""
            axieMove2Attack = ""
            axieMove2Defense = ""
            axieMove2Energy = ""
            axieMove2Desc = ""
            axieMove3 = ""
            axieMove3Attack = ""
            axieMove3Defense = ""
            axieMove3Energy = ""
            axieMove3Desc = ""
            axieMove4 = ""
            axieMove4Attack = ""
            axieMove4Defense = ""
            axieMove4Energy = ""
            axieMove4Desc = ""
            
            partNum = 0
            moveNum = 0
            for part in axieData["parts"]:
                partAbilities = part["abilities"]
                if part["abilities"] != []:
                    partAbilities = partAbilities[0]
                    if moveNum == 0:
                            axieMove1 = partAbilities["name"]
                            axieMove1Attack = partAbilities["attack"]
                            axieMove1Defense = partAbilities["defense"]
                            axieMove1Energy = partAbilities["energy"]
                            axieMove1Desc = partAbilities["description"]
                            moveNum += 1
                    elif moveNum == 1:
                            axieMove2 = partAbilities["name"]
                            axieMove2Attack = partAbilities["attack"]
                            axieMove2Defense = partAbilities["defense"]
                            axieMove2Energy = partAbilities["energy"]
                            axieMove2Desc = partAbilities["description"]
                            moveNum += 1
                    elif moveNum == 2:
                            axieMove3 = partAbilities["name"]
                            axieMove3Attack = partAbilities["attack"]
                            axieMove3Defense = partAbilities["defense"]
                            axieMove3Energy = partAbilities["energy"]
                            axieMove3Desc = partAbilities["description"]
                            moveNum += 1
                    elif moveNum == 3:
                            axieMove4 = partAbilities["name"]
                            axieMove4Attack = partAbilities["attack"]
                            axieMove4Defense = partAbilities["defense"]
                            axieMove4Energy = partAbilities["energy"]
                            axieMove4Desc = partAbilities["description"]
                            moveNum += 1
                partNum += 1

            axieIDs.append(axieID)
            axieQueueTimes.append(axieQueueTime)
            axiePrices.append(axiePrice)
            axieStatSums.append(axieStatSum)

    numRounds += 1
    time.sleep(0.5)

csvRows = []

x = 0
while x < len(axieIDs):
    csvRows.append([axieIDs[x],axieQueueTimes[x], axiePrices[x],axieStatSums[x]])
    x += 1

path = "output.csv"

csv_writer(csvRows, path)

print("Program axielowest.py Complete!")
     







