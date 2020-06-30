import numpy as np
import matplotlib.pyplot as mp

# Interpolates the function f using the left rectangle method on the range [a, b] with a precision of epsilon
# Returns the integral of f on the range [a, b], if track_efficiency = False
# Returns the integral of f on the range [a, b] and the dictionnary containing the value of each step, otherwise
def rectangle(f, a, b, epsilon, track_efficiency = False):
	n = 1
	# Initial integral for n = 1
	curIntegration = (b-a) * f(a)

	if track_efficiency:
		interalArray = {}
		interalArray[1] = curIntegration

	while n == 1 or np.abs(lastIntegration - curIntegration) > epsilon:
		lastIntegration = curIntegration # Save the previous value

		n *= 2
		h = (b-a)/n

		# Compute the new integral value
		sum = 0
		for i in range(1, n, 2):
			sum += f(a + h*i)

		curIntegration = h * sum + lastIntegration / 2

		if track_efficiency:
			interalArray[n] = curIntegration

	if track_efficiency:
		return curIntegration, interalArray
	else:
		return curIntegration

# Interpolates the function f using the midpoint rectangle method on the range [a, b] with a precision of epsilon
# Returns the integral of f on the range [a, b], if track_efficiency = False
# Returns the integral of f on the range [a, b] and the dictionnary containing the value of each step, otherwise
def midpoint(f, a, b, epsilon, track_efficiency = False):
	n = 1
	# Initial integral for n = 1
	curIntegration = (b-a) * f((a+b)/2)

	if track_efficiency:
		interalArray = {}
		interalArray[1] = curIntegration

	while n == 1 or np.abs(lastIntegration - curIntegration) > epsilon:
		lastIntegration = curIntegration # Save the previous value

		n *= 3
		h = (b-a)/n

		# Compute the new integral value
		sum = 0
		for i in range(0, n, 3):
			sum += f(a + h*i + h/2) + f(a + h*(i + 2) + h/2)

		curIntegration = h * sum + lastIntegration / 3

		if track_efficiency:
			interalArray[n] = curIntegration

	if track_efficiency:
		return curIntegration, interalArray
	else:
		return curIntegration

# Interpolates the function f using the given method on the range [a, b] with a precision of epsilon
# Returns the integral of f on the range [a, b], if track_efficiency = False
# Returns the integral of f on the range [a, b] and the dictionnary containing the value of each step, otherwise
def integrate(method, f, a, b, epsilon, track_efficiency = False):
	return method(f, a,  b, epsilon, track_efficiency)

def test_integral():
	# f(x) = x² + 2
	f = lambda x: x*x + 2
	a = 0
	b = 1
	epsilon = 1e-4
	expected = 7/3
	print("f(x) = x² + 2")
	print("Expected:", expected)

	integralLeft, interalLeftArray = integrate(rectangle, f, a, b, epsilon, True)
	print("--Left rectangle method--")
	print("Computed integral:", integralLeft)
	print("Relative error:", np.abs(expected - integralLeft) / expected)

	integralMid, interalMidArray = integrate(midpoint, f, a, b, epsilon, True)
	print("--Middle rectangle method--")
	print("Computed integral:", integralMid)
	print("Relative error:", np.abs(expected - integralMid) / expected)


	mp.plot(list(interalLeftArray.keys()), np.abs([expected] * len(interalLeftArray) - np.array(list(interalLeftArray.values()))), label = "Left rectangle", marker='.', linewidth = 1.0)
	mp.plot(list(interalMidArray.keys()), np.abs([expected] * len(interalMidArray) - np.array(list(interalMidArray.values()))), label = "Middle rectangle", marker='.', linewidth = 1.0)
	mp.xscale('log')
	mp.yscale('log')
	mp.legend()
	mp.title("Absolute error of the left rectangle and the midpoint methods\non the function $f(x) = x^2 + 2$ on the range [0, 1] with epsilon = $10^{-4}$")
	mp.xlabel("n, the number of calls of f")
	mp.ylabel("Absolute error of the computed integral value")
	mp.show()


if __name__ == "__main__":
	test_integral()