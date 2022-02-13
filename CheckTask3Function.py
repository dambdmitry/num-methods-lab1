import math

y0 = 1
h = 0.1
a = 0
b = 1
N = int((b - a) / h)


def dy(x, y):
    return x*y*y + y


def deltaY(xi, yi, step):
    k1 = step * dy(xi, yi)
    k2 = step * dy(xi + step / 2, yi + k1 / 2)
    k3 = step * dy(xi + step / 2, yi + k2 / 2)
    k4 = step * dy(xi + step, yi + k3)
    return (1 / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


if __name__ == "__main__":
    yGrid = [y0]
    for i in range(N):
        xi = (a + h * i)
        yi = yGrid[i]
        deltaYi = deltaY(xi, yi, h)
        yi_plus1 = yi + deltaYi
        yGrid.append(yi_plus1)
    yGridHalfStep = [y0]
    step = h / 2
    x = a
    i = 0
    while x < b:
        yi = yGridHalfStep[i]
        deltaYi = deltaY(x, yi, step)
        yi_plus1 = yi + deltaYi
        yGridHalfStep.append(yi_plus1)
        x += step
        i += 1
    yGridHalfStep = yGridHalfStep[::2]
    vaults = []
    for i in range(len(yGrid)):
        vault = math.fabs(yGrid[i] - yGridHalfStep[i]) / 15
        vaults.append(vault)

    x = a
    i = 0
    for y in yGrid:
        print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), vaults[i]))
        x = round(x + h, 1)
        i += 1