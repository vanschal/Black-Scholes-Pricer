# Black-Scholes-Pricer

This project is a Dash-based implementation of the Black-Scholes option pricing model. It provides a user-friendly web interface for calculating option prices and visualizing the results using interactive heatmaps.

## Features

- Black-Scholes Pricing: Calculate Call and Put option prices based on user-defined parameters such as Spot Price, Strike Price, Time to Maturity, Volatility, and Risk-Free Rate.
- Interactive Heatmaps: Visualize PnL (Profit and Loss) for Call and Put options as heatmaps. Heatmaps dynamically adjust based on user input for spot price range and volatility range.
- Database Integration (Optional): Save user inputs and calculated outputs to a MySQL relational database for tracking and analysis.
- Responsive Design: Built with Dash and Bootstrap for a clean, responsive user interface.

## Code Overview

- app.py: Main application file containing the Dash app layout and callback logic.
- Calculation_Utils.py: Contains the implementation of the Black-Scholes model.
- Object_Utils.py: Includes helper classes for creating UI components like formula variables and cards.
- SQL_functions.py: Provides functions for saving inputs and outputs to a MySQL database (optional).

## Acknowledgements

This project draws significant inspiration from the Black-Scholes implementation in the following repository:

- prudhvi-reddy-m/BlackScholes (https://github.com/prudhvi-reddy-m/BlackScholes/blob/main/streamlit_app.py#L166)

### Key Differences:

- This implementation uses Dash instead of Streamlit for the front-end interface.
- Added functionality for calculating and visualizing PnL (Profit and Loss).
- Includes optional integration with a MySQL database to store user inputs and outputs.
