
import pandas as pd
import numpy as np
from scipy.integrate import quad
import matplotlib.pyplot as plt

# params
U_W = 40        # wind velocity in m/s
U_V = 40        # car velocity  in m/s
order = 2       # interpolation order

# read in angles 
thetas = pd.read_csv(r'C:\Users\amirt\Desktop\Kandidat\angles.txt', header=None)
theta_max = np.max(thetas[0])   

# read in C_d
cd_s = pd.read_csv(r'C:\Users\amirt\Desktop\Kandidat\cd.txt', header=None)

# make a linear interpolation between theta and cd 
theta_max = np.max(thetas[0])

def interpolation(thetas, cd_s, order):
    ''' function that interpolates the thetas and cd_s through some
    order and evaluates it at theta_:e'''
    coefficients = np.polyfit(thetas[0]*np.pi/180, cd_s[0], order) 
    return np.poly1d(coefficients)

interpolation_function = interpolation(thetas, cd_s, order)

# calculate relative speed
def relative_speed(U_W, U_V, theta):
    ''' function that calculates the relative speed 
    between the car and wind for a given yaw angle theta'''
    return np.sqrt((U_V**2+U_W**2+2*U_V*U_W*np.cos(theta)))

# calculate wind averaged drag coefficient
def wind_averaged_drag(U_W,U_V):
    ''' function that calculates wind-averaged drag coefficient
    for an input of the wind speed U_W and car speed U_V'''
    def integrand(psi):
        relative_velocity_ratio = (relative_speed(U_W, U_V, psi)/U_V)**2
        return interpolation_function(psi*np.pi/180) *(1 + relative_velocity_ratio * (1 - np.cos(psi * np.pi / 180))) ** 2
    
    result, _ = quad(integrand, 0, np.pi*theta_max/180, limit = 1000)
    return result / (np.pi*theta_max/180)

average_drag = wind_averaged_drag(U_W, U_V)
print("Wind averaged C_D = {}".format(average_drag))