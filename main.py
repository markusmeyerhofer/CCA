import datetime as dt

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import gc
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, Dropout, LSTM
from tensorflow.keras.models import Sequential

import importmodulepd as inp

# Load Data
cur = "ADA"

data = inp.getPanda()

#print(data)

a = pd.DataFrame()
data = data[data[ 'Kürzl' ] == cur ]
data = pd.DataFrame.append(a, data, ignore_index="True")

#print(data)

# Prepare Data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(data[ "PreisÄpct" ].values.reshape(-1, 1))

#prediction_days = (len(data)-1)
prediction_days = 60

x_train = [ ]
y_train = [ ]

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[ x - prediction_days:x, 0 ])
    y_train.append(scaled_data[ x, 0 ])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[ 0 ], x_train.shape[ 1 ], 1))

# Build The Model
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[ 1 ], 1)))
model.add(Dropout(0.9))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.9))
model.add(LSTM(units=50))
model.add(Dropout(0.9))
model.add(Dense(units=1))  # Prediction of next closing value

model.compile(optimizer="adam", loss="mean_squared_error")
model.fit(x_train, y_train, epochs=10, batch_size=32)

'''Test The Model Accuracy on Existing Data'''

# Load Test Data
test_start = dt.datetime(2020, 1, 1)
test_end = dt.datetime.now()

test_data = inp.getPanda()

a = pd.DataFrame()
test_data = test_data[ test_data[ 'Kürzl' ] == cur ]
test_data = pd.DataFrame.append(a, test_data, ignore_index="True")

actual_prices = test_data[ "PreisÄpct" ].values

total_dataset = pd.concat((data[ "PreisÄpct" ], test_data[ "PreisÄpct" ]), axis=0)

model_inputs = total_dataset[ len(total_dataset) - len(test_data) - prediction_days: ].values
model_inputs = model_inputs.reshape(-1, 1)
model_inputs = scaler.transform(model_inputs)

# Make Predictions on Test Data
x_test = [ ]

for x in range(prediction_days, len(model_inputs)):
    x_test.append(model_inputs[ x - prediction_days:x, 0 ])

x_test = np.array(x_test)
x_test = np.reshape(x_test, (x_test.shape[ 0 ], x_test.shape[ 1 ], 1))

predicted_prices = model.predict(x_test)
predicted_prices = scaler.inverse_transform(predicted_prices)

# Plot The Test Predictions
plt.plot(actual_prices, color="blue", label=f"Actual {cur} Price USD")
plt.plot(predicted_prices, color="orange", label=f"Predicted {cur} Price USD")
plt.title(f"{cur} Share Price")
plt.xlabel("Abrufe")
plt.ylabel(f"{cur} Share Price")
plt.legend()
plt.show()

# Predict Next Day

real_data = [ model_inputs[ len(model_inputs) + 1 - prediction_days:len(model_inputs + 1), 0 ] ]
real_data = np.array(real_data)
real_data = np.reshape(real_data, (real_data.shape[ 0 ], real_data.shape[ 1 ], 1))

prediction = model.predict(real_data)
prediction = scaler.inverse_transform(prediction)
print(f"Prediction:  {prediction} USD | {prediction*0.81876} EUR")
