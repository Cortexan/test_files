import pandas as pd
import numpy as np
import math

def getPower(mass, kph, grade, frontalArea = 0.4, dragCoeff = 0.8, rollingCoeff = 5.0e-3):
    rho = 1.2
    eta = 0.985 # 1 - drive train loss = efficiency
    rollingCoeff = 5.0e-3 # from haskell code
    # mass = mass #kg
    grade = grade/100
    g = 9.81
    # kph = 45
    v = (0.277778 * kph)

    def fDrag(velocity):
        return 0.5*dragCoeff*frontalArea*rho*velocity*velocity

    def fRolling(grade, mass, velocity):
        if velocity > 0.01:
            return g * math.cos(math.atan(grade)) * mass * rollingCoeff
        else:
            return 0.0

    def fGravity(grade, mass):
        return g*math.sin(math.atan(grade))*mass
    
    totalForce = fDrag(v) + fRolling(grade, mass, v) + fGravity(grade, mass)
    return np.round(totalForce * v / eta, 2)

weeks = 75
week = []
ride = []
weight = []
grade = []
dist, d_low, d_high = [], 25, 50
speed, s_low, s_high = [], 15, 35
power, p_low, p_high = [], 80, 180
weights = np.flip(np.sort(np.random.uniform(low=64, high=71, size=(75,)))).tolist()
n_ride = 0


for we in range(weeks):
    mass    = weights[we] + 7.5
    rides   = np.random.choice([1,2,3,4,5], p = [0.03, 0.2, 0.5, 0.2, 0.07])
    grads   = np.random.choice([0,1,2,3,4,5,6,7], size=rides, p = ([0.5, 0.2, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0] if we < 50 else [0.1, 0.05, 0.05, 0.1, 0.1, 0.2, 0.2, 0.2]))

    for ri in range(rides):
        n_ride += 1
        gr = grads[ri]
        di = np.random.uniform(d_low*(1-(0.1*gr)), d_high*(1-(0.1*gr)))
        sp = (np.random.uniform(s_low, s_high))
        possible = False
        while not possible:
            po = getPower(mass, sp, gr) 
            if po > p_high:
                sp -= 1
            elif po < p_low:
                sp += 1
            else:
                possible = True
        
        week.append(we+1)
        ride.append(n_ride)
        weight.append(weights[we])
        dist.append(di)
        grade.append(gr)
        speed.append(sp)
        power.append(po)
    
    if we != 0:
        if we % 3 == 0:
            if d_low < 50:
                d_low += 5
            if d_high < 160: 
                d_high += 5

        if we < 25:
            if we % 2 == 0:
                    s_low += 0.05
                    s_high += 0.1
                    p_low += 2
                    p_high += 4
        if 25 <= we < 50:
            if we % 2 == 0:
                    s_low += 0.1
                    s_high += 0.25
                    p_low += 4
                    p_high += 5
        if 50 <= we < 70:
            if we % 2 == 0:
                    s_low += 0.25
                    s_high += 0.30
                    p_low += 3
                    p_high += 4
        if we >= 70:
            if we % 2 == 0:
                    s_low += 0.1
                    s_high += 0.15
                    p_low += 1
                    p_high += 1

cycling = pd.DataFrame()

cycling['week']         = pd.Series(week)
cycling['ride']         = pd.Series(ride)
cycling['distance']     = pd.Series(dist).round(2)
cycling['speed (avg)']  = pd.Series(speed).round(2)
cycling['gradient (avg)'] = pd.Series(grade).round(0)
cycling['power (avg)']  = pd.Series(power).round(2)
cycling['weight (kg)']  = pd.Series(weight).round(2)
cycling['w/kg']         = (cycling['power (avg)']/cycling['weight (kg)']).round(2)

cycling.to_csv('cycling_progress.csv')