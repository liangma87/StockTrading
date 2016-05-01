# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 13:37:26 2016

@author: evan87
"""

from stock_data import lm_stock
import os
import json
from pandas import read_hdf
import sys

def get_stock_ret():
    
    symbol = raw_input('input the stock symbol: ')
    
    start = raw_input('input the start date(month/day/year): ')
    
    end   = raw_input('input the end date(month/day/year): ')
     
    stock = lm_stock()
    
    stock.symbol = symbol
    
    ret = stock.get_stock_return(start,end)
    
    print "stock %s return is %f " %(symbol,ret[0])
    
    print "start price %f end price %f" %(ret[1],ret[2])

def stock_db_info():
    
    symbol = raw_input('input the stock symbol: ')
    
    stock = lm_stock()
    
    stock.symbol = symbol
    
    stock.print_stock_statistics()
    
def rank_stock ():
    
    start = raw_input('input the start date(month/day/year): ')
    
    end   = raw_input('input the end date(month/day/year): ')
    
    stocks = get_stock_list()
    
    count = len(stocks)
    
    print "Analyzing on %d stocks now...." %(count)
    
    rets = list() 
    
    count = 0
    
    for item in stocks:
    
        count += 1
        
        stock = lm_stock()
    
        stock.symbol = item['symbol']  
    
        if stock.is_in_hdf5store() == True : 
            
            ret = stock.get_stock_return(start,end)
            
            rets.append((stock.symbol,ret[0]))
            
        if count % 100 == 0 :
             print " %d stocks have been analyzed" %(count)
            
    
    rets.sort(key=lambda tup:tup[1],reverse=True)
    
    count =0;
    
    f = open('rank','w') 
    for ret in rets:
        
        if count <200 :
            print "stock %s return %f" %(ret[0],ret[1]) 
            
        f.write("stock %s return %f \n" %(ret[0],ret[1]) )
        
        count += 1
    
    f.close()
            
        
def get_stock_list(gen_file=0):
            
    stocks = list()
    symbols = set()
    
    if os.path.exists('nasdaq.json'):
    
        nasdaq_file =  open('nasdaq.json', 'r')
    
        nasdaq_json = json.loads(nasdaq_file.read())
            
        nasdaq_file.close()
    
    for stock in nasdaq_json:
        
        if stock['symbol'] in symbols:
            continue
        else:
            symbols.add(stock['symbol'])
            stocks.append(stock)
        
            
    if os.path.exists('nyse.json'):
    
        nyse_file =  open('nyse.json', 'r')
    
        nyse_json = json.loads(nyse_file.read())
            
        nyse_file.close()
        
    for stock in nyse_json:
        
        if stock['symbol'] in symbols:
            continue
        else:
            symbols.add(stock['symbol'])
            stocks.append(stock)
        
    if os.path.exists('amex.json'):
    
        amex_file =  open('amex.json', 'r')
    
        amex_json = json.loads(amex_file.read())
            
        amex_file.close()
        
            
    for stock in amex_json:
        
        if stock['symbol'] in symbols:
            continue
        else:
            symbols.add(stock['symbol'])
            stocks.append(stock)
        
    
    if gen_file == 1:
    
        f = open('stock_list','w')

        for stock in stocks:
            
            f.write(stock['symbol']+'\n')
    
    return stocks

def create_or_update_stock_db(debug=0) :
    
    #if os.path.exists('sp500.json'):
    
        #sp500_file =  open('sp500.json', 'r')
    
        #sp500_json = json.loads(sp500_file.read())
            
        #sp500_file.close()
        
    stocks = get_stock_list()

    count = 0;
                        
    for item in stocks:
    
        stock = lm_stock()
    
        stock.symbol = item['symbol']  
    
        if stock.is_in_hdf5store() == True : 
            
            stock.update_hdf5store()
        
        else :
            
            data = stock.get_stock_data()

            if data is not None :
                
                stock.create_hdf5store(data)
        
        print "Finished dataset for stock %s" %stock.symbol
    
        count = count + 1
    
        if count == 5 and debug==1 :
            break;
        

if __name__ == "__main__":
    
    if len(sys.argv) < 2  or len(sys.argv) > 2:        
        print "***************Usage*****************"
        print "Info: Press -h for help info"
        print "***************Usage*****************"    
        exit(0)
    else :
        para = str(sys.argv[1])
        
    if para == '-h' or para == '-help':
        print "***************Usage*****************"
        print "Info: python %s -h for help info" %str(sys.argv[0])
        print "Info: python %s -clean to remove stock_data_meta.json, stock_data.h5s " %str(sys.argv[0])
        print "Info: python %s -run to update or create stock database " %str(sys.argv[0])
        print "Info: python %s -ask to choose what to run " %str(sys.argv[0])
        print "Info: python %s -debug to run a debug test case " %str(sys.argv[0])
        print "***************Usage*****************"    
        exit(0)
        
    if para == '-clean':
        decision = raw_input('Are you sure you want to clean the meta file and database??<y/n>:')
        if decision == 'y' or decision =='yes':
            if os.path.exists('stock_data.json'):
                os.remove('stock_data.json')
            if os.path.exists('stock_data.h5s'):
                os.remove('stock_data.h5s')
            if os.path.exists('err.log'):
                os.remove('err.log')
        else :
            exit(0)
            
    
    if para == '-run':
        create_or_update_stock_db(0)
        
    if para == '-ask':
        
        user_ask = raw_input('What do you want to know? (rank/stock_db_info/stock_list/get_stock_ret):')
        
        if user_ask == 'rank' or user_ask == 'r':
            rank_stock ()
            
        if user_ask == 'stock_db_info' or user_ask == 'sdb':
            stock_db_info()
            
        if user_ask == 'stock_list' or user_ask == 'sl':
            get_stock_list(gen_file=1)
            
        if user_ask == 'get_stock_re' or user_ask == 'gsr':            
            get_stock_ret()

    if para == '-debug':
        create_or_update_stock_db(1)
        
        if os.path.exists('sp500.json'):
    
            sp500_file =  open('sp500.json', 'r')
    
            sp500_json = json.loads(sp500_file.read())
            
            sp500_file.close()

            count = 0;

        for item in sp500_json:
    
            data =read_hdf('stock_data.h5s', item['symbol'])
    
            print "stock %s data", item['symbol']
    
    
            print data.info()
    
            count = count + 1
    
            if count == 5 :
                break;