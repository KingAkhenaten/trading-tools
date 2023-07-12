# -*- coding: utf-8 -*-
"""
Helper functions for futures trading tools
Created on Tue Jul 11 22:56:04 2023

@author: Christian
"""
import math
from functools import wraps
from decimal import Decimal, ROUND_DOWN


def decimal_arguments(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        new_args = [Decimal(arg) if isinstance(
            arg, (int, float, str)) else arg for arg in args]
        new_kwargs = {k: Decimal(v) if isinstance(
            v, (int, float, str)) else v for k, v in kwargs.items()}
        return func(*new_args, **new_kwargs)
    return wrapper


@decimal_arguments
def round_partial(value, resolution):
    return math.ceil(value / resolution) * resolution


@decimal_arguments
def round_decimal(value):
    return value.quantize(Decimal('0.00'), ROUND_DOWN)
