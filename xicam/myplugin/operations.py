import numpy as np
from scipy.ndimage import gaussian_filter

from xicam.plugins.operationplugin import OperationPlugin, output_names

# How to define an operation plugin ...
# define a python function with type hinting
# then add special decorators


# inputs are defined as the function parameters
# outputs are defined as a decorator, output_names


@OperationPlugin
@output_names("output_image", "X")
def fft(input_image:np.ndarray = np.zeros(5),input_param:int = 3) -> (np.ndarray,int):
    output = np.abs(np.fft.ifft(np.real(np.fft.fft(input_image))))
    outputsm = gaussian_filter(output,input_param, order=0, mode='wrap')
    output_2 = input_param
    return outputsm, output_2

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
    output = np.absolute(input_image)
    output_2 = "x"
    return output, output_2
