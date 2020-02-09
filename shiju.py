# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 11:38:00 2020

@author: 91467
"""

import requests

import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import os
import sys
import json
import pymysql
import random
 


def discern():
    # try:
        image_path = input("enter your image path\n")
        image_data = open(image_path, "rb").read()
        
        if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
            subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
        else:
            print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
            sys.exit()
        
        if 'COMPUTER_VISION_ENDPOINT' in os.environ:
            endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
        
        analyze_url = endpoint + "vision/v2.1/analyze"
        
       

        headers = {'Ocp-Apim-Subscription-Key': subscription_key,
                    'Content-Type': 'application/octet-stream'}
        params = {'visualFeatures': 'Categories,Description,Color'}
        response = requests.post(
            analyze_url, headers=headers, params=params, data=image_data)
        response.raise_for_status()
        analysis = response.json()
    
        analysis=json.loads(json.dumps(analysis))
        print(analysis)
    
        a1=(analysis['categories'][0]['name'])
        # a2=(analysis['categories'][0]['score'])
        image_caption = analysis["description"]["captions"][0]["text"].capitalize()
    
        # Display the image and overlay it with the caption.
        image = Image.open(BytesIO(image_data))
        plt.imshow(image)
        plt.axis("off")
        _ = plt.title(image_caption, size="x-large", y=0,color='green')
        return a1
    # except Exception:
    #     print("读取图片出错")




if __name__ == "__main__":
    a1=discern()
    db = pymysql.connect("localhost","root","Gty19981225","shiju" )
    cursor = db.cursor()
    sql="SELECT sentence,sencol FROM `shiju`.`sen` where shiju.sen.tag='"+a1+"';"
    cursor.execute(sql)
    results = cursor.fetchall()
    m=0
    for index in range(len(results)):
        m+=1
    resultList=random.sample(range(0,m),m)
    n=0
    flag=1
    while(flag==1):
        num=resultList[n]
        print(results[num][0]+"---"+results[num][1])
        flag=int(input("输入1换一句，输入0结束"))
        n+=1
        if(n>=m):
            break
    print('已经翻过所有诗句')
    db.close()
    






