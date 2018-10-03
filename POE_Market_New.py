# -*- coding: utf-8 -*-
"""
Created on Tue Oct  2 11:17:02 2018

@author: 羅宇呈
"""

import pythoncom, pyHook
import win32clipboard
import requests
import json
import time
import threading
import os


#pyHook control keyboard input
def OnKeyboardEvent(event):
    global STOP
    global index
    global Clipboard_base
    global Database
    global price_text
    global tmp
    global Item_base
    global count
    global item_amount
    global url_get
    global post
    print ('MessageName:',event.MessageName)
    print ('Message:',event.Message)
    print ('Time:',event.Time)
    print ('Window:',event.Window)
    print ('WindowName:',event.WindowName)
    print ('Ascii:', event.Ascii, chr(event.Ascii))
    print ('Key:', event.Key)
    print ('KeyID:', event.KeyID)
    print ('ScanCode:', event.ScanCode)
    print ('Extended:', event.Extended)
    print ('Injected:', event.Injected)
    print ('Alt', event.Alt)
    print ('Transition', event.Transition)
    print ('---')
    if (event.Key=='E'):
        #hm.KeyDown=win32con.WM_CLOSE     
        STOP=1 
        return True
    elif (event.Key=='Down'):
        print(len(Database))        
        if((index+10)<len(Database)-10):index=index+10
        print(index)
        show_price_text(index,price_text)
        return True
    elif (event.Key=='Up'):
        if((index-10)>=0):index=index-10
        show_price_text(index,price_text)
        print(index)
        return True
    elif (event.Key=='Left'):
        show_price_text(index,price_text)
        return True
    elif ((event.Key=='0')or (event.Key=='1') or (event.Key=='2') or (event.Key=='3') or (event.Key=='4') or (event.Key=='5') or (event.Key=='6') or (event.Key=='7') or (event.Key=='8') or (event.Key=='9')):
        tmp=index+int(event.Key)
        print(index,tmp)
        ans=Clipboard_base[tmp]
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
        win32clipboard.CloseClipboard()  
        print(ans)
        return True
    elif (event.Key=='A'):
        ans=Item_base[tmp].whisper
        #print(ans)
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
        win32clipboard.CloseClipboard()
        print(ans)
        return True
    elif(event.Key=='Z'):
        if(count<int(item_amount)):
            ans="正在獲取下100筆資料..."
            
            #print("akesjfgha",count)
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
            win32clipboard.CloseClipboard() 
            count=count+100
            
            Final_Part(url_get,post['result'],Clipboard_base,Database)
            Create_price_text(price_text)
            
        else:
            ans="無法獲取下100筆資料!!"
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
            win32clipboard.CloseClipboard()
        return True
    elif(event.Key=='Q'):
        for i in range(len(Clipboard_base)):
            print(i,Clipboard_base[i])
        print(len(Clipboard_base))
        print(len(Database))
        print(len(Item_base))
        return True
    elif(event.Key=='D'):
        ans=Clipboard_base[tmp]+data
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
        win32clipboard.CloseClipboard()
        print(ans)
        return True
    # return True1ddddd to pass the event to other handlers
    else:
        return True
#--------------------------------------------------------------------------------------------------------------
#functions for POE Markete
def show_price_text(index,price_text):
    #print(price_text)
    ans=price_text[0]+'\n'+price_text[1]+'\n'+price_text[2]+'\n'
    for i in range(index+3,index+13):
        ans=ans+price_text[int(i)]+'\n'
    ans=ans+price_text[0]
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans)
    win32clipboard.CloseClipboard()        
    print(ans)
    return True      
def socket_translation(sockets):
    translation=[[] for i in range(6)]
    ans=[]
    for i in range(len(sockets)):     
        translation[sockets[i]['group']].append(sockets[i]['sColour'])
    for i in range(6):
        result=''
        for j in range(len(translation[i])):
            result=result+translation[i][j]
            if(j!=len(translation[i])-1): result=result+'-'
        ans.append(result)        
    return ans        

def price_translation(price):
    #print(price)
    
    if(price==None):
        ans='未標價'
    #print('zzz',price['type'])
    else:
        if(price['type']=='~price'):ans='直購不二價 '
        else: ans='直購可議價 ' 
        
        ans=ans+str(price['amount'])
        cur=''
    #print(price['currency'])
        if(price['currency']=='alt'):cur=' 改造石'
        elif(price['currency']=='alch'):cur=' 點金石'
        elif(price['currency']=='chaos'):cur=' 混沌石'
        elif(price['currency']=='fuse'):cur=' 鏈結石'
        elif(price['currency']=='chisel'):cur=' 製圖釘'
        elif(price['currency']=='chrom'):cur=' 幻色石'
        elif(price['currency']=='exa'):cur=' 崇高石'
        elif(price['currency']=='orb'):cur=' 神聖石'
        elif(price['currency']=='gcp'):cur=' 寶石匠的稜鏡'
        elif(price['currency']=='vaal'):cur=' 瓦爾寶珠'
        elif(price['currency']=='ggb'):cur=' 玻璃彈珠'
        else: cur='Unknown'
        ans=ans+cur
        
    return ans 

