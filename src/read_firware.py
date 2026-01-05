import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import serial as sr
import re

class reading:
    
    def __init__(self, serial_conn):
        self.serial = serial_conn
        self.datafr = pd.DataFrame(columns = ["rms_A", "raw_line","W", "timestamp"])
        
        self.rms_value = None
        self.w_value = None
    
    def read_data(self):
        if self.serial.is_open:
            #processing and adding the dataframe
            line = self.serial.readline().decode(errors = 'ignore').strip(); 
        
        if not line:
            return None
        
        # Extracting data
        I_corresp = re.search(r"rms_A:\s*([\d\.]+)", line)
        W_corresp = re.search(r"W:\s*([\d\.]+)", line)
        
        # Processing the RMS
        rms_value = None
        if I_corresp:
            try:
                rms_value = float(I_corresp.group(1))
            except ValueError:
                rms_value = None
        
        # Processing W values
        w_value = None
        if W_corresp:
            try:
                w_value = float(W_corresp.group(1))
            except ValueError:
                w_value = None
        
        # Building a new line with dictionaries
        new_row = {
            "rms_A": rms_value,
            "raw_line": line,
            "W": w_value,
            "timestamp": pd.Timestamp.now()
        }
        
        # Adding in DataFrame
        self.datafr.loc[len(self.datafr)] = new_row
        
        return {"rms_A": rms_value, "W": w_value, "raw_line": line, "timestamp": pd.Timestamp.now()}
    
    def get_dataframe(self):
        return self.datafr

    def visualization_plot(self):

        if self.datafr.empty:
            print("Dataframe is empty")
            return
        
        if "timestamp" in self.datafr.columns:
            x = self.datafr["timestamp"]
        else:
            x = self.datafr.index
            
        y = self.datafr["rms_A"];
        z = self.datafr["W"]
        
        print("Reading plot")
        
        plt.subplot(1,2,1)
        plt.plot(x, y, marker = "o");
        plt.title("Current over time")
        plt.xlabel("time")
        plt.ylabel("Current")
        
        plt.subplot(1,2,2)
        plt.plot(x, z, marker = "x");
        plt.title("Power over time")
        plt.xlabel("time")
        plt.ylabel("Power")
        plt.show()
