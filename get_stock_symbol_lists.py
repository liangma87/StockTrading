# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 23:48:41 2016

@author: evan87
"""

import finsymbols
import json
import sys

if len(sys.argv) == 1:
    exchange = 'all'
    print "Generating JSON file for nyse, nasdaq, amex, sp500"
else:
    exchange = str(sys.argv[1])
    
    if exchange == '-h' or exchange =='-help':
        print "***************Usage*****************"
        print "Info: python %s -h for help info" %str(sys.argv[0])
        print "Info: python %s to dump all stock list including nyse, nasdaq, amex and sp500 " %str(sys.argv[0])
        print "Info: python %s -[nyse|nasdaq|amex|sp500] to dump selected stock list " %str(sys.argv[0])
        print "***************Usage*****************"    
        exit(0)
    
    elif exchange == '-nyse' or exchange == '-nasdaq' or exchange == '-amex' or exchange == '-sp500':
        print "Generating JSON file for %s" %exchange
    else :
        print "Error : %s is not a supported command " %str(sys.argv[1]) 
        print "Error : use -h to see all supported commands"
        exit(0)

        
if exchange == 'all' or exchange == '-nyse':
    nyse = finsymbols.get_nyse_symbols()
    nyse_json = open('nyse.json', 'w')
    nyse_json.write(json.dumps(nyse))
    
if exchange == 'all' or exchange == '-nasdaq':
    nasdaq = finsymbols.get_nasdaq_symbols()
    nasdaq_json = open('nasdaq.json', 'w')
    nasdaq_json.write(json.dumps(nyse))

if exchange == 'all' or exchange == '-amex':
    amex = finsymbols.get_amex_symbols()
    amex_json = open('amex.json', 'w')
    amex_json.write(json.dumps(nyse))

if exchange == 'all' or exchange == '-sp500':
    sp500 = finsymbols.get_sp500_symbols()
    sp500_json = open('sp500.json', 'w')
    sp500_json.write(json.dumps(sp500))






