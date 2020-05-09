import matplotlib.pyplot as plt
import math

#x - artist pop, y - artist followers, z - song pop

#Distribution of z/x+1
def ratio_distribution():
    f = []
    for x in range(0, 101):
        for z in range(0, 101):
            f.append(z/(x+1))
    plt.hist(f)
    plt.show()
    return f

# Naive equation
# f(x,y,z) = z/x+1 + [(7.79 - log(Y+1)/7.79)*z - x]/x+1
# May not be the best equation, but it satisfies all necessary constraints (i.e. min/max at the correct values)
def EQ1(x, y, z):
    underrated_factor = (7.79 - math.log10(y+1))/7.79
    return z/(x + 1) + (underrated_factor * z -  x)/(x+1)

def EQ1_dist():
    f = []
    for x in range(0, 101):
        for z in range(0, 101):
            y = 0
            while(y < 20000000):
                f.append(EQ1(x,y,z))
                y += 100000
    plt.hist(f)
    plt.show()

#Perhaps use a more sophisticated regression model to map x,y,z, -> rank
