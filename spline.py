import numpy as np
import load_foil as lf
import matplotlib.pyplot as mp;

# Returns the second derivative of the interpolating function at each point where
# xa is the array containing the x coordinate of each point
# ya is the array containing the y coordinate of each point
# n is the number of points
def spline(xa, ya, n):
	u = np.zeros(n)
	y2 = np.zeros(n)

	y2[1] = 0.0
	u[1] = 0.0

	for i in range(1, n-1):
		sig = (xa[i] - xa[i-1]) / (xa[i+1] - xa[i-1])
		p = sig * y2[i-1] + 2.0
		y2[i] = (sig - 1.0) / p
		u[i] = (ya[i+1] - ya[i]) / (xa[i+1] - xa[i]) - (ya[i] - ya[i-1]) / (xa[i] - xa[i-1])
		u[i] = (6.0 * u[i] / (xa[i+1] - xa[i-1]) - sig * u[i-1]) / p

	y2[n - 1] = 0.0
	for k in range(n-2, 0, -1):
		y2[k] = y2[k] * y2[k+1] + u[k]

	return y2

# Return the value of the spline at a given x coordinate where
# xa is the array containing the x coordinate of each point
# ya is the array containing the y coordinate of each point
# y2a is the array containing the second derivaive of the function at each point
# n is the number of points
def splint(xa, ya, y2a, n, x):
	k = 0
	h = 0.0
	b = 0.0
	a = 0.0
	klo=1
	khi=n
	while khi - klo > 1:
		k = (khi + klo) // 2
		if xa[k - 1] > x:
			khi = k
		else:
			klo = k

	khi = khi - 1
	klo = klo - 1

	h = xa[khi] - xa[klo]

	if (h == 0.0):
		raise Exception("Bad xa input to routine splint")

	a = (xa[khi] - x) / h
	b = (x - xa[klo]) / h

	return a * ya[klo] + b * ya[khi] + (((a**3) - a) * y2a[klo] + ((b**3) - b) * y2a[khi]) * (h * h) / 6.0

# Return the spline function passing through each provided point where
# xa is the array containing the x coordinate of each point
# ya is the array containing the y coordinate of each point
# n is the number of points
def spline_fun(xa, ya, n):
	y2 = spline(xa, ya, n)
	return lambda x: splint(xa, ya, y2, n, x)


if __name__ == "__main__":
	(dim,ex,ey,ix,iy) = lf.load_foil("k1.dat")
	espline = spline_fun(ex, ey, int(dim[0]))
	ispline = spline_fun(ix, iy, int(dim[1]))

	r = np.arange(0, 1.00001, 0.001)

	mp.plot(r, list(map(espline, r)), linewidth = 1.0)
	mp.plot(ex, ey, marker='.', linestyle="None")
	mp.plot(r, list(map(ispline, r)), linewidth = 1.0)
	mp.plot(ix, iy, marker='.', linestyle="None")
	mp.axis('equal')
	mp.title("Cubic spline interpolation of the airfoil")
	mp.show()



