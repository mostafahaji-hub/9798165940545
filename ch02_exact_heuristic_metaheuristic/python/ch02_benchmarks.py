"""Five standard benchmark test functions (Section 2-8-4). All have global minimum f* = 0.
Used again in Chapter 9 to compare SA, GA and Keshtel."""
import numpy as np
def sphere(x):     x = np.asarray(x); return float(np.sum(x**2))                                  # x in [-100,100], f*=0 at 0
def rosenbrock(x): x = np.asarray(x); return float(np.sum(100*(x[1:]-x[:-1]**2)**2 + (1-x[:-1])**2))  # f*=0 at (1,...,1)
def rastrigin(x):  x = np.asarray(x); return float(10*len(x) + np.sum(x**2 - 10*np.cos(2*np.pi*x)))  # x in [-5.12,5.12]
def ackley(x):
    x = np.asarray(x); D = len(x)
    return float(-20*np.exp(-0.2*np.sqrt(np.sum(x**2)/D)) - np.exp(np.sum(np.cos(2*np.pi*x))/D) + 20 + np.e)
def griewank(x):
    x = np.asarray(x); i = np.arange(1, len(x)+1)
    return float(1 + np.sum(x**2)/4000 - np.prod(np.cos(x/np.sqrt(i))))
FUNCTIONS = {'Sphere': sphere, 'Rosenbrock': rosenbrock, 'Rastrigin': rastrigin, 'Ackley': ackley, 'Griewank': griewank}
if __name__ == '__main__':
    for n, f in FUNCTIONS.items(): print(f'{n:11s} f(opt)={f([1,1]) if n=="Rosenbrock" else f([0,0]):.6f}   f(3,4)={f([3,4]):.4f}')
