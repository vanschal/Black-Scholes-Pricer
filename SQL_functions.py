import mysql.connector
from uuid import uuid4

# Insert your details here, it will be used as a helper method in the function below
# Before using the functionality make sure you set up a mySQL database already so that you can access it
def connect_to_db():
    return mysql.connector.connect(
        host = "localhost",
        user = "your_username",
        password = "your_password",
        database = "your_database"
    )
# Function that saves the inputs as a snapshot
def save_inputs_to_db(spot_price, strike_price, time_to_maturity, volatility, risk_free_rate):
    connection = connect_to_db()
    cursor = connection.cursor()
    calculation_id = str(uuid4()) # Generates a unique identifier 
    query = """INSERT INTO inputs (Spot, Strike, InterestRate, Volatility, TimeToExp, CalculationId) \
               VALUES (%s, %s, %s, %s, %s, %s)""" # Defining input categories
    values = (spot_price, strike_price, risk_free_rate, volatility, time_to_maturity, calculation_id) # Query and insert values into the table
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    connection.close()
    return calculation_id # Returning the calculation_id so that the outputs table can have the same one
# Function that saves the outputs as a snapshot
def save_outputs_to_db(calculation_id, spot_range, vol_range, call_pnl, put_pnl):
    connection = connect_to_db()
    cursor = connection.cursor()
    query = """INSERT INTO outputs (CalculationId, SpotShock, VolShock, OptionType, Value) \ 
               VALUES (%s, %s, %s, %s, %s)""" # Defining the output categories
    for i, vol in enumerate(vol_range):
        for j, spot in enumerate(spot_range):
            cursor.execute(query, (calculation_id, spot, vol, 'CALL', call_pnl[i, j])) # Iterates through the heatmaps and saves the values
            cursor.execute(query, (calculation_id, spot, vol, 'PUT', put_pnl[i, j]))
    connection.commit()
    cursor.close()
    connection.close()

"""
Below is the code to initialize the SQL inputs and outputs table that corresponds to the functionality

CREATE TABLE inputs (
    Spot DECIMAL(10, 2),
    Strike DECIMAL(10, 2),
    InterestRate DECIMAL(5, 4),
    Volatility DECIMAL(5, 4),
    TimeToExp DECIMAL(5, 2),
    CalculationId VARCHAR(36) PRIMARY KEY
);

CREATE TABLE outputs (
    CalculationId VARCHAR(36),
    SpotShock DECIMAL(10, 2),
    VolShock DECIMAL(5, 4),
    OptionType ENUM('CALL', 'PUT'),
    Value DECIMAL(10, 2),
    FOREIGN KEY (CalculationId) REFERENCES inputs(CalculationId)
);
"""