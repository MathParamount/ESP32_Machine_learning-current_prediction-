Durante a etapa do código houve diversos erros corrigidos que são mostrados aqui 
(During the code step there were several issues wrapped up, which are showing right here):

# Overview

![lamp](https://github.com/user-attachments/assets/3021a97d-780f-4e55-bea5-e76ad04ade0c)


This project focuses on serial data acquisition, data processing, machine learning regression, and visualization to predict electrical power consumption in a simple electronic system.
Data is collected using an ESP32, processed in Python, and analyzed with machine learning models (Perceptron / MLPRegressor).

The system measures current and power in a circuit built on a protoboard using sensors and simple loads such as a fan and a lamp.

# Project Structure

The creater followed a logical order to organize the project files.
```
├── src 
     └──read_firmware.py
     └──main.py
     └──regression.py
     ├── fireware_esp32
        └──fireware_esp32.ino
├── libraries
   └──details.txt
└── README.md

```

The image below shows a roadmap about the coding project structure:
![roadmap_pessoal_proj](https://github.com/user-attachments/assets/b40e25dd-0128-4fae-8b70-961156c6fecc)


# Read_firmware

This module is responsible for serial data parsing and dataframe construction.

## Key points:

The firmware data is converted into a DataFrame based on serial broadcasting, initially without predefined columns, such as:

1. W (power)
2. timestamp
3.raw_line

Data extraction was a learning process. Regular expressions were used with the re library, especially using:

```
\s*([\d\.]+)
```

to correctly capture numeric values from raw serial lines.
Dictionaries were used to incrementally build structured data before appending it to the DataFrame (self.datafr).
Initially, the idea was to have two classes in read_firmware: one for data acquisition and another for visualization.
However, the visualization class was removed and replaced with simple plotting functions, keeping this module focused only on data handling.

## Main

The main.py file acts as the execution entry point of the project.
Responsibilities:
1. Initializes the serial communication port to read data from the ESP32.
2. Implements logic to collect and print samples captured from the serial connection.
3. Initial tests with 20 samples resulted in high outliers. Increasing to 40 samples produced more stable and less biased results.

4. Calls the Regression class, passing the DataFrame obtained from read_firmware, and retrieves the weight coefficient (W).

# Regression

This module is responsible for data analysis, prediction, and model training.
Main features:
The goal is to predict system power based on serially injected data into the protoboard.

## Handles:

1. Data cleaning
2. Training
3. Prediction
4. Model evaluation

Drops unnecessary columns because they don't contribute to model training  such as:

* timestamp
* raw_line

A Perceptron-based approach was chosen due to system simplicity. However, since Perceptron is more suitable for classification, a Multi-Layer Perceptron Regressor (MLPRegressor) was adopted.

## Initial model used:

* 100 hidden layers
* Fair random state
* Data scaling was necessary because:
* Bias dominated the dataset
* Weights were very small

Both X and y were scaled, and y_pred was normalized for better visualization and the initial MLPRegressor failed to capture early and late data behavior. Adjustments made:

* Solver changed to adam
* Reduced learning_rate_init
* Enabled early_stopping
* Hidden layers changed to (100, 50)

Predictions were scaled back to original values, and Root Mean Square Error (RMSE) was calculated and the data reshaping and normalization were applied to fix plotting issues.
Moreover, the residual analysis showed dispersion between predicted and real values, which motivated further solver and training parameter adjustments.

# Visualization

This module is responsible for graphical interpretation of the data.

## Visual outputs:

1. Current vs Time: Shows how current flows through the circuit.
2. Average Power vs Time: Displays power dissipation behavior.
3. Linear Regression Plot: Comparison between predicted power and real power over normalized time.

The photos about the project is below:

1) Current and power
![current_ov_time_power](https://github.com/user-attachments/assets/0a5dddb7-527e-4c8e-a0eb-fbcf78424b53)

2) Prediction
![pred_x_res_linear](https://github.com/user-attachments/assets/161939ee-ef02-4f71-924d-c1c1ca7ec3e3)

## Residuals vs Prediction:

Compares Perceptron predictions with a manually calculated prediction and manual prediction is based on the X variable and weights from the regression class.
The Perceptron consistently predicts values approximately 0.1 above the manual estimation.

![manual_x_pred](https://github.com/user-attachments/assets/0a3cde76-f4d4-4519-ab18-a1d53935030e)

# Compilation
The project was used in python3 that is the newest version of python with less bugs and a better syntaxe and to install the Pyhton 3 you should verify the actual version of their computer.
1. Ubuntu/Debian:
``
sudo apt update
sudo apt install python3
``

2. Windows:
You need to acess the link below and download the newest version of python:
``
 https://python.org/downloads
``

You need to install the libraries to be able to compile the program:
``
pip install pandas;
pip install numpy;
pip install sklearn;
pip install matplotlib;
``

The code project was created in C++ and Pyhton. The C++ was used to create a fireware program with goal of read the serial ESP32 data. Which was calculated the offset and root mean square of current and voltage. In Python code I built 3 files for compile the project you should only call main.py file. If the serial connection is available it will run.

``
python3 main.py
``

# Practical Project

## Hardware setup:

The system is composed of:

* ESP32
* ACS712-5B current sensor
* Protoboard
* DC fan (cooler)
* Small lamp (LED)
* capacitor of 10 nF
* Resistor of 100 kΩ

Cooler specifications:

* Max speed: 1500 RPM
* Average consumption: 0.9 W
* Operating current: < 180 mA

Measured values are plausible, with average power around 1.6 W.

The frequency calcule is measured by formula below:

``
f = 1 / (2πRC) 
``

That gives us the frequency: ``` f ≈ 1591.5 Hz```

# Model limitations:

* High offset
* Electromagnetic noise

According to the ACS712 datasheet, offset noise can reach tens of millivolts.
In simulation, the power difference between the cooler ON and OFF was approximately 1.67 W.
In a more efficient system, this difference should be higher.

## LED behavior:

The LED does not turn on because the voltage drop after the cooler is approximately 0.5 V and it is insufficient for LED operation. Applying Ohm’s Law:

```
R = V / I = (12 - 0.5) / 2 A ≈ 5.75 Ω

```

## Observations:
* The cooler has significant resistance.
* The motor generates counter-electromotive force.
* It Requires startup current.

Series connection with an LED creates a paradox:
* LED requires current
* Motor requires voltage

The electric circuit was tested in serial and parallel connections. The image below shows a serial connection:

![fan](https://github.com/user-attachments/assets/3101d8fb-e709-4556-8d55-3630617c1e4b)

This circuit above only the fan activated and the lamp after the fan remained turned off, due to the voltage drop and fan's conter-electromotive force.

![parallel](https://github.com/user-attachments/assets/3d1f8cce-cc3d-4433-83dd-911504f994ae)

The parallel circuit didin't work so well, due to the starting current that ringes on threfold fan current.
Moreover, we realized that due to the starting current caused the prediction to fail, turning the system unstable and resulting in a wrong prediction, as show in image below.
![pique_corrente](https://github.com/user-attachments/assets/d905b4ee-5274-4ea2-abe4-db27624ff734)

It taught me that machine learning model works only to stable and linear systems. The image below shows a failed attempt to model a fan and lamp in a parallel connection.

![predic_failed](https://github.com/user-attachments/assets/2e0c58ea-a7f4-42d7-9496-f91d3c1d400b)


# Conclusion

This project demonstrates the complete pipeline of:

1. Embedded data acquisition
2. Serial communication
3. Data preprocessing
4. Machine learning regression
5. Model tuning
6. Visualization
7. Practical electronic validation

Despite limitations caused by noise, offsets, and hardware constraints, the results are consistent and educational, highlighting both machine learning challenges and real-world electronics behavior.
