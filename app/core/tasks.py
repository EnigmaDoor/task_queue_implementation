import time

def basic(data_input):
    a = data_input['a']
    b = data_input['b']
    output = { 'result': a * b }
    time.sleep(5)
    return output

def add(data_input):
    a = data_input['a']
    b = data_input['b']
    output = { 'result': a + b }
    time.sleep(5)
    return output

def divide(data_input):
    a = data_input['a']
    b = data_input['b']
    output = { 'result': a / b }
    time.sleep(5)
    return output
