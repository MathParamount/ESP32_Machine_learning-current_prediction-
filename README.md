Durante a etapa do código houve diversos erros corrigidos que são mostrados aqui:

# Overview

This project focuses on serial data acquisition, data processing, machine learning regression, and visualization to predict electrical power consumption in a simple electronic system.
Data is collected using an ESP32, processed in Python, and analyzed with machine learning models (Perceptron / MLPRegressor).

The system measures current and power in a circuit built on a protoboard using sensors and simple loads such as a fan and a lamp.

# Project Structure

```
├── read_firmware.py
├── main.py
├── regression.py
├── visualization.py
└── README.md

```

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

## Residuals vs Prediction:

Compares Perceptron predictions with a manually calculated prediction and manual prediction is based on the X variable and weights from the regression class.
The Perceptron consistently predicts values approximately 0.1 above the manual estimation.

# Practical Project

## Hardware setup:

The system is composed of:

* ESP32
* ACS712-5B current sensor
* Protoboard
* DC fan (cooler)
* Small lamp (LED)

Cooler specifications:

* Max speed: 1500 RPM
* Average consumption: 0.9 W
* Operating current: < 180 mA

Measured values are plausible, with average power around 1.6 W.

## Model limitations:

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
* Motor requires voltag

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
