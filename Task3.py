import math

y0 = 1
a = 0
b = 1
epsilon = 1e-4

h = 0.1

N = int((b - a) / h)


def f(x, y):
    return x * y * y + y


def deltaY(xi, yi, step):
    k1 = step * f(xi, yi)
    k2 = step * f(xi + step / 2, yi + k1 / 2)
    k3 = step * f(xi + step / 2, yi + k2 / 2)
    k4 = step * f(xi + step, yi + k3)
    return (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def explicitFormula(xk_minus1, yk_minus1, xk_minus2, yk_minus2, step):
    return yk_minus1 + step * (1.5 * f(xk_minus1, yk_minus1) - 0.5 * f(xk_minus2, yk_minus2))


def getYkByExplicitFormula(xk, step):
    x = a
    yGrid = [y0]
    xGrid = [x]
    y1 = y0 + deltaY(x, y0, step)
    x = x + step
    yGrid.append(y1)
    xGrid.append(x)
    k = 2
    while x < xk:
        yk = explicitFormula(xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], step)
        x += step
        k += 1
        xGrid.append(x)
        yGrid.append(yk)
    return yGrid.pop()


def implicitFormula(xk, yk, xk_minus1, yk_minus1, xk_minus2, yk_minus2, step):
    return yk_minus1 + step * (5 / 12 * f(xk, yk) + 8 / 12 * f(xk_minus1, yk_minus1) - 1 / 12 * f(xk_minus2, yk_minus2))

def getYkByImplicitFormula(xk, step):
    x = a
    yGrid = [y0]
    xGrid = [x]
    y1 = y0 + deltaY(x, y0, step)
    x = x + step
    yGrid.append(y1)
    xGrid.append(x)
    k = 2
    while x < xk:
        yk_ = explicitFormula(xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], step)
        x = a + step * k
        yk_1 = implicitFormula(x, yk_, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], step)
        yk_2 = implicitFormula(x, yk_1, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], step)
        while math.fabs(yk_2 - yk_1) > step*step*step:
            yk_1 = yk_2
            yk_2 = implicitFormula(x, yk_2, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], step)
        xGrid.append(x)
        yGrid.append(yk_2)
        k += 1
    return yGrid.pop()

if __name__ == "__main__":
    print("ЯВНАЯ СХЕМА АДАМСА")
    x0 = a
    yGrid = [y0]
    xGrid = [x0]
    y1 = y0 + deltaY(x0, y0, h)
    xGrid.append(x0 + h)
    yGrid.append(y1)
    vaults = [0]
    vaults.append(math.fabs(y1 - (y0 + deltaY(x0, y0, h / 2))))
    for k in range(2, N+1):
        yk = explicitFormula(xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], h)
        xk = a + h * k
        xGrid.append(xk)
        yGrid.append(yk)
        ykHalfStep = getYkByExplicitFormula(xk, h / 2)
        vaults.append(math.fabs(yk - ykHalfStep) / 3)
    x = a
    i = 0
    for y in yGrid:
        print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), vaults[i]))
        x = round(x + h, 1)
        i += 1

    print("НЕЯВНАЯ СХЕМА АДАМСА")
    xGrid = xGrid[:2]
    yGrid = yGrid[:2]
    vaults = vaults[:2]
    for k in range(2, N+1):
        yk_ = explicitFormula(xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], h)
        xk = a + h * k
        yk_1 = implicitFormula(xk, yk_, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], h)
        yk_2 = implicitFormula(xk, yk_1, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], h)
        while math.fabs(yk_2 - yk_1) > h*h*h:
            yk_1 = yk_2
            yk_2 = implicitFormula(xk, yk_2, xGrid[k - 1], yGrid[k - 1], xGrid[k - 2], yGrid[k - 2], h)
        yGrid.append(yk_2)
        xGrid.append(xk)
        ykHalfStep = getYkByImplicitFormula(xk, h / 2)
        vaults.append(math.fabs(yk_2 - ykHalfStep) / 7)
    x = a
    i = 0
    for y in yGrid:
        print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), vaults[i]))
        x = round(x + h, 1)
        i += 1
