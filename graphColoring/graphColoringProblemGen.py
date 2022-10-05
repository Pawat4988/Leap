import itertools
import random

random.seed(100)
# borders = [("BC", "AB"), ("BC", "NT"), ("BC", "YT"), ("AB", "SK"),
#            ("AB", "NT"), ("SK", "MB"), ("SK", "NT"), ("MB", "ON"),
#            ("MB", "NU"), ("ON", "QC"), ("QC", "NB"), ("QC", "NL"),
#            ("NB", "NS"), ("YT", "NT"), ("NT", "NU")]

def genProblem():

    provinces = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numOfProvince = random.randint(5,26)
    provinces = provinces[:numOfProvince]

    combOfProvinces = list(itertools.combinations(provinces,2))

    numOfBorders = random.randint(1,len(combOfProvinces))
    borders = random.sample(combOfProvinces, numOfBorders)

    return (provinces,borders)

def getMaxDegree(borders, lengOfBorder,provinces) :

    # Map to store the degrees of every node
    m = {}
     
    for i in range(lengOfBorder) :
        m[borders[i][0]] = 0
        m[borders[i][1]] = 0
         
    for i in range(lengOfBorder) :
         
        # Storing the degree for each node
        m[borders[i][0]] += 1
        m[borders[i][1]] += 1
 
    # maxi and mini variables to store
    # the maximum and minimum degree
    maxi = 0
 
    for i in provinces :
        try:
            maxi = max(maxi, m[i])
        except:
            pass

    return maxi

def genColor(maxDegree):
    output = []
    for i in range(maxDegree+1):
        output.append(i)
    return output


# provinces,borders = genProblem()
# maxDegree = getMaxDegree(borders,len(borders),provinces)
# colors = genColor(maxDegree)

