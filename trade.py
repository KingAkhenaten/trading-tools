# -*- coding: utf-8 -*-
"""
Futures Trading Tools

Created on Tue Jul 11 22:56:04 2023

@author: Christian
"""
import numpy as np
from decimal import Decimal, getcontext
from utils import decimal_arguments, round_decimal, round_partial
import pandas as pd

FEE = Decimal('2.62')
STEP = Decimal('0.25')
COST_PER_POINT = Decimal('5.00')
RANGE = 5  # Range for choose_long and choose_short

getcontext().prec = 28


@decimal_arguments
def calc_be_long(open_price):
    """
    Calculate Break-Even
    (rounded up, so the exact value may be slightly profitable)
    """
    # Cost for opening and closing a trade
    point_difference = (FEE * 2) / COST_PER_POINT
    break_even = round_partial(open_price + point_difference, STEP)
    return break_even


@decimal_arguments
def calc_be_short(open_price):
    """
    Calculate Break-Even
    """
    # Cost for opening and closing a trade
    point_difference = (FEE * 2) / COST_PER_POINT
    break_even = open_price - round_partial(point_difference, STEP)
    return break_even


@decimal_arguments
def calc_loss(open_price, current_price):
    """
    Calculate loss + commissions
    """
    loss = (open_price - current_price) * COST_PER_POINT + (2 * FEE)
    return loss


@decimal_arguments
def calc_profit(open_price, current_price):
    """
    Calculate profit - commissions
    """
    profit = abs((current_price - open_price)) * COST_PER_POINT - (2 * FEE)
    return profit


@decimal_arguments
def choose_long(open_price):
    """
    Scan for target closes given a long
    """
    low = calc_be_long(open_price)
    high = low + RANGE
    price_range = [round_decimal(Decimal(x))
                   for x in np.arange(float(low), float(high) + float(STEP), float(STEP))]
    profit_range = [round_decimal(calc_profit(open_price, price))
                    for price in price_range]
    # We want to sort top-down, high to low (descending)
    df = pd.DataFrame({"Price": price_range,
                       "Profit": profit_range})
    print(df.sort_values(by="Price", ascending=False).to_string(index=False))


@decimal_arguments
def choose_short(open_price):
    """
    Scan for target closes given a short
    """
    high = calc_be_short(open_price)
    low = high - RANGE
    price_range = [round_decimal(Decimal(x))
                   for x in np.arange(float(low), float(high) + float(STEP), float(STEP))]
    profit_range = [round_decimal(calc_profit(open_price, price))
                    for price in price_range]
    # We want to go top-down, high to low (descending)
    df = pd.DataFrame({"Price": price_range,
                       "Profit": profit_range})
    print(df.sort_values(by="Price", ascending=False).to_string(index=False))
