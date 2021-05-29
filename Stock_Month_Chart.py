import matplotlib.pyplot as plt
import numpy as np
import urllib.request
import json
from datetime import datetime

def get_stock_M_record(url):
    responce = urllib.request.urlopen(url)
    ele_json = json.loads(responce.read())
    return ele_json

def reptile_stock_one_month(date,stock_num):
    dict1 = get_stock_M_record('https://www.twse.com.tw/exchangeReport/STOCK_DAY?date='+ date + '&stockNo=' + stock_num)
    length = len(dict1['data'])
    date  = []
    end_price = []
    amount = []

    for i in range(length) :
        date.append(dict1['data'][i][0].split('/')[2])
        end_price.append(float(dict1['data'][i][6]))
        amount.append(int(dict1['data'][i][1].replace(",","")))

    title_name = dict1['title'].replace(" ","")
    stock_chart(date,end_price,amount,title_name)


def stock_chart(x_axis,y_axis,y_axis2,stock_info) :
    # 資料
    max_value = np.max(y_axis)
    min_value = np.min(y_axis)
    x_max_value = y_axis.index(max_value)
    x_min_value = y_axis.index(min_value)
    average_value = round(np.average(y_axis),2)
    show_max = str(max_value)
    show_min = str(min_value)
    show_avg = str(average_value)

    # 軸 標題 字體   設定
    fig,ax2 = plt.subplots()
    #plt.figure("一週股價變化")
    #plt.xticks(rotation = '-5')
    plt.title(stock_info)
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    # 具有共同 X 軸但不同 Y 軸的圖使用 twinx()
    ax1 = ax2.twinx()

    # 子圖1
    ax1.set_ylabel('成交股數', color='tab:green')   
    ax1.tick_params(axis='y', labelcolor='tab:green')
    ax1.bar(x_axis,y_axis2,0.2,color = 'yellow',alpha=0.3)

    # 子圖2
    ax2.set_ylabel('股價', color='tab:blue')
    ax2.tick_params(axis='y', labelcolor='tab:blue')
    ax2.plot(x_axis,y_axis,'-',color = 'gray',alpha=1)
    ax2.plot(x_max_value,max_value,'ko',color='red',alpha=1)
    ax2.plot(x_min_value,min_value,'ko',color='blue',alpha=1)
    ax2.axhline(y=average_value, color="gray",linestyle= '--',alpha=1)
    ax2.annotate(('  '+ show_max),(x_max_value,max_value))
    ax2.annotate(('  '+ show_min),(x_min_value,min_value))
    ax2.annotate((show_avg),(0,average_value))

    length = len(x_axis)
    x = np.linspace(1,length,length)
    #趨勢線圖
    trend_line = []
    coefficients = np.polyfit(x,y_axis,1)
    #formula = np.poly1d(coefficients)
    for i in range(length) :
        trend_line.append(coefficients[0]*x[i] + coefficients[1])
    
    ax2.plot(x_axis,trend_line,color = 'pink',linestyle= 'dotted',alpha=1)

    #調整 存圖 或是 顯示圖
    fig.tight_layout()
    #plt.savefig('./Stock_M_graph.png')
    plt.show()

if __name__ == "__main__":
   now = datetime.now()
   date = now.strftime("%Y%m%d")
   print("請輸入股票代號:")
   stock_num = input()
   reptile_stock_one_month(date,stock_num)