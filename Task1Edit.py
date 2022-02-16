import math

# Function constant
y0 = 0
a = 0
b = 1
N = 10
h = (b - a) / N
epsilon = 0.0005


def f(x, y, k, n):
    alpha = 1 + 0.25 * k
    beta = -0.5 + 0.2 * n
    return math.cos(y) / (alpha + x) + beta * y * y


def getYiPlus1ByExplicitMethod(xi, yi, step, k, n):
    yPlus1 = yi + step * f(xi, yi, k, n)
    return yPlus1


def getYiPlus1ByExplicitMethodHalfStep(xi, step, k, n):
    yGridHalfStep = [y0]
    x = a
    i = 0
    while x <= xi:
        yi = yGridHalfStep[i]
        yGridHalfStep.append(getYiPlus1ByExplicitMethod(x, yi, step, k, n))
        x += step
        i += 1
    return yGridHalfStep.pop()


def getYiByImplicitMethod(xi, yi, yi_minus1, step, k, n):
    yi = yi_minus1 + step * f(xi, yi, k, n)
    return yi


def getYiByImplicitMethodHalfStep(xi, step, k, n):
    yGridHalfStep = [y0]
    x = a
    i = 1
    while x <= xi:
        yi_minus1 = yGridHalfStep[i - 1]
        yiByExplicitMethod = getYiPlus1ByExplicitMethodHalfStep(x, step, k, n)
        yi = getYiByImplicitMethod(x, yiByExplicitMethod, yi_minus1, step, k, n)
        yGridHalfStep.append(yi)
        x += step
        i += 1
    return yGridHalfStep.pop()


def predictor(xi, yi, step, alpha, k, n):
    yi_plus1 = yi + alpha * step * f(xi, yi, k, n)
    return yi_plus1


def corrector(xi, yi, step, predictor, delta, alpha, k, n):
    yi_plus1 = yi + step * ((1 - delta) * f(xi, yi, k, n) + delta * f(xi + alpha * step, predictor, k, n))
    return yi_plus1


def getYi_plus1ByPC(xi, yi, step, alpha, delta, k, n):
    predictorValue = predictor(xi, yi, step, alpha, k, n)
    return corrector(xi, yi, step, predictorValue, delta, alpha, k, n)


def getYi_plus1ByPCHalfStep(xi, step, alpha, delta, k, n):
    yGridHalfStep = [y0]
    x = a
    i = 0
    while x <= xi:
        yi = yGridHalfStep[i]
        yi_plus1 = getYi_plus1ByPC(x, yi, step, alpha, delta, k, n)
        x += step
        i += 1
        yGridHalfStep.append(yi_plus1)
    return yGridHalfStep.pop()


def fillByExplicitMethod(step, k, n):
    yGridA = [y0]
    xi = a
    i = 0
    while xi < b-step:
        xi = a + step * i
        yi = yGridA[i]
        yi_plus1 = getYiPlus1ByExplicitMethod(xi, yi, step, k, n)
        i += 1
        yGridA.append(yi_plus1)
    return yGridA


def explicitVaults(yGridA, yGridAHalfStep):
    vaults = []
    for i in range(len(yGridA)):
        vault = math.fabs(yGridA[i] - yGridAHalfStep[i])
        vaults.append(vault)
    return vaults


if __name__ == "__main__":
    for k in range(5):
        for n in range(5):
            print("Результаты при k = {0}, n = {1}".format(k, n))
            print("Явный метод Эйлера")
            yGridA = fillByExplicitMethod(h, k, n)
            step = h / 2
            sliceNum = 2
            yGridAHalfStep = fillByExplicitMethod(step, k, n)[::2]
            sliceNum *= 2
            vaultsA = explicitVaults(yGridA, yGridAHalfStep)
            while max(vaultsA) > epsilon:
                yGridA = yGridAHalfStep
                step = step / 2
                yGridAHalfStep = fillByExplicitMethod(step, k, n)[::sliceNum]
                sliceNum *= 2
                vaultsA = explicitVaults(yGridA, yGridAHalfStep)
            x = a
            i = 0
            for y in yGridA:
                print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), round(vaultsA[i], 6)))
                x = round(x + h, 1)
                i += 1
            ############################################################################################################
            print("Неявный метод Эйлера")
            yGridB = [y0]
            vaultsB = [0]
            for i in range(1, N + 1):
                xi = (a + h * i)
                yiByExplicitMethod = yGridA[i]
                yi_minus1 = yGridB[i - 1]
                yi = getYiByImplicitMethod(xi, yiByExplicitMethod, yi_minus1, h, k, n)
                step = h / 2
                yiHalfStep = getYiByImplicitMethodHalfStep(xi, step, k, n)
                while math.fabs(yi - yiHalfStep) > epsilon:
                    yi = yiHalfStep
                    step = step / 2
                    yiHalfStep = getYiByImplicitMethodHalfStep(xi, step, k, n)
                yGridB.append(yiHalfStep)
                vaultsB.append(math.fabs(yi - yiHalfStep))
            x = a
            i = 0
            for y in yGridB:
                print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), round(vaultsB[i], 6)))
                x = round(x + h, 1)
                i += 1
            ############################################################################################################
            print("Метод Предикатор-Корректор")
            yGridC = [y0]
            vaultsC = [0]
            ALPHA = 1
            DELTA = 0.5
            for i in range(N):
                xi = (a + h * i)
                yi = yGridC[i]
                yi_plus1 = getYi_plus1ByPC(xi, yi, h, ALPHA, DELTA, k, n)
                step = h / 2
                yi_plus1HalfStep = getYi_plus1ByPCHalfStep(xi + h, step, ALPHA, DELTA, k, n)
                while math.fabs(yi_plus1 - yi_plus1HalfStep) / 3 > epsilon:
                    yi_plus1 = yi_plus1HalfStep
                    step = step / 2
                    yi_plus1HalfStep = getYi_plus1ByPCHalfStep(xi + h, step, ALPHA, DELTA, k, n)
                yGridC.append(yi_plus1HalfStep)
                vaultsC.append(math.fabs(yi_plus1 - yi_plus1HalfStep) / 3)
            x = a
            i = 0
            for y in yGridC:
                print("x = {0}; y = {1}; погрешность = {2}".format(x, round(y, 5), round(vaultsC[i], 6)))
                x = round(x + h, 1)
                i += 1
