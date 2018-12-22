from tkinter import *
from math import cos
from math import sin
from math import sqrt
size = 500
root = Tk()
canvas = Canvas(root, width=size, height=size)
canvas.pack()


def draw_line_horizontal(X,Y) :
    if Y[1] != Y[0] :
        return None
    if X[1] < X[0] :
        X[0], X[1] = X[1], X[0]
    for x in range(X[0], X[1]+1) :
        canvas.create_rectangle(x,Y[0],x,Y[0],fill="black")

def draw_line_vertical(X,Y) :
    if X[0] != X[1] :
        return None
    if Y[1] < Y[0] :
        Y[0], Y[1] = Y[1], Y[0]
    for y in range(Y[0],Y[1]+1) :
        canvas.create_rectangle(X[0],y,X[0],y,fill="black")

def draw_line(X,Y) :
    if len(X) != 2 and len(Y) != 2 :
        return None
    dx = X[1]-X[0]
    dy = Y[1]-Y[0]
    if dx == 0 :
        draw_line_vertical(X,Y)
        return None
    if dy == 0 :
        draw_line_horizontal(X,Y)
        return None
    if abs(dy/dx) <= 1 :
        if dx < 0 :
            X[0], X[1] = X[1], X[0]
            Y[0], Y[1] = Y[1], Y[0]
            dx=X[1]-X[0]; dy = Y[1]-Y[0]
        if dy > 0:
            step = 1
        if dy < 0:
            step = -1
        error = 0
        y = Y[0]
        dy = abs(dy)
        for x in range(X[0], X[1]+1) :
            canvas.create_rectangle(x,y,x,y,fill="black")
            error+=dy
            if 2*error>dx:
                y+=step
                error -= dx
        return None
    if abs(dy/dx) > 1 :
        if dy < 0 :
            X[0], X[1] = X[1], X[0]
            Y[0], Y[1] = Y[1], Y[0]
            dx=X[1]-X[0]; dy = Y[1]-Y[0]
        if dx > 0:
            step = 1
        if dx < 0:
            step = -1
        error = 0
        x = X[0]
        dx = abs(dx)
        for y in range(Y[0], Y[1]+1) :
            canvas.create_rectangle(x,y,x,y,fill="black")
            error+=dx
            if 2*error>dy:
                x+=step
                error -= dy
        return None

def draw_poly(X,Y, Fill=0) :
    #Fill = 0 -- no filling
    #Fill = 1 -- even odd method
    #Fill = 2 -- nonzero method
    if len(Y) != len(X) :
        return None
    line_list = []
    for i in range( len(X) ):
        line_list.append( [ [ X[i-1],X[i] ], [ Y[i-1],Y[i] ] ] )
    #poly_type(line_list)
    print(None)
    if Fill != 0 :
        for i in range(size) :
            for j in range(size) :
                if Fill == 1 :
                    if(even_odd(i,j,line_list) == True) :
                        canvas.create_rectangle(i,j,i,j,fill="black")
                if Fill == 2 :
                    if(non_zero(i,j,line_list) == True) :
                        canvas.create_rectangle(i,j,i,j,fill="black")
    for i in range( len(line_list) ):
        draw_line(line_list[i][0],line_list[i][1])

def intersection(X0,Y0,X1,Y1) :
    A = []; B =[]; C = []
    A.append(Y0[0] - Y0[1]); A.append(Y1[0] - Y1[1])
    B.append(X0[1] - X0[0]); B.append(X1[1] - X1[0])
    C.append(X0[1]*Y0[0] - X0[0]*Y0[1])
    C.append(X1[1]*Y1[0] - X1[0]*Y1[1])

    D = A[0]*B[1] - A[1]*B[0]
    if D == 0 :
        return False
    Dx = -(B[0]*C[1] - B[1]*C[0])
    Dy = A[0]*C[1] - A[1]*C[0]

    xi = Dx/D; yi = Dy/D
    if (X0[1]-X0[0]) != 0 :
        t = (xi-X0[0])/(X0[1]-X0[0])
        dx = abs( 1/(X0[1]-X0[0]) )
        #print("t =",t,"dx =",dx)
        if t > 1-dx or t<0+dx :
            return False
    else :
        t = (yi-Y0[0])/(Y0[1]-Y0[0])
        dy = abs( 1/(Y0[1]-Y0[0]) )
        #print("t =",t,"dy =",dy)
        if t > 1-dy or t<0+dy :
            return False
    if (X1[1]-X1[0]) != 0 :
        t = (xi-X1[0])/(X1[1]-X1[0])
        dx = abs( 1/(X1[1]-X1[0]) )
        #print("t =",t,"dx =",dx)
        if t > 1-dx or t<0+dx :
            return False
    else :
        t = (yi-Y1[0])/(Y1[1]-Y1[0])
        dy = abs( 1/(Y1[1]-Y1[0]) )
        #print("t =",t,"dy =",dy)
        if t > 1-dy or t<0+dy :
            return False

    return True

