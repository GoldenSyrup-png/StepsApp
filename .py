from flask import Flask, redirect, url_for, request, render_template
import pandas as pd
from datetime import date
import random
import string
import hashlib

def encrypt(password):
    salt = "5gz"
    dataBase_password = password+salt
    hashed = hashlib.md5(dataBase_password.encode())
    return hashed.hexdigest()

print(encrypt("1234"))