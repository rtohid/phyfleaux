from pytiramisu import init, var, expr, computation

if __name__ == "__main__":

    init("foo")
    srange_expr = expr(0) 
    erange_expr = expr(100) 
    i = var("i", srange_expr, erange_expr)
    j = var("j", srange_expr, erange_expr)
    iter_range = [i, j]
    crange_expr = expr(0)
    C = computation(iter_range, crange_expr)
    #C.parallelize()
    #C.vectorize(j, 4)
