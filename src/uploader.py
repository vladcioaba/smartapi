import csv
from datetime import datetime
import re;
import sys

class StockPriceReader:

    price_regex = r"(^[0-9]+\.[0-9]{2}$)"
    date_format = f"%d-%m-%Y"

    '''
    Function needed to validate the price, will return error message if the price is not
    in the correct format.
    '''
    def _validatePrice(self, price_val):
        # price not valid
        if price_val=="":
            return "Price is empty!"
        if re.findall(self.price_regex, price_val)[0] == "":
            return "Price not in format XX.XX!"
        if price_val:
            return ""
    
    '''
    Function needed to validate the symbol, will return error message if the symbol is not
    in the correct format.
    '''
    def _validateSymbol(self, first_symbol_val, symbol):
        if (symbol == ""):
            return "Symbol is empty!"
        if (first_symbol_val != "" and symbol != first_symbol_val):
            return "Symbol is different!"
        elif len(symbol) < 2 and len(symbol) > 4:
            return "Symbol naming error!"
        else:
            return ""
        
    '''
    Function needed to validate the date string, will return error message if the date is not
    in the correct format.
    '''
    def _validateDate(self, value_date, date_format):
        try:
            d = datetime.strptime(value_date, date_format)
            return ["", d]
        except ValueError as ex:
            print(f"_validateDate {ex}", file=sys.stdout)
            return ["Date format should be DD-MM-YYYY", None]
        
    '''
    Function responsible to parse the input file and validate the csv
    Will check that: 
     - all the values at 0 will be the same and not empty and at least 2 characters
     - the value at 1st position is a date object DD-MM-YYYY and not empty
     - the value at 2nd position is a price with 2 fractional digits and at least 1 integer digit
     
    Returs a tuple where 0 is a string success / error and the second part is a list of objects for success or
    a list of error objects. 
    '''
    def read(self, data):
        print(f"StockPriceReader::read data_len {data}", file=sys.stdout)
        
        list_prices = []
        list_errors = []

        reader = csv.reader(data, delimiter=',')
        index = -1

        first_symbol_val = ""
        for row in reader:
            index += 1
            if len(row) == 3:
                symbol = row[0]
                price_date = row[1]
                price_val = row[2]
                
                # empty or different symbol name
                symbol_error = self._validateSymbol(first_symbol_val, symbol)
                if symbol_error != "":
                    list_errors.append({"index":index, "error":symbol_error})
                    continue
            
                if (first_symbol_val == ""):
                    first_symbol_val = symbol
                
                # date time not valid or empty
                date_obj = self._validateDate(price_date, self.date_format)
                if date_obj[0] != "":
                    list_errors.append({"index":index, "error":date_obj[0]})
                    continue

                # price not valid
                price_error = self._validatePrice(price_val)
                if price_error != "":
                    list_errors.append({"index":index, "error":price_error})
                    continue
                
                # if everything was all right append
                list_prices.append([symbol, date_obj[1], float(price_val)])
                    
            else:
                list_errors.append({"index":index, "error":"Format incorrect!"})
        
        return {"rows":list_prices, "errors":list_errors}

    
    
