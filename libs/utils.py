import pandas as pd

# Safe division function to avoid division by zero
def safe_divide(numerator, denominator):
    return numerator / denominator.where(denominator != 0, other=pd.NA)

def cast_number(number, type):
    return pd.to_numeric(number, errors='coerce').fillna(0).astype(type)