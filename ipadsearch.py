import aiohttp
import asyncio
import pandas
import time
import json
from flask import Flask, request
from bs4 import BeautifulSoup

headers = {
    'user-agent':
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}
url = "https://feebee.com.tw/channel/mobile"

# phone
phoneName = list()
phoneImg = list()
phoneMinPrice = list()
phoneMaxPrice = list()
phoneData = {
    "phoneName": phoneName,
    "phoneImg": phoneImg,
    "phoneMinPrice": phoneMinPrice,
    "phoneMaxPrice": phoneMaxPrice,
}

# phone accessories
accName = list()
accImg = list()
accMinPrice = list()
accMaxPrice = list()
accData = {
    "accName": accName,
    "accImg": accImg,
    "accMinPrice": accMinPrice,
    "phoneMaxPrice": accMaxPrice
}

# widget accessories
widName = list()
widImg = list()
widMinPrice = list()
widMaxPrice = list()
widData = {
    "widName": widName,
    "widImg": widImg,
    "widMinPrice": widMinPrice,
    "widMaxPrice": widMaxPrice
}

app = Flask(__name__)

# def _init_(self, url, html):
#     self.url = url 
#     self.headers = headers
#     self.html = html 
#     self.data = ""

def _parse_results(url, html):
    # print(url)
    try: 
      soup = BeautifulSoup(html, 'html.parser')
      p = soup.select("div#mobile_手機 > ul > li > a.link_ghost > img")
      p2 = soup.select("div#mobile_手機配件 > ul > li > a.link_ghost > img")
      p3 = soup.select("div#mobile_智慧穿戴與配件 > ul > li > a.link_ghost > img")
      p4 = soup.select("div#mobile_手機 > ul > li > span > meta")
      p5 = soup.select("div#mobile_手機配件 > ul > li > span > meta")
      p6 = soup.select("div#mobile_智慧穿戴與配件 > ul > li > span > meta")
      # print(p)
      for i in range(10):
          phoneName.append(p[i].get('alt'))
          accName .append(p2[i].get('alt'))
          widName.append(p3[i].get('alt'))
          # print('pName:', pName)
          phoneImg.append(p[i].get('src'))
          accImg.append(p2[i].get('src'))
          widImg.append(p3[i].get('src'))
          # print('img:', img)

      for i in range(30):
        if(i%3 == 1):
          phoneMinPrice.append(p4[i] .get('content'))
          accMinPrice.append(p5[i] .get('content'))
          widMinPrice.append(p6[i] .get('content'))
          # print('minPrice:' ,minPrice, i )
        if(i%3 == 2):
          phoneMaxPrice.append(p4[i] .get('content'))
          accMaxPrice .append(p5[i] .get('content'))
          widMaxPrice.append(p6[i] .get('content'))
          # print('maxPrice:' ,maxPrice, i)
    except Exception as e:
      raise e

async def fetch(session, url, headers):
    # url = url + ss
    async with  session.get(url, headers = headers, timeout = 10) as response:
        return await response.text()

async def main():
    async with aiohttp.ClientSession() as client:
        html = await fetch(client, url, headers = headers)
        try:
          _parse_results(url, html)
        except Exception as e:
          raise e

loop = asyncio.get_event_loop()

@app.route('/', methods=['POST'])
def gogo():
  # request.get_json()
  #t1 = time.time()
  loop.run_until_complete(main())
  phoneTable = pandas.DataFrame(phoneData)
  accTable = pandas.DataFrame(accData)
  widTable = pandas.DataFrame(widData)
  #t2 = time.time()
  #print('t2-t1', t2-t1)
  phoneOutput = json.loads(phoneTable.to_json(orient='records', force_ascii=False)) #每個第一筆加成json物件
  accOutput = json.loads(accTable.to_json(orient='records', force_ascii=False))
  widOutput = json.loads(widTable.to_json(orient='records', force_ascii=False))

  print(phoneOutput)
  print(accOutput)
  print(widOutput)
  #t3 = time.time()
  #print('t3-t2', t3-t2)
  haha = {"phone": phoneOutput,"accessory": accOutput,"widget": widOutput}
  # print(phoneOutput)
  return  haha


@app.route('/', methods=['GET'])
def getDisplay():
    return "Please Use Post Method"


if __name__ == '__main__':
     app.run()