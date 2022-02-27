import math

h = 0.1
a = 0
b = 1
N = int((b - a) / h)


def p(x, alpha):
    return 0.5 / (x + alpha)

def q(x, alpha):
    return 0

def f(x, alpha):
    return -1 / (math.sqrt(x + alpha))

def ak(xk, alpha, step):
    return 1 + (p(xk, alpha) * step) / 2

def bk(xk, alpha, step):
    return 1 - (p(xk, alpha) * step) / 2

def ck(xk, alpha, step):
    return 2 - q(xk, alpha) * step * step

def alpha(m):
    return 1 + 0.4 * m


def rk_plus1(rk, xk, alpha, step):
    return ak(xk, alpha, step) / (ck(xk, alpha, step) - bk(xk, alpha, step) * rk)

def sk_plus1(sk, rk, xk, alpha, step):
    return (f(xk, alpha) * step * step + bk(xk, alpha, step) * sk) / (ck(xk, alpha, step) - bk(xk, alpha, step) * rk)

def r1(x1, alpha, step):
    return (4*alpha*ak(x1, alpha, step) - ck(x1, alpha, step)*alpha) / (3*ak(x1, alpha, step)*step + 3*alpha*ak(x1, alpha, step) - bk(x1, alpha, step)*alpha)

def s1(x1, alpha, step):
    return (alpha*ak(x1, alpha, step)*step + f(x1, alpha)*step*step*alpha) / (3*ak(x1, alpha, step)*step + 3*alpha*ak(x1, alpha, step) - bk(x1, alpha, step)*alpha)


def fillRcf(step, alpha):
    result = []
    x1 = a + step
    rFirst = r1(x1, alpha, step)
    result.append(rFirst)
    n = int((b - a) / step)
    for k in range(1, n):
        xk = a + h*k
        rk = result[k-1]
        rk_Plus1 = rk_plus1(rk, xk, alpha, step)
        result.append(rk_Plus1)
    return result

def fillCcf(step, alpha, rCfs):
    result = []
    x1 = a + step
    sFirst = s1(x1, alpha, step)
    result.append(sFirst)
    n = int((b - a) / step)
    for k in range(1, n):
        xk = a + h * k
        sk = result[k-1]
        rk = rCfs[k-1]
        sk_Plus1 = sk_plus1(sk, rk, xk, alpha, step)
        result.append(sk_Plus1)
    return result


def yNN(rn, rn_minus1, sn, sn_minus1, alpha, step):
    return (step * (2 * math.sqrt(1 + alpha) - rn_minus1 * sn - sn_minus1 - 4 * sn)) / (3 + step * rn * (rn_minus1 - 4))


def yN(rn, rn_minus1, sn, sn_minus1, alpha, step):
    return (2*step*math.sqrt(1+alpha) - rn_minus1*sn - sn_minus1 + 4*sn) / (3 + rn_minus1*rn - 4*rn)


def fillBySweepMethod(step, alpha):
    result = []
    rCoefficients = fillRcf(step, alpha)
    sCoefficients = fillCcf(step, alpha, rCoefficients)
    rn = rCoefficients[-1]
    rn_minus1 = rCoefficients[-2]
    sn = sCoefficients[-1]
    sn_minus1 = sCoefficients[-2]
    yn = yN(rn, rn_minus1, sn, sn_minus1, alpha, step)
    result.append(yn)
    k = 0
    for i in range(len(rCoefficients) - 1, -1, -1):
        yk = rCoefficients[i] * result[k] + sCoefficients[i]
        result.append(yk)
        k += 1
    result.reverse()
    return result


def calculateVaults(yGrid, yGridHalfStep):
    vaults = []
    for i, value in enumerate(yGrid):
        vaults.append(math.fabs(value - yGridHalfStep[i])/3)
    return vaults

def yy(x, alpha):
    return 2/3*(x + alpha)**1.5 + alpha/3
if __name__ == "__main__":
    for m in range(1, 11):
        ALPHA = alpha(m)
        print("m = {0}; alpha = {1}".format(m, ALPHA))
        yGrid = fillBySweepMethod(h, ALPHA)
        yGridHalfStep = fillBySweepMethod(h / 2, ALPHA)
        yGridHalfStep = yGridHalfStep[::2]
        vaults = calculateVaults(yGrid, yGridHalfStep)

        x = a
        i = 0
        for y in yGrid:
            yyy = yy(x, ALPHA)
            print("x = {0}; y = {1}; точное решение = {2} погрешность = {3}".format(round(x, 4), round(y, 5),round(yyy, 5), round(vaults[i], 6)))
            x += h
            i += 1
