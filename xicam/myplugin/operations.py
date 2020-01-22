import numpy as np

from xicam.plugins.operationplugin import OperationPlugin, output_names

# How to define an operation plugin ...
# define a python function with type hinting
# then add special decorators


# inputs are defined as the function parameters
# outputs are defined as a decorator, output_names


@OperationPlugin
@output_names("output_image", "X")
def fft(input_image:np.ndarray = np.zeros(5)) -> (np.ndarray,str):
    output = np.fft.fftn(input_image)
    output_2 = "x"
    return output, output_2

@OperationPlugin
@output_names("output_image", "X")
def fft2(input_image:np.ndarray = np.zeros(5)) -> (np.ndarray,str):
    output = np.fft.fftn(input_image)
    output_2 = "x"
    return output, output_2


@OperationPlugin
@output_names("output_image", "X")
def imagpart(input_image:np.ndarray = np.zeros(5)) -> (np.ndarray,str):
    output = np.imag(input_image)
    output_2 = "x"
    return output, output_2


@OperationPlugin
@output_names("output_image", "X")
def realpart(input_image:np.ndarray = np.zeros(5)) -> (np.ndarray,str):
    output = np.real(input_image)
    output_2 = "x"
    return output, output_2


@OperationPlugin
@output_names("output_image", "X")
def absval(input_image:np.ndarray = np.zeros(5)) -> (np.ndarray,str):
    output = np.abs(input_image)
    output_2 = "x"
    return output, output_2
