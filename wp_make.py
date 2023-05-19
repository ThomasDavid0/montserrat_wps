import numpy as np
from geometry import Point, PX, PY, PZ, Euler, Euldeg
from geometry import GPS


SUMMIT = GPS(16.71036180777751, -62.1768528125355)
SUMMIT_H = 900

hmin=450
w=2000
downw = 1000

tri_w = 150
tri_d = 100
legh = 50


def create_tri(tri_w, tri_d, legh):
    return Point(np.array([
        [0, 0, 0],
        [tri_d, tri_w, legh/2],
        [0, tri_w, legh]
    ]))

def create_stack(n, w, tri_w, tri_d, legh):
    ps = [PY(w/2)]
    for i in range(n):
        ps.append(create_tri(-tri_w, -tri_d, -legh) + Point(0, -w/2, -2*i*legh))
        if i < n-1:
            ps.append(create_tri(tri_w, -tri_d, -legh) + Point(0, w/2, -(2*i+1)*legh) )
        else:
            ps.append(Point(0, w/2, -(2*i+1)*legh))
    return Point.concatenate(ps)


def offset_stack(h_wind, depth, hmin, stack):
    return Euldeg(0, 0, h_wind).transform_point(
        stack + Point(-depth, 0, -hmin)
    )


def create_mission(missionxyz: Point, outfile:str):
    mission = SUMMIT.offset(missionxyz)
    
    with open(outfile, "w") as f:
        f.write("QGC WPL 110\n")
        f.write("0	1	0	16	0	0	0	0	16.7146981	-62.2280973	13.309999	1\n")
        f.write("1	0	3	16	0.00000000	0.00000000	0.00000000	0.00000000	16.71495970	-62.22436310	60.000000	1\n")
        i=2
        for gps, alt in zip(mission, missionxyz.z):
            f.write(f"1	0	3	16	0.00000000	0.00000000	0.00000000	0.00000000	{gps.lat[0]}	{gps.long[0]}	{int(-alt)}	1\n")
            i+=1
        f.write(f"{i}	0	3	17	0.00000000	0.00000000	0.00000000	0.00000000	16.71419930	-62.22685220	50.000000	1\n")
    

if __name__ == "__main__":
    from wps_plot import plot_wpxys
    stack = create_stack(3, 2000, 250, 150, 100)
    stack2 = create_stack(3, 2000, 250, 150, -100)
    offset_stack1 = offset_stack(90, 2200, 450, stack)
    offset_stack2 = offset_stack(90, 3500, 950, stack2)
    #plot_wpxys(offset_stack)
    
    create_mission(
        Point.concatenate([offset_stack1, offset_stack2]), 
        "/mnt/c/users/td6834/test.txt"
    )