def properties_translation(properties):
    ans=[]
    for i in range(len(properties)):
        if(len(properties[i]['values'])==0): ans.append(properties[i]['name'])
        else: ans.append(properties[i]['name']+': '+properties[i]['values'][0][0])
    return ans

def explicitMods_translation(explicitMods,mods):
    ans=[]
    for i in range(len(explicitMods)):
        
        if(i>=len(mods['explicit'])):
            #print("zz")
            ans.append(explicitMods[i])
        else:
            ans.append(explicitMods[i]+' ('+str(mods['explicit'][i]['magnitudes'][0]['min'])+' ~ '+str(mods['explicit'][i]['magnitudes'][0]['max'])+')')
    return ans   
           
def fetch(url):
    response = requests.get(url)
    return response

def create_clipboard_Item(Item):
    board=int(len(Item.whisper)*1.5)
    #print(board)
    Result='_'*(board)+'\n'
    Result=Result+'|'+Item.name+' '*(board-len('|'+Item.name))+'\n'
    Result=Result+'|'+Item.typeLine+' '*(board-len('|'+Item.typeLine))+'\n'
    Result=Result+'|'+'_'*(board-1)+'\n'
    Result=Result+'|'+'插槽: '
    for i in range(len(Item.sockets)):
        if(Item.sockets[i]!=''):
            Result=Result+Item.sockets[i]
            if(i!=len(Item.sockets)): Result=Result+' '
    Result=Result+'\n'
    Result=Result+'|'+'_'*(board-1)+'\n'
    if(Item.identified==False): 
        Result=Result+'|'+'未鑑定'+'\n'
    for i in range(len(Item.properties)):
        Result=Result+'|'+Item.properties[i]
        if(i!=len(Item.properties)): Result=Result+'\n'
        
    Result=Result+'|'+'物品等級: '+str(Item.ilvl)+'\n'
    Result=Result+'|'+'需求: '
    for i in range(len(Item.requirements)):
        Result=Result+Item.requirements[i]
        if(i!=len(Item.requirements)-1): Result=Result+','
    Result=Result+'\n'
    Result=Result+'|'+'_'*(board-1)+'\n'
    for i in range(len(Item.explicitMods)):
        Result=Result+'|'+Item.explicitMods[i]
        if(i!=len(Item.explicitMods)-1):
            Result=Result+'\n'
        
    Result=Result+'\n'
    Result=Result+'|'+'_'*(board-1)+'\n'
    for i in range(len(Item.flavourText)):
        Result=Result+'|'+Item.flavourText[i]
        if(i!=len(Item.flavourText)-1): Result=Result+'\n'
    Result=Result+'\n'
    Result=Result+'|'+'_'*(board-1)+'\n'
    Result=Result+'|'+'賣家售價: '+Item.price+'\n'
    Result=Result+'|'+'賣家: '+Item.seller_name+' in '+Item.league+' ( '+Item.status+' ) \n'
    
    Result=Result+'|'+Item.whisper+'\n'
    Result=Result+'|'+'搜尋時間:'+str(time.time()-begin)+' s'+'\n'
    Result=Result+'_'*(board)
    #print(Result)
    return Result

