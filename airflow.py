import numpy as np
import matplotlib.pyplot as mp
from integration import *
import load_foil as lf
from spline import spline_fun
from math import *

# Returns the derivative of the function f at the point x
def derivate(f, x, h):
	return  (f(x+h)-f(x-h))/(2 * h)

# Returns the length of the curve f
# [a;b] is the interval of integration
# epsilon is the precision of the integral
def length (f, a, b, method, epsilon, h):
	g = lambda x : derivate(f, x, h)
	u = lambda x : sqrt(1 + g(x)*g(x))
	return integrate(method, u, a, b, epsilon)

# Returns the curve situated between the upper side of the wing and the maximal altitude
#beyond which the air is not disturbed by the wing.
# l is the lambda in the interval [0;1]
# h is the maximum of the function f in the interval [0;1]
def airflow_curve(f, l, h):
	return lambda x: (1 - l) * f(x) + l * 3*h

# Returns the spped of the airflow following the curve
# l is the lambda in the interval [0;1]
# h is the maximum of the function f in the interval [0;1]
def airflow_speed(f, l, h):
	return length(airflow_curve(f, l, h), 0, 1, midpoint, 1e-2, 1e-6)

# Returns the pressure of the airflow following the curve
# l is the lambda in the interval [0;1]
# h is the maximum of the function f in the interval [0;1]
def airflow_pressure(f, l, h):
	return 0.5 * (airflow_speed(f, l, h) ** 2)

# Returns the pressure of the airflow at a given point around the wing
# (x,y) the position where the pressure is calculated
# espline is the curve describing the upper surface of the wing ""extrados""
# ispline is the curve describing the lower surface of the wing ""intrados""
# hmax (hmin) is the maximum (the minimum) of the function
def airflow_pressure_map(x, y, espline, ispline, hmax, hmin):
	if y > 3*hmax or y < 3*hmin:
		return 0.5

	ev = espline(x)
	if y > ev:
		l = (y - ev) / (3*hmax - ev)
		return airflow_pressure(espline, l, hmax)

	iv = ispline(x)
	if y < iv:
		l = (y - iv) / (3*hmin - iv)
		return airflow_pressure(ispline, l, hmin)

	return 0.5

# Show the laminar flow
# espline is the curve describing the upper surface of the wing ""extrados""
# ispline is the curve describing the lower surface of the wing ""intrados""
# p/l are steps used in drawing the map
def laminar_flow_display(espline,ispline,p,l):
	hmax = ey.max()
	hmin = iy.min()

	r = np.arange(0, 1.00001, p)
	mp.subplot(121)
	for i in np.arange(0, 1.00001, l):
		mp.plot(r, list(map(airflow_curve(espline, i, hmax), r)), color='black', linewidth = 1.0)
		mp.plot(r, list(map(airflow_curve(ispline, i, hmin), r)), color='black', linewidth = 1.0)
	mp.axis('equal')
	mp.title("Laminal flow above and below the wing")

# Show the pressure map 
# espline is the curve describing the upper surface of the wing ""extrados""
# ispline is the curve describing the lower surface of the wing ""intrados""
def pressure_map_diplay(espline,ispline):
	hmax = ey.max()
	hmin = iy.min()

	pmap = np.matrix([[airflow_pressure_map(x, y, espline, ispline, hmax, hmin) for x in np.arange(0, 1.00001, 0.005)] 
		for y in np.arange(3 * hmax, 3 * hmin, -0.002)])
	mp.subplot(122)
	mp.imshow(pmap, cmap = 'hot', interpolation = 'bilinear',extent = [0, 1, 3*hmin, 3*hmax])
	mp.plot()
	mp.title("Pressure map")
	mp.show()

if __name__ == "__main__":
	(dim,ex,ey,ix,iy) = lf.load_foil("k1.dat")
	espline = spline_fun(ex, ey, int(dim[0]))
	ispline = spline_fun(ix, iy, int(dim[1]))

	laminar_flow_display(espline,ispline,0.001,0.1)
	pressure_map_diplay(espline,ispline)
	