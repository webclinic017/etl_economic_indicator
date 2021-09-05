#%% Import Module
import warnings
warnings.filterwarnings('ignore')
import pandas as pd
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import urllib.request
from bs4 import BeautifulSoup
import numpy as np
import getpass
import datetime
import lxml
import sqlserverconnection
    
#%%

class class_get_economic_data_from_investing_com():
    
    CONSTANTS_STR_INVESTING_COM_URL = 'https://www.investing.com/economic-calendar/'
    CONSTANTS_STR_CHROME_DRIVER_FILE_PATH = './chromedriver/chromedriver.exe'
    
    def __init__(self,
                 str_start_date = None,
                 str_end_date = None):
        
        self.str_start_date = str_start_date
        self.str_end_date = str_end_date
    
    ######################################################################
    
    def func_df_get_economic_data(self,
                                  bool_upload_data_to_sqlserver_True_or_False = False,
                                  bool_sqlserver_upload_append_or_replace = 'append'):
        

        
        df_economic_data = pd.DataFrame([])
        
        list_date = pd.date_range(start = self.str_start_date, 
                                    end = self.str_end_date,
                                    freq='M'
                                    ).date

        for str_last_month_date in list_date:
            
            str_start_month_date = pd.to_datetime(str_last_month_date.strftime('%Y-%m-01')).strftime('%m/%d/%Y')
            str_last_month_date = pd.to_datetime(str_last_month_date).strftime('%m/%d/%Y')
            
            print(str_start_month_date)
            print(str_last_month_date)
            
            df_data = self._func_df_extract_economic_data_from_investing_com(str_start_date = str_start_month_date,
                                                                             str_end_date = str_last_month_date)
            
            df_data = self._func_df_clean_data(df_data = df_data)
            
            df_economic_data = df_economic_data.append(df_data, ignore_index = True)
             
            if bool_upload_data_to_sqlserver_True_or_False == True:
                
                self._func_upload_data_to_sql_server(df_data = df_economic_data,
                                                     bool_sqlserver_upload_append_or_replace = bool_sqlserver_upload_append_or_replace)
        
        return df_economic_data
    
    ######################################################################
    
    def _func_upload_data_to_sql_server(self,
                                        df_data = None,
                                        bool_sqlserver_upload_append_or_replace = 'append'):
        
        obj_sql_connection = sqlserverconnection.CONNECT_TO_SQL_SERVER(_str_driver = "SQL Server Native Client 11.0",
                                                _str_server = "LAPTOP-9O71KA1L",
                                                _str_database = 'db_economic_data_indicators',
                                                _str_trusted_connection = 'yes',
                                                str_download_or_upload = 'upload')

        df_data.to_sql('tbl_economic_data_indicator_investing_com', 
                        schema='dbo', 
                        con = obj_sql_connection, 
                        if_exists = bool_sqlserver_upload_append_or_replace,
                        index= False)
        
        return print('The economic data is now uploaded to SQL Server database')
    
    ######################################################################

    def _func_df_extract_economic_data_from_investing_com(self,
                                                       str_start_date: (str) = None,
                                                        str_end_date: (str) = None):
        
        
    
        obj_chrome_driver = webdriver.Chrome(executable_path = self.CONSTANTS_STR_CHROME_DRIVER_FILE_PATH)

        
        
        #_username = getpass.getuser()
        
        obj_chrome_driver.get(self.CONSTANTS_STR_INVESTING_COM_URL)
        time.sleep(10)
        
        
        def _func_remove_popup():
            actions = ActionChains(obj_chrome_driver)
            actions.send_keys(Keys.ESCAPE).perform()
        
    
        try:
            obj_chrome_driver.find_element_by_id('datePickerToggleBtn').click()
            time.sleep(3)
        except Exception:
            time.sleep(3) 
            _func_remove_popup()
            time.sleep(3) 
            obj_chrome_driver.find_element_by_id('datePickerToggleBtn').click()
            time.sleep(3)
        
        

        
        try:
            startDate_html_link = obj_chrome_driver.find_element_by_id('startDate')
            time.sleep(3)
        except Exception:
            _func_remove_popup()
            time.sleep(3) 
            startDate_html_link = obj_chrome_driver.find_element_by_id('startDate')
            time.sleep(3)    
        
        
        for i in range(10):
            startDate_html_link.send_keys(Keys.BACKSPACE)
        
        
        startDate_html_link.send_keys(str_start_date)
        endDate_html_link = obj_chrome_driver.find_element_by_id('endDate')
        
        for i in range(10):
            endDate_html_link.send_keys(Keys.BACKSPACE)
            
        
        endDate_html_link.send_keys(str_end_date)
        
        
        try:
            obj_chrome_driver.find_element_by_id('applyBtn').click()
            time.sleep(3)
        except Exception:
            _func_remove_popup()
            time.sleep(3) 
            obj_chrome_driver.find_element_by_id('applyBtn').click()
            time.sleep(3)      

        try:
            obj_chrome_driver.find_element_by_id('filterStateAnchor').click()
            time.sleep(3)
        except Exception:
            _func_remove_popup()
            time.sleep(3) 
            obj_chrome_driver.find_element_by_id('filterStateAnchor').click()
            time.sleep(3)  
            
        try:
            obj_chrome_driver.find_element_by_link_text("Select All").click()
            time.sleep(3)
        except Exception:
            _func_remove_popup()
            time.sleep(3) 
            obj_chrome_driver.find_element_by_link_text("Select All").click()
            time.sleep(3)  
            
        
        try:
            obj_chrome_driver.find_element_by_id("ecSubmitButton").click()
            time.sleep(3)
        except Exception:
            _func_remove_popup()
            time.sleep(3) 
            obj_chrome_driver.find_element_by_id("ecSubmitButton").click()
            time.sleep(3) 
            
        actions = ActionChains(obj_chrome_driver)
        _last_date_load_finish_marker = pd.to_datetime(str_end_date).date().strftime("%B %d, %Y")
        
        html=obj_chrome_driver.page_source
        

        _counter_break = 0
        while html.find(_last_date_load_finish_marker) == -1:
            print(f'Loading Bottom Page until {_last_date_load_finish_marker} shows up')

            
            actions.send_keys(Keys.END).perform()
            time.sleep(3)
            html=obj_chrome_driver.page_source
            _counter_break += 1
            print(_counter_break)
            if _counter_break == 10:
                break
        
        
        
        table=pd.read_html(html)
        
        df_economic_calendar_raw = pd.DataFrame(table[2])
        
        df_economic_calendar_raw['TimeZone'] = obj_chrome_driver.find_element_by_id('timeZoneGmtOffsetFormatted').text
        
        obj_chrome_driver.quit()
        
        
        
        return df_economic_calendar_raw
    
    ######################################################################
    
    def _func_float_extract_figures_and_units(self,
                                  x: (str) = None ):
        
        if str(x) != 'nan':
            if not str(x[-1]).isnumeric():
                _figure = x[:-1]
                _figure = str(_figure).replace(',','')
                _unit = x[-1]
                
                if _unit == '%':
                    _figure = float(_figure) /100
                elif _unit == 'K':
                    _figure = float(_figure) * 1_000
                elif _unit == 'M':
                    _figure = float(_figure) * 1_000_000
                elif _unit == 'B':
                    _figure = float(_figure) * 1_000_000_000
                elif _unit == 'T':
                    _figure = float(_figure) * 1_000_000_000_000
                    
                return _figure, _unit
            else: 
                x = str(x).replace(',','')
                return x, ""
        return np.nan , ""
    
    ######################################################################
    
    def _func_str_extract_month_from_economic_event(self,
                                                    x: (str) = None):
        _list_of_months = ['(Jan)','(Feb)','(Mar)','(Apr)','(May)','(Jun)','(Jul)','(Aug)','(Sep)','(Aug)','(Nov)','(Dec)','(Q1)','(Q2)','(Q3)','(Q4)']
        
        if str(x) != 'nan':
            for _month in _list_of_months:
                if x.find(_month) >= 0:
                    x = x.replace(_month, "")
                    break
                _month = '' 
        return x, _month
    
    ######################################################################
    
    def _func_str_extract_frequency_from_economic_event(self,
                                              x: (str) = None):
        _list_of_months = ['(MoM)','(QoQ)','(YoY)']
        
        if str(x) != 'nan':
            for _month in _list_of_months:
                if x.find(_month) >= 0:
                    x = x.replace(_month, "")
                    break
                _month = '' 
        return x, _month
    
    ######################################################################
    
    def _func_str_identify_european_country(self,
                                        _event: (str) =  None):
        
        if 'Austria' in str(_event):
            _country = 'Austria'
    
        elif 'Austrian' in str(_event):
            _country = 'Austria'
    
        elif 'Belgian' in str(_event):
            _country = 'Belgium'
    
        elif 'Belgium' in str(_event):
            _country = 'Belgium'
    
        elif 'Dutch' in str(_event):
            _country = 'Netherland'
    
        elif 'Estonian' in str(_event):
            _country = 'Estonia'
    
        elif 'Finnish' in str(_event):
            _country = 'Finland'
    
        elif 'France' in str(_event):
            _country = 'France'
    
        elif 'French' in str(_event):
            _country = 'France'
    
        elif 'German' in str(_event):
            _country = 'Germany'
    
        elif 'Greece' in str(_event):
            _country = 'Greece'
    
        elif 'Greek' in str(_event):
            _country = 'Greece'
    
        elif 'Irish' in str(_event):
            _country = 'Ireland'
    
        elif 'Italian' in str(_event):
            _country = 'Italy'
    
        elif 'Latvian' in str(_event):
            _country = 'Latvia'
    
        elif 'Lithuania' in str(_event):
            _country = 'Lithuania'
    
        elif 'Portugal' in str(_event):
            _country = 'Portugal'
    
        elif 'Portuguese' in str(_event):
            _country = 'Portugal'
    
        elif 'Slovak' in str(_event):
            _country = 'Slovak'
    
        elif 'Spanish' in str(_event):
            _country = 'Spain'
            
        else:
            _country = np.nan
            
        return _country
    
    
    
    def _func_df_clean_data(self, df_data = None):
        #%% Event, Period & Frequency
        df_data['Reporting Period'] = df_data['Event'].apply(lambda x: self._func_str_extract_month_from_economic_event(str(x))[1])
        df_data['Event'] = df_data['Event'].apply(lambda x: self._func_str_extract_month_from_economic_event(str(x))[0])
        df_data['Reporting Frequency'] = df_data['Event'].apply(lambda x: self._func_str_extract_frequency_from_economic_event(str(x))[1])
        df_data['Event'] = df_data['Event'].apply(lambda x: self._func_str_extract_frequency_from_economic_event(str(x))[0])

        #%% Remove white spaces
        #Remove all whitespace
        for _col_names in df_data.columns:
            df_data[_col_names] = df_data[_col_names].apply(lambda x: str(x).strip())
        
        #%% Replace nan with NA
        df_data = df_data.replace('nan',np.nan)
        
        
        #%% Holiday
        #Create new column to identify Holiday dates
        df_data['Holiday'] = np.where(df_data['Imp.'] == 'Holiday',
                                    True,
                                    False)
        #%%
        df_data['Imp.'] = np.where(df_data['Imp.'] == 'Holiday',
                                    np.nan,
                                    df_data['Imp.'])
        
        #%% Remove Unamed Columns
        #Remove Unnamed columns
        df_data = df_data.drop(labels = df_data.filter(regex = 'Unnamed').columns, axis = 1)
        
        #%%
        #Replace values of All Day time to 00:00
        df_data['Time'] = np.where((df_data['Time'] == 'All Day') | (df_data['Time'] == 'Tentative'),
                                '00:00',
                                df_data['Time'])
        #%% Date
        #Create a new column Date based of the values from the Imp
        df_data['Date'] = np.where((df_data['Imp.'] != 'Holiday') & (~pd.isna(df_data['Imp.'] )),
                                df_data['Imp.'],
                                np.nan)
        
        df_data['Date'] = df_data['Date'].fillna(method = 'ffill')
        
        
        
        #%%
        #Remove all dates row
        print(df_data)
        _condition = pd.isna(df_data['Imp.'])
        print(_condition)
        df_data = df_data[_condition]
        
        #%% Clear Actual Forecast & Previous columns of Holiday values
        for _colname in ['Actual','Forecast','Previous']:
            df_data[_colname] = np.where(df_data['Holiday'] == True,
                                        np.nan,
                                        df_data[_colname])
            
        #%% Extract Unit Actual Previous and Forecast Values
        #Extract unit
        df_data['Unit'] = df_data['Actual'].apply(lambda x: self._func_float_extract_figures_and_units(str(x))[1])
        df_data['Actual'] =  df_data['Actual'].apply(lambda x: self._func_float_extract_figures_and_units(str(x))[0])
        df_data['Previous'] =  df_data['Previous'].apply(lambda x: self._func_float_extract_figures_and_units(str(x))[0])
        df_data['Forecast'] =  df_data['Forecast'].apply(lambda x: self._func_float_extract_figures_and_units(str(x))[0])
        
        
        #%% CHnage data type from string to floating point 
        
        df_data['Actual'] =  df_data['Actual'].astype('float64')
        df_data['Previous'] =  df_data['Previous'].astype('float64')
        df_data['Forecast'] =  df_data['Forecast'].astype('float64')
        
        
        #%% Remove Imp column
        
        del df_data['Imp.']
        
        
        #%% Split the date from the day
        
        df_data['Date'] = df_data['Date'].apply(lambda x: pd.to_datetime(str(x).split(sep = ' ', maxsplit = 1)[1]).strftime('%Y-%m-%d') ).astype('datetime64[ns]').dt.date
        
        
        #%% Remove parenthesis from frequency and reporting period
        
        df_data['Reporting Period'] = df_data['Reporting Period'].str.replace('(','').str.replace(')','')
        df_data['Reporting Frequency'] = df_data['Reporting Frequency'].str.replace('(','').str.replace(')','')
        
        
        
        #%% European country
        
        df_data['EuropeanCountry'] = df_data['Event'].apply(lambda x: self._func_str_identify_european_country(x))
        
        #%% Rename column in pandas
        df_data.rename(columns = {'Cur.':'Cur'}, inplace = True)
            
        #%%
        
        df_data = df_data[[ 'Date','Time', 'Cur', 'Event', 'Actual', 'Forecast', 'Previous','Unit','Reporting Period', 'Reporting Frequency', 'Holiday','TimeZone','EuropeanCountry']]
        
        #%% Function return
        
        return df_data

#%% Save Output.csv

if __name__ == '__main__':    
    #Earliest data available is 1/1/1970
    str_date_filter_from = '1/1/1970'
    str_date_filter_to = '9/6/2021'
    
    ged = class_get_economic_data_from_investing_com(   str_start_date = str_date_filter_from,
                                                        str_end_date = str_date_filter_to
                                                    )
    
    df_economic_data = ged.func_df_get_economic_data(bool_upload_data_to_sqlserver_True_or_False = True,
                                                     bool_sqlserver_upload_append_or_replace = 'append')
    