def create_Item(ten_items):
    ItemList=[]    
    if(ten_items.get('result',-1)==-1):
        print(ten_items)
    for i in range(len(ten_items['result'])):
        
        #print(ten_items['result'][i]['item'])
        #if(i==0):
        #    print(type(ten_items['result'][i]['listing']['price']))
        ilvl=ten_items['result'][i]['item']['ilvl']
        league=ten_items['result'][i]['item']['league']
        if(ten_items['result'][i]['item'].get('sockets',-1)==-1):
            sockets=''
        else:
            sockets=socket_translation(ten_items['result'][i]['item']['sockets'])

        price=price_translation(ten_items['result'][i]['listing']['price'])
        if(ten_items['result'][i]['item'].get('properties',-1)==-1):
            properties=ten_items['result'][i]['item']['implicitMods']
        else:
            properties=properties_translation(ten_items['result'][i]['item']['properties'])
        
        #print(properties)
        seller_name=ten_items['result'][i]['listing']['account']['lastCharacterName']
        date=ten_items['result'][i]['listing']['indexed']
        whisper=ten_items['result'][i]['listing']['whisper']
        identified=ten_items['result'][i]['item']['identified']
        #.get('requirements',default=-1)
        if(ten_items['result'][i]['item'].get('requirements',-1)==-1):
            requirements=''
        else:
            requirements=properties_translation(ten_items['result'][i]['item']['requirements'])
        if(ten_items['result'][i]['item']['identified']):
            explicitMods=explicitMods_translation(ten_items['result'][i]['item']['explicitMods'],ten_items['result'][i]['item']['extended']['mods'])
            flavourText=ten_items['result'][i]['item']['flavourText']
            name=ten_items['result'][i]['item']['name']
            typeLine=ten_items['result'][i]['item']['typeLine']
        else:
            explicitMods=''
            flavourText=''
            name='未鑑定'
            typeLine=''
        if(ten_items['result'][i]['listing']['account']['online']==None):
            status='不在線上'
        elif(ten_items['result'][i]['listing']['account']['online'].get('status',-1)==-1):
            status='線上'
        else:
            status=ten_items['result'][i]['listing']['account']['online']['status']
        ItemList.append(Item(name,typeLine,ilvl,league,sockets,price,properties,seller_name,date,whisper,identified,requirements, explicitMods,flavourText,status))
    return ItemList


def get_request(start,end,post_result,url):
    
    for i in range(start,end):
        #print(start,end)
       # print(len(post_result))
        if(i>=len(post_result)):
            print("Out of Range")
        else:
            if(i!=end-1 and i!=len(post_result)-1):
                url=url+post_result[i]+','
            else:
                url=url+post_result[i]      
        #print(url)            
    r_get = requests.get(url, params=payload_get, headers=header_get)
    
    ten_items=r_get.json()#type:dict 
    return ten_items

class Item:
    def __init__(self,name,typeLine,ilvl,league,sockets,price,properties,seller_name,date,whisper,identified,requirements,explicitMods,flavourText,status):
        self.name=name
        self.typeLine=typeLine
        self.ilvl=ilvl
        self.league=league
        self.sockets=sockets
        self.price=price
        self.properties=properties
        self.seller_name=seller_name
        self.date=date
        self.whisper=whisper
        self.identified=identified
        self.requirements=requirements
        self.explicitMods=explicitMods
        self.flavourText=flavourText
        self.status=status

def create_clipboard_Database(Database,Clipboard_base,start,end,datalist):
    for i in range(end-start):
        #print(start,"start","end",end)
        Item_base.insert(start+i,datalist[i])
        Clipboard_base.insert(start+i,create_clipboard_Item(datalist[i]))
        #print(start+i,datalist[i].seller_name)
        Database.insert(start+i,datalist[i])

        
def Final_Database(start,end,post_result,url,Clipboard_base,Database):    
    ten_items=get_request(start,end,post_result,url)
    Item_Result=create_Item(ten_items)
    #forz i in range(len(Result)):
    #    print(Result[i].name,Result[i].price)
    end=start+len(Item_Result)
    create_clipboard_Database(Database,Clipboard_base,start,end,Item_Result)
        
def Final_Part(url_get,post_result,Clipboard_base,Database):
    for i in range(12):#0~99
        #print('thread',index)
        threads.append(threading.Thread(target = Final_Database, args = ( (count+i*9),(count+(i+1)*9),post['result'],url_get,Clipboard_base,Database)))
        num=int((count/100)*12+i)
        #print("num",num)
        threads[num].start()
        time.sleep(0.05)
        
    for t in threads:
        t.join()

    
    
def Create_price_text(price_text):
    #print(count)
    #print("arisdadsfh",count*100,len(Database))
    for i in range(count,len(Database)):
        if(Database[i].typeLine==''):
            price_text.insert(i+3,'|'+("{0:^6d} | {1:^10s}{2:^14s} | {3:^16s} | {4:^15s} ({5:^6s}) in {6:^6s} ").format(i,Database[i].name,Database[i].typeLine,Database[i].price,Database[i].seller_name,Database[i].status,Database[i].league))
        else:
            price_text.insert(i+3,'|'+("{0:^6d} | {1:^10s}{2:^10s} | {3:^16s} | {4:^15s} ({5:^6s}) in {6:^6s} ").format(i,Database[i].name,Database[i].typeLine,Database[i].price,Database[i].seller_name,Database[i].status,Database[i].league))        
        if(i==9):
            ans=''
            for w in range(0,13):
                ans=ans+price_text[w]+'\n'           
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(win32clipboard.CF_UNICODETEXT, ans+'_'*130+'\n')
            win32clipboard.CloseClipboard()

    return price_text
