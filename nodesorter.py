import math
def swap(a,b):
    return b,a
thresh  = 25
i=0
def dist_scan(nodept,nodept_old):
    dist = []
    for i in range(len(nodept)) :
        dist.append(math.sqrt((pow(nodept_old[i][0]-nodept[i][0],2)+pow(nodept_old[i][1]-nodept[i][1],2))))
    i=0
    for i in range(len(nodept)) :
        print i
        try :
            if  dist[i]>thresh :
                    if dist[i+1]>thresh :
                        nodept[i],nodept[i+1] = swap(nodept[i],nodept[i+1])
                        i=i+1
                        print "swapped"
        except:
            pass


    return nodept

