import math
import matplotlib
matplotlib.use("Agg")
from scipy.stats import norm

class BlackScholes:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        self.time_to_maturity = time_to_maturity
        self.strike = strike
        self.current_price = current_price
        self.volatility = volatility
        self.interest_rate = interest_rate
        self.call_price = 0
        self.put_price = 0

    def calculate_prices(self):
        d1 = (math.log(self.current_price / self.strike) + (self.interest_rate + 0.5 * self.volatility ** 2) * self.time_to_maturity) / (self.volatility * math.sqrt(self.time_to_maturity))
        d2 = d1 - self.volatility * math.sqrt(self.time_to_maturity)

        self.call_price = (self.current_price * norm.cdf(d1) - self.strike * math.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(d2))
        self.put_price = (self.strike * math.exp(-self.interest_rate * self.time_to_maturity) * norm.cdf(-d2) - self.current_price * norm.cdf(-d1))
