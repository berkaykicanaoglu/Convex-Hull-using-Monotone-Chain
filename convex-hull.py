#----------------------------
# Class definitions
#----------------------------
class Point2D(object):
    # constructor for the point class
    def __init__(self, x, y):
        self.x = x
        self.y = y
    # override the representation method   
    def __repr__(self):
        return "(%f, %f)" %(self.x, self.y) 
    def getCoordinates(self):
        return [self.x, self.y]    
    
class Line2D(object):
    # constructor for the line class
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2
        print point2.x, point1.x
        # calculate the slope of the line
        self.slope = (self.p2.y - self.p1.y) \
                     / (self.p2.x - self.p1.x) 
        # set the variable derivative
        if self.slope > 0:
            self.derivative = "positive"
        elif self.slope == 0:
            self.derivative = "none"
        else:
            self.derivative = "negative" 
    # return the slope
    def getSlope(self):
        return self.slope

    ''' define the orientation of point-triplet
        and decide whether they form a ccw or cw
        rotation (or colinear).
        source: 
        http://www.geeksforgeeks.org/orientation-3-ordered-points/
    '''         
    def orientation(self,line2):
        # get slopes
        slope1 = self.getSlope()
        slope2 = line2.getSlope()
        # get difference
        diff = slope2-slope1
        # determine orientation
        if diff > 0:
            return -1 # counter-clockwise
        elif diff == 0:
            return 0  # colinear
        else:
            return 1  # clockwise 
#----------------------------
# Helper functions
#----------------------------
def getX(point):
    return point.x
def getY(point):
    return point.y            
def sortPoints(point_list):
    point_list = sorted(point_list,key = getX)
    # This function do not account for comparison
    # of two points at the same x-location. Resolve!  
    return point_list          
            
def ConvexHull(point_list):
    # initalize two empty lists for upper 
    # and lower hulls.
    upperHull = []
    lowerHull = [] 
    # sort the list of 2D-points
    sorted_list = sortPoints(point_list) 
  
    for point in sorted_list:
        if len(lowerHull)>=2:
            line1 = Line2D(lowerHull[len(lowerHull)-2],\
                           lowerHull[len(lowerHull)-1]) 
            line2 = Line2D(lowerHull[len(lowerHull)-1],\
                           point)               
        while len(lowerHull)>=2 and \
        line1.orientation(line2) != -1:
            removed = lowerHull.pop()
            if lowerHull[0] == lowerHull[len(lowerHull)-1]:
                break
            # set the last two lines in lowerHull
            line1 = Line2D(lowerHull[len(lowerHull)-2],\
                           lowerHull[len(lowerHull)-1]) 
            line2 = Line2D(lowerHull[len(lowerHull)-1],\
                           point)
        lowerHull.append(point)  
    # reverse the list for upperHull search     
    reverse_list = sorted_list[::-1]                    
    for point in reverse_list:
        if len(upperHull)>=2:
            line1 = Line2D(upperHull[len(upperHull)-2],\
                           upperHull[len(upperHull)-1]) 
            line2 = Line2D(upperHull[len(upperHull)-1],\
                           point)               
        while len(upperHull)>=2 and \
        line1.orientation(line2) != -1:
            removed = upperHull.pop()
            if upperHull[0] == upperHull[len(upperHull)-1]:
                break
            # set the last two lines in lowerHull
            line1 = Line2D(upperHull[len(upperHull)-2],\
                           upperHull[len(upperHull)-1]) 
            line2 = Line2D(upperHull[len(upperHull)-1],\
                           point)
        upperHull.append(point)          
    
    # final touch: remove the last members
    # of each point as they are the same as 
    # the first point of the complementary set. 
    removed = upperHull.pop()
    removed = lowerHull.pop()
    # concatenate lists
    convexHullPoints = lowerHull + upperHull
    print "Lower: ",lowerHull
    print "Upper: ",upperHull 
    return convexHullPoints
def visualize(point_list,convexHull_list):
    import matplotlib.pyplot as plt
    x = [a.x for a in point_list]
    y = [a.y for a in point_list]
    plt.scatter(x,y)  
    # draw lines
    for p in range(len(convexHull_list)-1):
        p1 = convexHull_list[p]
        p2 = convexHull_list[p+1]
        plt.plot([p1.x, p2.x], [p1.y, p2.y], color='k', linestyle='-', linewidth=2)
    # connect first and last points
    first = convexHull_list[0]
    last  = convexHull_list[len(convexHull_list)-1]
    plt.plot([first.x, last.x], [first.y, last.y], color='k', linestyle='-', linewidth=2)
    # display the hull
    plt.show()    
      
# main.py
# read the points from a file (I/O)
point_list = []
file_name = "points.txt"
with open(file_name) as pointSet:   
    for line in pointSet:
        coords = line.split(" ")
        point = Point2D(float(coords[0]),float(coords[1]))
        point_list.append(point)

# call the convex hull (Monotone Chain) function
convexSet_list = ConvexHull(point_list)
# visualize the hull
visualize(point_list,convexSet_list)