def vect_product(X0,Y0,X1,Y1) :
    a0 = [ X0[1]-X0[0], Y0[1]-Y0[0] ]
    a1 = [ X1[1]-X1[0], Y1[1]-Y1[0] ]
    return a0[0]*a1[1] - a0[1]*a1[0]

def scal_product(v1,v2, is_int = True) :
    if len(v1) != len(v2) :
        return None
    result = 0
    for i in range( len(v1) ) :
        result+=v1[i]*v2[i]
    if is_int == True :
        return int(result)
    else:
        return result

def poly_type(LL) :
    simp = []
    conv = []
    #print(len(LL))
    for i in range(len(LL)) :
        for j in range(i,len(LL)) :
            simp.append( intersection(LL[i-1][0],LL[i-1][1],LL[j][0],LL[j][1]) )
        #print(simp[i])
    if simp.count(True) != 0 :
        print("сложный, не выпуклый")
        return None
    else :
        for i in range(len(LL)) :
            conv.append( vect_product(LL[i-1][0],LL[i-1][1],LL[i][0],LL[i][1]) )
        if conv[0] > 0 :
            for i in range(1,len(conv)):
                if conv[i] < 0 :
                    print("простой, не выпуклый")
                    return None
        if conv[0] < 0 :
            for i in range(1, len(conv)) :
                if conv[i] > 0 :
                    print("простой, не выпуклый")
                    return None
        print("простой, выпуклый")
        
def even_odd(x0,y0,LL) :
    ray_x = [x0,size]
    ray_y = [y0,y0]
    is_in = False
    for i in range(len(LL)) :
        if( intersection(LL[i][0],LL[i][1],ray_x,ray_y) == True ) :
            is_in = not is_in
        else :
            continue
    return is_in

def non_zero(x0,y0,LL) :
    ray_x = [x0,size]
    ray_y = [y0,y0]
    is_in = 0
    for i in range(len(LL)) :
        if( intersection(LL[i][0],LL[i][1],ray_x,ray_y) == True ) :
            rl = vect_product( LL[i][0],LL[i][1],ray_x,ray_y )
            is_in+= rl/abs(rl)
    if is_in != 0 :
        return True
    else :
        return False

def factorial(n) :
    if n == 0 :
        return 1
    else :
        return factorial(n-1)*n

def C_nk(n) :
    b = []
    for k in range(n+1):
        b.append(factorial(n)/factorial(k)/factorial(n-k))
    return b

def bezier(X,Y) :
    #Bezier curves
    #   B = Sum n! / k! /(n-k)! * (1-t)^(n-k) * Pk
    N = len(X); n = N-1
    b = C_nk(n)
    print( b )
    B = []
    t = 0; dt = 0.05
    while t <= 1+dt :
        x = 0; y = 0
        dbdx = 0
        for k in range(N) :
            x += ( b[k]*(1-t)**(n-k) * t**k )*X[k]
            y += ( b[k]*(1-t)**(n-k) * t**k )*Y[k]
        B.append([int(x),int(y)])
        t+=dt
    #print(B)
    line_list = []
    for i in range(len(B)-1) :
        line_list.append( [ [ B[i][0],B[i+1][0] ], [ B[i][1],B[i+1][1] ] ] )
    print(line_list)
    for line in line_list :
        draw_line( line[0],line[1] )

def points_intersec(X0,Y0,X1,Y1) :
    A = []; B =[]; C = []
    A.append(Y0[0] - Y0[1]); A.append(Y1[0] - Y1[1])
    B.append(X0[1] - X0[0]); B.append(X1[1] - X1[0])
    C.append(X0[1]*Y0[0] - X0[0]*Y0[1])
    C.append(X1[1]*Y1[0] - X1[0]*Y1[1])

    D = A[0]*B[1] - A[1]*B[0]
    if D == 0 :
        return False
    Dx = -(B[0]*C[1] - B[1]*C[0])
    Dy = A[0]*C[1] - A[1]*C[0]

    xi = Dx/D; yi = Dy/D
    return [int(xi),int(yi)]

def distance_to_poly(poly) :
    #poly = [ [X, Y, Z],...,[X,Y,Z] ] 
    Z = []
    for line in poly :
        Z.append( (line[2][0]+line[2][1])/2 )
    return  abs(sum(Z)/len(Z))

