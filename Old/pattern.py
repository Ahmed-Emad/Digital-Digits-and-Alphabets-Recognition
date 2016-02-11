from random import uniform
from random import randint

def data(N = 100):
    'return N random points (x1,x2)'
    d = []
    for i in range(N):
        x = uniform(-1,1)
        y = uniform(-1,1)
        d.append([x,y])
    return d

def randomline():
    'computes a random line and returns a and b params: y = ax + b'
    x1 = uniform(-1,1)
    y1 = uniform(-1,1)
    x2 = uniform(-1,1)
    y2 = uniform(-1,1)
    
    a = abs(x1-x2)/abs(y1-y2)
    b = y1 - a*x1
    return [a,b] # a*x + b

def map_x(point,f):
    'maps a point (x1,x2) to a sign -+1 following function f '
    x1 = point[0]
    y1 = point[1]
    
    y = f(x1)
    compare_to = y1
    return sign(y,compare_to)

def sign(x,compare_to = 0):
    'returns +1 or -1 by comparing x to compare_to param (by default = 0)'
    if x > compare_to:
        return +1
    else:
        return -1

def build_misclassified_set(t_set,w):
    '''returns a tuple of index of t_set items
such that t_set[index] is misclassified <=> yn != sign(w*point)'''
    res = tuple()
            
    for i in range(len(t_set)):
        point = t_set[i][0]
        s = h(w,point)
        yn = t_set[i][1]
        if s != yn:
            res = res + (i,)
    return res

def h(w,x):
    'Hypothesis function returns w0 x0 + w1 x1 ... + wn xn'
    res = 0
    for i in range(len(x)):
        res = res + w[i]*x[i]
    return sign(res)

def PLA(N_points = 100):
    ''' Returns
t_set: item of t_set is: [[vector_x], y]
w: vector of same dimention as vector_x of weights
iteration: Number of iterations needed for convergence
f: target lambda function f
'''
    N = N_points
    iteration = 0
    # create random contelation of points () in interval [-1,1]
    d = data(N)
    # create random target function
    l = randomline()
    # print 'Target function: %s x + %s' %(l[0], l[1])
    f = lambda x: l[0]*x + l[1]
    # weight vector w0 , w1, w2
    w = [0,0,0]
    # build training set
    t_set = []
    
    for i in range(len(d)):
        x = d[i]
        y = map_x(x,f) # map x to +1 or -1 for training points
        t_set.append( [ [ 1 ,x[0],x[1] ] , y ] )

    #iterate Perceptron Algorithm
    iterate = True
    count = 0
    while iterate:
        iteration = iteration + 1
        #pick a misclasified point from misclassified set
        misclassified_set = build_misclassified_set(t_set,w)
        # if there are no misclassified points break iteration weight are ok.
        if len(misclassified_set)==0:break
        index = randint(0,len(misclassified_set)-1)
        p = misclassified_set[index]
        point = t_set[p][0]

        s = h(w,point)
        yn = t_set[p][1]

        # update weights if misclassified
        if s != yn:
            xn = point
            w[0] = w[0] + yn*xn[0]
            w[1] = w[1] + yn*xn[1]
            w[2] = w[2] + yn*xn[2]
    return t_set,w,iteration,f

def evaluate_diff_f_g(f,w):
    'Returns the average of difference between f and g (g is equivalent as vector w )'
    count = 0
    limit = 100
    diff = 0
    while count < limit:
        count = count + 1
        # generate random point as out of sample data
        x = uniform(-1,1)
        y = uniform(-1,1)
        vector = [1,x,y]

        sign_f = sign(f(x),y)
        sign_g = h(w,vector)
        # check result and count if difference between target function f and hypothesis function g
        if sign_f != sign_g: diff = diff + 1

    return diff/(count*1.0)
        
    
def run_PLA(N_samples,N_points):
    samples = []# vector of 1 clasified, 0 misclassified
    iterations = []#vector of iterations needed for each PLA
    b_misclassified = False
    diff = []#vector of difference average between f and g

    for i in range(N_samples):
        # run PLA in sample
        t_set,w,iteration,f = PLA(N_points)
        iterations.append(iteration)
        # check if points are classified or not
        for i in range(len(t_set)):
            point = t_set[i][0]
            s = h(w,point)
            yn = t_set[i][1]
            if yn != s:
                samples.append(0)
                b_misclassified = True
                break
        # check difference between f and g
        diff.append(evaluate_diff_f_g(f,w))
        if not b_misclassified: samples.append(1)

        b_misclassified = False

    print 'number of samples misclassified: %s ' % samples.count(0)
    print 'number of classified samples: %s ' % samples.count(1)
    print 'number of iteration avg: %s ' % (str(sum(iterations)/len(iterations)*1.0))
    print 'average of difference in function g: %s' % ( sum(diff)/(len(diff)*1.0) )
