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


def create_or_update_stock_db(debug=0) :
    
    if os.path.exists('sp500.json'):
    
        sp500_file =  open('sp500.json', 'r')
    
        sp500_json = json.loads(sp500_file.read())
            
        sp500_file.close()

    count = 0;
    
    for item in sp500_json:
    
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