def clipped_line(X,Y,poly,poly_draw=False) :
    line_list = []
    section = []
    for i in range( len(poly[0]) ):
        line_list.append( [ [ poly[0][i-1],poly[0][i] ], [ poly[1][i-1],poly[1][i] ] ] )
    #for line in line_list:
        #draw_line(line[0],line[1])
    for line in line_list :
        if intersection(X,Y,line[0],line[1]) == True :
            section.append(points_intersec(X,Y,line[0],line[1]))
    print(section)
    section[0][1], section[1][0] = section[1][0], section[0][1]
    draw_line(section[0],section[1])
    if poly_draw :
        for line in line_list:
            draw_line(line[0],line[1])

def line_rotation(M, X,Y,Z) :
    for i in range(len(X)) :
        dot_new = dot_rotation(M, [X[i],Y[i], Z[i]])
        X[i] = dot_new[0]; Y[i] = dot_new[1]; Z[i] = dot_new[2]

def dot_rotation(M, dot) :
    dot_new = []
    for i in range(3) :
        dot_new.append( scal_product(M[i],dot) )
    return dot_new

def cube_rotation(line_list,axis,phi) :
    M = [] # матрица поворота
    c = cos(phi); s = sin(phi)
    l = sqrt(axis[0]**2+axis[1]**2+axis[2]**2)
    if l == 1 :
        x = axis[0]; y = axis[1]; z = axis[2]
    else :
        x = axis[0]/l; y = axis[1]/l; z = axis[2]/l
    # заполнение матрицы поворота относительно произвольной оси v = (x,y,z)
    M.append( [ c+(1-c)*x**2, (1-c)*x*y-s*z, (1-c)*x*z+s*y ] )
    M.append( [ (1-c)*y*x+s*z, c+(1-c)*y**2, (1-c)*y*z-s*x ] )
    M.append( [ (1-c)*z*x-s*y, (1-c)*z*y+s*x, c+(1-c)*z**2 ] )
    dot_new = []

    for line in line_list :
        line_rotation(M,line[0],line[1],line[2])

def get_visible_polies(poly_list) :
    rho = []; visible = []
    for i in range( len(poly_list) ) :
        rho.append( distance_to_poly(poly_list[i]) )
    print(rho) 
    for i in range( 3 ) :
        idx = rho.index( min(rho) )
        print(idx)
        visible.append( poly_list[idx] )
        rho.pop(idx); poly_list.pop(idx)
    return(visible)

def draw_cube(X,Y,Z,axis=[1,1,0], phi=0.1, persp = False, hide = True) :
    # X = [x1,x2], Y = [y1,y2], Z = [z1,z2] -- параллелипипед, плоскости которого параллельны Z
    line_list = []
    for z in Z :
        for i in range(len(X)) :
            line_list.append( [ [X[i],X[i]], [Y[-1],Y[0]], [z,z] ] )
        for i in range(len(Y)) :
            line_list.append( [ [X[-1],X[0]], [Y[i],Y[i]], [z,z] ] )
    for x in X :
        for i in range(len(Z)) :
            line_list.append( [ [x,x], [Y[-1],Y[0]], [Z[i],Z[i]] ] )
        for i in range(len(Y)) :
            line_list.append( [ [x,x], [Y[i],Y[i]], [Z[-1],Z[0]] ] )
    for y in Y :
        for i in range(len(X)) :
            line_list.append( [ [X[i],X[i]], [y,y], [Z[-1],Z[0]] ] )
        for i in range(len(Z)) :
            line_list.append( [ [X[-1],X[0]], [y,y], [Z[i],Z[i]] ] )
    cube_rotation(line_list,axis,phi)
    poly_list = [ line_list[i:i+4] for i in range(0,len(line_list),4) ]
    #print(len(poly_list))
    if hide == True :
        visible_poly = get_visible_polies(poly_list)
        line_list.clear()
        #print(len(visible_poly))
        for i in range(len(visible_poly)) :
            line_list.extend(visible_poly[i])
    if persp == True :
        dot_perspective( line_list )
    else :
        parallel_projection(line_list)

def parallel_projection(line_list) :
    for line in line_list :
        draw_line(line[0],line[1])

def dot_perspective(line_list,dot = [250,250,-500]) :
    for line in line_list :
        for j in range(len(line[0])) :
            x = line[0][j]; y = line[1][j]; z = line[2][j]
            x = int( dot[0] + dot[2]*(dot[0]-x)/(z-dot[2]) )
            y = int( dot[1] + dot[2]*(dot[1]-y)/(z-dot[2]) )
            line[0][j] = x; line[1][j] = y
        draw_line( line[0],line[1] ) 
    

dphi = 0.1
phi = 0
while True :
    canvas.delete("all")
    #bezier([50,450,50,450],[450,450,50,50])
    #clipped_line( [0,500],[250,250], [ [50,450,450,50],[50,50,450,450] ], True )
    draw_cube([200,300],[200,300],[100,300],[1,1,0],phi,False)
    phi+=dphi
    root.update()