#--------------------------------------------------------------------------------------------------------------
#Main function
        
        
STOP=0    
index=0    
count=0
begin=time.time()
# get clipboard data9
win32clipboard.OpenClipboard()
data = win32clipboard.GetClipboardData()
win32clipboard.CloseClipboard()
#print(data)vzq
#print(data)
data=data.replace('\r','')

affix=data.split('\n')
#print(affix)
url = 'https://web.poe.garena.tw/trade/search/%E6%8E%98%E7%8D%84%E8%81%AF%E7%9B%9F'
resp = fetch(url)  
url_post = 'https://web.poe.garena.tw/api/trade/search/%E6%8E%98%E7%8D%84%E8%81%AF%E7%9B%9F'



if not(os.path.isdir("C:\\"+"POE_Market")):
    os.makedirs("C:\\"+"POE_Market")

if(resp.status_code!=200):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText('無法連線至POE交易市集!')
    win32clipboard.CloseClipboard()
else:
    #POST    
    header_post={
    'Accept-Encoding':"gzip, deflate, br",
    'Accept-Language':"zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'Connection':"keep-alive",
    'Content-Type': "application/json",
    'Host': "web.poe.garena.tw",
    'Origin': "https://web.poe.garena.tew",
    'Referer': "https://web.poe.garena.tw/trade/search/%E6%8E%98%E7%8D%84%E8%81%AF%E7%9B%9F",
    'X-Requested-With': "XMLHttpRequest"
    }
  
    payload_post={"query":{"status":{"option":"online"},"name": affix[1],"type":affix[2],"stats":[{"type":"and","filters":[]}]},"sort":{"price":"asc"}}
    r_post = requests.post(url_post, data=json.dumps(payload_post), headers=header_post)
      
    #ID
    post=r_post.json()
    ID=post['id']
    
    
    #Item_amount
    start=r_post.text.find('"total":')
    end=r_post.text.find("}")
    item_amount=r_post.text[start+8:end]
    #print(item_amount)
    #At most 200 records
    
    
    #Get   
    header_get={
    'Accept': "*/*",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    'Connection': "keep-alive",
    'Host': "web.poe.garena.tw",
    'Referer': "https://web.poe.garena.tw/trade/search/%E6%8E%98%E7%8D%84%E8%81%AF%E7%9B%9F/"+ID,
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    'X-Requested-With': "XMLHttpRequest"
    }
    Database=[]
    Clipboard_base=[]
    Item_base=[]
    price_text=[]
    payload_get={"query":ID}
    url_get='https://web.poe.garena.tw/api/trade/fetch/'    
    
    threads = []
    
    common_price=[]
    price_counter=[]    
    price_index=0
    found=0
    for i in range(12):#0~99
        #print('thread',i)
        threads.append(threading.Thread(target = Final_Database, args = ( i*9,(i+1)*9,post['result'],url_get,Clipboard_base,Database)))
        threads[i].start()
        time.sleep(0.05)
        
    for t in threads:
        t.join()
    
    for i in range(len(Database)):
        if(i==0): 
            common_price.append(Database[i].price)
            price_counter.insert(price_index,1)
            price_index=price_index+1
        else:
            found=0
            for j in range(len(common_price)):
                if(Database[i].price==common_price[j]):
                    price_counter[j]=price_counter[j]+1
                    found=1
            if(found==0):
                common_price.append(Database[i].price)
                price_counter.insert(price_index,1)
                price_index=price_index+1
    
    #print(common_price)
    #print(price_counter.index(max(price_counter)))
    
    
    #for i in range(len(Database)):v
     #   print(i,Database[i].name)
    price_text.append('_'*130)
    price_text.append(("|{0:^2s} | {1:^30s} | {2:^35s} | {3:^30s} #最多人標註的價格(前100筆):{4:^10s} ".format('排序','商品名稱','價格','賣家名稱',common_price[price_counter.index(max(price_counter))]))+'\n')
    price_text.append('_'*130)    
    Create_price_text(price_text)
    
    #for i in range(len(price_text)):
    #    print(price_text[i])
    
    
    #eprint(price_text)
    end=time.time()
    
    #for i in range(100):
    #    print(i,Clipboard_base[i])
        
    print(end-begin)
#--------------------------------------------------------------------------------------------------------------
#Set up pyHook to listen to global keyboard input.    

# create a hook manager
hm = pyHook.HookManager()
hm.KeyDown = OnKeyboardEvent
#--------------------------------------------------------------------------------------------------------------
#Loop control for additional functions
while not STOP:
    if(STOP==1): print("I should STOP")
    # set the hook
    hm.HookKeyboard()
    pythoncom.PumpWaitingMessages()