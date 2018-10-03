# POE-Market
利用python 實作 web crawling獲取POE網站資料，並實作各項功能統計呈現

#請勿將本軟體用作非法用途，版權皆非本人所有，請注意使用
#使用AutoHotKey(AHK)自動執行程式並呈現結果，使用前請自行注意可能後果(如:被ban等等)
#程式會記錄鍵盤key_in，但並沒有後臺紀錄，原始碼一併附上，可自行查看
#可利用pyinstaller 將.py檔轉成.exe執行

POE_Market 使用python 實做multi thread Web Crawling，由POE交易市集自動獲取物品素質。

實作多種功能，利用AHK自動執行並將成果呈現於ToolTip上，省去使用者上網查詢的時間，快速比價。

#目前僅支援Legendary Items的查詢，主因是想不到其他Item的查詢方式，有想法可來訊討論

以下為簡單Demo影片:
https://www.youtube.com/watch?v=dvusfx0OPwA&t=4s

使用步驟:
1.  請將POE_Market_New.exe放置於C槽中
2.  安裝AutoHotKey，並以系統管理員權限執行 Poe_Market_New.ahk
3.  可以開始測試囉!

實作功能:
輸入
1.  ctrl+C:必要的首先動作，獲取裝備的前100筆資訊(根據價格由低到高)
2.  上、下:列出上10筆、下10筆資料
3.  0~9(非Numpad上的):觀看當前10筆的指定物品素質
4.  D:與自己的物品素質互相比較
5.  A:複製賣家密語
6.  Z:獲取下100筆物品資訊(請勿在短時間內連續按Z，將會被網路Autoban一小段時間)
7.  E:關閉查詢(查詢結束時請記得關閉)
8.  滑鼠左鍵+R:重新讀取.ahk檔(若遭遇腳本不正常顯示時可使用)

TODO:
1.  支援其他查價方式(如descending、by health...)
2.  將可查詢之物品數量提高到200以上(每次Post Request只能獲得200筆)
3.  支援Non-Legendary Items的查詢



