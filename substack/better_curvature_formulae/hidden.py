#!/usr/bin/python3
'''
calculate height hidden by curve
'''
import sys, os, logging  # pylint: disable=multiple-imports
from math import sqrt, sin, cos

# "standard" values from metabunk's calculator
RADIUS = 3959  # standard value for earth's radius
REFRACTION = 7 / 6  # multiply by radius to get virtual radius
V_RADIUS = RADIUS * REFRACTION
FEET_PER_MILE = 5280

logging.basicConfig(level=logging.DEBUG if __debug__ else logging.INFO)

def parabolic(distance, height=None, radius=RADIUS):
    '''
    usual way flat earth proponents estimate the curve

    it doesn't account for observer height nor for atmospheric refraction

    it's the formula x~=(d-sqrt(2rh))**2/2r with h=0, yielding d**2/2r
    since we're using R=RADIUS, d expressed in miles, and returning feet
    of hidden height, 2r=7918, and 1/7918*5280=.667; so, simplified,
    feet of hidden height is about 2/3 d squared
    '''
    logging.debug('calculating hidden height using parabolic formula')
    distance = float(distance)  # in case string passed in from shell
    height = float(height or 0)
    radius = int(radius)
    logstring = ('returning hidden height in feet for distance=%.02f miles,'
                 ' observer height=%.02f feet, radius=%.01f miles')
    logging.info(logstring, distance, height, radius)
    height = height / FEET_PER_MILE  # same unites for all values
    hidden = (distance - sqrt(2 * radius * height)) ** 2 / (2 * radius)
    return hidden * FEET_PER_MILE  # back to feet for result

def refracted_parabolic(distance, height=None, radius=V_RADIUS):
    '''
    parabolic formula, but using standard refraction value
    '''
    return parabolic(distance, height, radius)

hidden = parabolic  # default function

if __name__ == '__main__':
    logging.debug('sys.argv before modification: %s', sys.argv)
    if len(sys.argv) >= 1:
        COMMAND = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    elif len(sys.argv) >= 2:
        if sys.argv[1].isdigit():
            sys.argv.insert(1, 'DEFAULT')
        else:
            COMMAND = sys.argv[1]
    logging.debug('sys.argv after modification: %s', sys.argv)
    print(eval(COMMAND)(*sys.argv[1:]))  # pylint: disable=eval-used
