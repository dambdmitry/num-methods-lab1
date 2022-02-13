import math

h = 0.1
a = 0
b = 1
N = int((b - a) / h)


def p(x, alpha):
    return 0.5 / (x + alpha)


def q(x, alpha):
    return 0


def f(x, alpha, step):
    return (1 / (math.sqrt(x + alpha))) * step * step


def ak(xk, alpha, step):
    return 1 - p(xk, alpha) * step / 2


def bk(xk, alpha, step):
    return (2 - q(xk, alpha) * step * step) * (-1)


def ck(xk, alpha, step):
    return (1 + p(xk, alpha) * step / 2)


def alpha(m):
    return 1 + 0.4 * m


def rk(rk_minus1, xk_minus1, m, step):
    return -ck(xk_minus1, alpha(m), step) / (ak(xk_minus1, alpha(m), step) * rk_minus1 + bk(xk_minus1, alpha(m), step))


def sk(rk_minus1, sk_minus1, xk_minus1, m, step):
    return (f(xk_minus1, alpha(m), step) - ak(xk_minus1, alpha(m), step) * sk_minus1) / (
    ak(xk_minus1, alpha(m), step) * rk_minus1 +bk(xk_minus1, alpha(m), step))


if __name__ == "__main__":
    xk = 0
    k = 0
    x1 = a + h
    m = 1
    r2 = -ck(x1, alpha(m), h) / bk(x1, alpha(m), h)
    s2 = f(x1, alpha(m), h) / bk(x1, alpha(m), h)
    r1 = (-ck(x1, alpha(m), h) / r2 - bk(x1, alpha(m), h)) / ak(x1, alpha(m), h)
    s1 = (s2 * (ak(x1, alpha(m), h) * r1 + bk(x1, alpha(m), h)) - f(x1, alpha(m), h)) / (-ak(x1, alpha(m), h))

    print("r1 = {0}; s1 = {1}".format(r1, r2))
    print("r2 = {0}; s1 = {1}".format(r2, s2))
    print("===================================")
    r2 = rk(r1, x1, m, h)
    s2 = sk(r1, s1, x1, m, h)
    print("r2 = {0}; s2 = {1}".format(r2, s2))
