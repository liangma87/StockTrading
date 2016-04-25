# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 10:44:11 2016

@author: evan87
"""

import pandas as pd
import pandas.io.data as web
import datetime
import time
import os
import json
from pandas import read_hdf

class lm_stock:
    
    '''A customer of ABC Bank with a checking account. Customers have the
       following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    '''
    
    def __init__(self):
        
        self.symbol = '^IXIC'
        
        self.start  = '1/1/1900'
        
        self.end    = '4/22/2015'
        
        self.dataFile = 'stock_data.h5s'
        
        self.dataPath = os.getcwd() + '/'
        
        
    def is_in_hdf5store(self):
        
        meta_data = self.__getMetaData__()
        
        if self.symbol in meta_data:            
            return True            
        else :
            return False 
                    
        

    def get_stock_data (self):

        try:            
            data = web.DataReader(self.symbol, data_source = 'yahoo', start=self.start,end=self.end)        
        except:    
            err_file = open('err.log','a')
            err_file.write("lm_stock::get_stock_data: Getting an error during web data fetch for stock %s\n" %self.symbol)
            err_file.close()
                         
            return None
            
        return data
        
    def get_local_stock_data (self):

        try:            
            meta_data = self.__getMetaData__()            
            if self.symbol in meta_data :                
                end_date = meta_data[self.symbol]                
            else :
                err_file = open('err.log','a')
                err_file.write("lm_stock::get_local_stock_data: stock is not present in local database!\n") 
                err_file.close()
                exit(0)
                
            saved_end_date = time.strptime(end_date, "%d/%m/%Y")
        
            new_end_date   = time.strptime(self.end, "%d/%m/%Y")
            
            if new_end_date > saved_end_date : 
                err_file = open('err.log','a')
                err_file.write("lm_stock::get_local_stock_data: stock info is not up2date in local database!\n")
                err_file.close()
            else :
                #read from hdf5           
                data =read_hdf(self.dataFile, self.symbol)
                        
        except:
            err_file = open('err.log','a')
            err_file.write("lm_stock::get_stock_data: Getting an error during local data fetch for stock %s\n" %self.symbol)   
            err_file.close()
            return None
            
        return data
    
    def create_hdf5store (self,data):
    
        #TODO if the store already exists, don't flush it
        #and print out a warning
        
        print "Creating %s @ %s for stock %s" %(self.dataFile ,self.dataPath,self.symbol) 
        
        h5s = pd.HDFStore(self.dataFile)
        
        #h5s.put(self.symbol,data)
        #h5s[self.symbol] = data
        
        h5s.append(self.symbol,data)
        
        #let's put the meta data inside json file

        #print h5s
        
        file_name = self.dataFile.split('.')[0] + '.json'

        print "JSON file name is ", file_name
        
        #meta data records the last date when stock in hdf5store gets updated
        
        meta_data = self.__getMetaData__()
                        
        meta_file = open(self.dataPath+file_name, 'w')
            
        meta_data[self.symbol] = self.end
        
        json.dump(meta_data,meta_file)
        
        meta_file.close()
        
        h5s.close()
        
        
    def update_hdf5store(self):
        
        #TODO what if error happends, just log it and continue...    
        meta_data = self.__getMetaData__()
        
        last_end_date = meta_data[self.symbol]
        
        today = self.__getTodayDate__()
        
        saved_date = time.strptime(last_end_date, "%m/%d/%Y")
        
        new_date   = time.strptime(today, "%m/%d/%Y")
        
        if new_date > saved_date:
            
            print "Updating %s @ %s for stock %s" %(self.dataFile ,self.dataPath,self.symbol)
            
            data = web.DataReader(self.symbol, data_source = 'yahoo', start=last_end_date,end=today)
            #first row is a duplicate
            h5s = pd.HDFStore(self.dataFile)
            
            h5s.append(self.symbol,data[1:])
            
            file_name = self.dataFile.split('.')[0] + '.json'
            
            meta_file = open(self.dataPath+file_name, 'w')
            
            meta_data[self.symbol] = today
            
            json.dump(meta_data,meta_file)
            
            meta_file.close()
            
            h5s.close()
                        
#private methods
            
    def __getTodayDate__(self):
        
        date=str(datetime.date.today())
        
        date = date.split('-')
        
        date = date[1] + '/'+date[2] + '/'+date[0]
        
        return date
        
        
    def __getMetaData__(self):
        
        meta_data = dict()
        
        file_name = self.dataFile.split('.')[0] + '.json'
        
        if os.path.exists(self.dataPath+file_name):
            
            meta_file = open(self.dataPath+file_name, 'r')
                        
            meta_data = json.loads(meta_file.read())
            
            meta_file.close()
        
        return meta_data
        
        
        
        
    
    
    

