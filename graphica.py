from tkinter import *
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

def scal_product(X0,Y0,X1,Y1) :
    a0 = [ X0[1]-X0[0], Y0[1]-Y0[0] ]
    a1 = [ X1[1]-X1[0], Y1[1]-Y1[0] ]
    return a0[0]*a1[0] + a0[1]*a1[1]

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

while True :
    canvas.delete("all")
    """
    draw_line([100,400],[100,50])
    draw_line([250,500],[250,150])
    draw_line([250,150],[250,0])
    draw_line([250,0],[250,150])
    
    draw_line([250,300],[250,500])
    draw_line([250,500],[250,300])
    draw_line([250,150],[250,500])
    draw_line([250,0],[250,400])
    """
    draw_poly([100,400,400,200,300,100],[100,100,400,250,250,400])
    root.update()