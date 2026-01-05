from read_firware import *

import numpy as np
import matplotlib.pyplot as plt     #Visualization

from sklearn.neural_network import MLPRegressor         #Perceptron function
from sklearn.model_selection import train_test_split        #training and test sample
from sklearn.metrics import *
from sklearn.preprocessing import StandardScaler        # Normalization

class regression:

    def __init__(self,datafr):
        self.datafr = datafr;
        self.residuo = 0;
        self.pred_regr = None
        self.rsme_regr = None
        
        if self.datafr is None:
            raise ValueError("Where is the dataframe?")
        
        #Treating problematic collumns
        self.datafr = datafr.drop(columns=["raw_line"], errors="ignore")

        self.X = self.datafr["timestamp"].values.reshape(-1,1)      ##getting timestamp and converting to 2D
        self.y = self.datafr["W"].values        ## Power prediction
        
        #Transforming calendar data to seconds
        x_time = self.datafr["timestamp"].astype("int64") / 1e9
        self.X = x_time.values.reshape(-1,1)
        
        self.X = np.c_[np.ones((self.X.shape[0], 1)), self.X]
        
        #Converting axis to float type
        self.X = self.X.astype(float)
        self.y = self.y.astype(float)
        
        #Analysing length of x and y component before training
        print(f"length of x: {self.X.shape}")
        print(f"length of y: {self.y.shape}")
        
        # Training the system ( error solved)
        if len(self.datafr) >= 4:
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.X,self.y,test_size=0.35, random_state = 50)
        else:
            #If we've small data
            self.x_train = self.X
            self.y_train = self.y
            
            self.y_test = None
            self.x_test = None
            
            self.test_error = None
            
        #problem wrapped up    
        self.scaler_X = StandardScaler()
        self.X_train_scaled = self.scaler_X.fit_transform(self.x_train)
        self.X_test_scaled  = self.scaler_X.transform(self.x_test)

        self.scaler_y = StandardScaler()
        self.y_train_scaled = self.scaler_y.fit_transform(self.y_train.reshape(-1, 1)).ravel()
        
        self.w = np.linalg.lstsq(self.X_train_scaled,self.y_train_scaled, rcond = None)[0]
        
        print("\nShape of training parameters:")
        print(self.X_train_scaled.shape)
        print(self.y_train_scaled.shape)
        print(self.X_test_scaled.shape)
        print(self.y_test.shape)

    def perceptron(self):
        
        print("Perceptron running...")
        
        #Verifying the data existence
        print("\ntraining parameters is None?")
        print("x_train:", self.X_train_scaled is None)
        print("y_train:", self.y_train_scaled is None)
        print("x_test:", self.X_test_scaled is None)
        print("y_test:", self.y_test is None)

        #training with multi layer perceptron
        regr = MLPRegressor(hidden_layer_sizes = (100,50), max_iter = 1000, random_state = 50,learning_rate_init = 0.001, activation='tanh', alpha = 1e-5,solver='adam',early_stopping = True,validation_fraction=0.1 )
        
        #problem solved
        regr.fit(self.X_train_scaled,self.y_train_scaled)
        
        if self.X_test_scaled is not None:
        
            self.pred_regr_scaled = regr.predict(self.X_test_scaled)
            
            #coming back to original scale
            self.pred_regr = self.scaler_y.inverse_transform(self.pred_regr_scaled.reshape(-1, 1)).ravel()
            
            self.rsme_regr = np.sqrt(mean_squared_error(self.y_test,self.pred_regr))
        else:    
        
            self.pred_regr_scaled = regr.predict(self.X_train_scaled)
            
            self.pred_regr = scaler_y.inverse_transform(self.pred_regr_scaled.reshape(-1, 1)).ravel()
            self.rsme_regr = None

        
        print("perceptron prediction:", self.pred_regr)
        print("rmse:", self.rsme_regr)
    
        return self.pred_regr, self.rsme_regr
        
    def visualization_reg(self):
        X = self.X
        y = self.y
        
        X_scaled = self.scaler_X.fit_transform(X)

        perc = self.perceptron()
        
        y_pred = X_scaled @ self.w
        
        #Normalizing y_pred
        y_pred_norm = self.scaler_y.inverse_transform(y_pred.reshape(-1,1))
        
        #Taking out the bias to visualization
        X_wbias = X_scaled[:,-1]

        #Manual Regression
        plt.figure(figsize=(10,4))
        plt.subplot(1, 2, 1)
        plt.scatter(X_wbias, y, color = 'blue',alpha=0.5)
    
        plt.plot(X_wbias, y_pred_norm, 'r-')
        plt.legend(["sample without bias","prediction"])
        plt.title('Linear regression')
        plt.xlabel('Features')
        plt.ylabel('Prediction (W)')
        plt.axhline(0, color= 'black', linestyle = '--') 
         
        #Residuos x prediction
        residuo_percp = self.y_test - self.pred_regr
        
        plt.figure(figsize=(10,4))
        plt.subplot(1, 2, 2)
        plt.scatter(self.pred_regr, residuo_percp, alpha=0.7)
        
        plt.title('prediction x residuo')
        plt.xlabel('prediction')
        plt.ylabel('residuos')
        plt.axhline(0, color= 'r', linestyle = '--')
        plt.show()
            
        #Analysing prediction
        print(f"\n\tManual prediction: \n{y_pred_norm}")
        
                
        y_pred_norm_new = y_pred_norm.ravel()
        pred_regr_new = self.pred_regr.ravel()
        
        #Looking to same length of both data to compare
        min_len = min(len(y_pred_norm_new), len(pred_regr_new))
        y_pred_norm_new = y_pred_norm_new[:min_len]
        pred_regr_new = pred_regr_new[:min_len]

        # Manual prediction x perceptron prediction
        print(f"manual: {y_pred_norm_new.shape}")
        print(f"perceptron: {pred_regr_new.shape}")
        
        plt.figure(figsize=(10,4))
        plt.scatter(y_pred_norm_new, pred_regr_new, alpha=0.7)
        
        plt.title('Manual prediction x perceptron prediction')
        plt.xlabel('Manual')
        plt.ylabel('Perceptron')
        plt.axhline(0, color= 'black', linestyle = '--')
        plt.show()
    
