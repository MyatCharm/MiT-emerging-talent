def polysum(n,s):
    '''
    n = number of side of a polygon
    s = length of side of the polygon
    '''
    import math
    tan = math.tan #tangent
    pi = math.pi #pi
    
    area = (0.25 * n * (s**2)) / (tan(pi/n))
    
    perimeter = n*s
    
    sum = round((area+perimeter**2),4)
    
    return sum