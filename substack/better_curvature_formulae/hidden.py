#!/usr/bin/python3
'''
calculate height hidden by curve
'''
import sys, os, logging  # pylint: disable=multiple-imports
from math import sqrt, cos, acos

# "standard" values from metabunk's calculator
RADIUS = 3959  # standard value for earth's radius
REFRACTION = 7 / 6  # multiply by radius to get virtual radius
V_RADIUS = RADIUS * REFRACTION
FEET_PER_MILE = 5280

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

def hidden(distance, height=None, radius=RADIUS, formula='parabolic'):
    '''
    defaults to usual way flat earth proponents estimate the curve

    it doesn't account for observer height nor for atmospheric refraction

    it's the formula x~=(d-sqrt(2rh))**2/2r with h=0, yielding d**2/2r
    since we're using R=RADIUS, d expressed in miles, and returning feet
    of hidden height, 2r=7918, and 1/7918*5280=.667; so, simplified,
    feet of hidden height is about 2/3 d squared

    formula='spherical' uses metabunk.com's trigonometric calculation of
    hidden height: r(r+h)/(r*cos(theta)+sqrt(h(2r+h))*sin(theta))-r
    '''
    logging.debug('calculating hidden height using %s formula', formula)
    distance = float(distance)  # in case string passed in from shell
    height = float(height or 0)
    radius = float(radius)
    logstring = ('returning hidden height in feet for distance=%.02f miles,'
                 ' observer height=%.02f feet, radius=%.01f miles')
    logging.info(logstring, distance, height, radius)
    height = height / FEET_PER_MILE  # same units for all values
    # distance to horizon: straight-line tangent for parabolic,
    # arc length along the surface for spherical
    if formula == 'parabolic':
        horizon = sqrt(2 * radius * height)
    else:
        alpha = acos(radius / (radius + height))  # angle to horizon
        horizon = radius * alpha
    if distance <= horizon:
        return 0.0  # target base is on our side of the horizon
    if formula == 'parabolic':
        obscured = (distance - horizon) ** 2 / (2 * radius)
    else:
        # metabunk's r(r+h)/(r*cos(theta)+sqrt(h(2r+h))*sin(theta))-r
        # reduces to r/cos(theta-alpha)-r; theta is the angle subtended
        # by distance, assumed point to point on a smooth globe
        theta = distance / radius
        obscured = radius / cos(theta - alpha) - radius
    return obscured * FEET_PER_MILE  # back to feet for result

def refracted(distance, height=None, radius=V_RADIUS, formula='parabolic'):
    '''
    parabolic formula by default, but using standard refraction value
    '''
    return hidden(distance, height, radius, formula)

def spherical(distance, height=None, radius=V_RADIUS, formula='spherical'):
    '''
    no sense using non-refracted radius for spherical calculation
    '''
    return hidden(distance, height, radius, formula)

parabolic = hidden  # enable `parabolic` symlink

if __name__ == '__main__':
    logging.debug('sys.argv before modification: %s', sys.argv)
    COMMAND = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    if len(sys.argv) < 2 and COMMAND != 'hidden':
        logging.error('Usage: %s distance height', sys.argv[0])
        logging.info('Example: %s 10 5  # 10 miles away from 5 feet up',
                     sys.argv[0])
    elif COMMAND == 'hidden':
        for d in 1, 5, 10, 50, 100, 200, 500, 1000:
            for h in 0, 5, 100:
                for f in parabolic, spherical:
                    print(f(d, h))
    else:
        print(eval(COMMAND)(*sys.argv[1:]))  # pylint: disable=eval-used
