"""
Test full area prediction mode runner.

"""
import pytest
import math
import numpy as np

from itmlogic.misc.qerfi import qerfi
from itmlogic.preparatory_subroutines.qlra import qlra
from itmlogic.lrprop import lrprop
from itmlogic.statistics.avar import avar


def test_itmlogic_area():
    """
    Test the model in area prediction mode.

    """
    prop = {}

    #Antenna height 1 (m), Antenna height 2 (m)
    prop['hg'] = [3.3, 1.3]

    #Frequency (MHz)
    prop['fmhz'] = 20

    #Terrain irregularity parameter dh (m)
    prop['dh'] = 102

    #Surface refractivity (N-units)
    prop['ens0'] = 301

    #Relative permittivity of ground
    prop['eps'] = 15

    #Conductivity (S/m) of ground
    prop['sgm'] = 0.001

    #Climate selection (1=equatorial, 2=continental subtropical,
    #3=maritime subtropical, 4=desert, 5=continental temperate,
    #6=maritime temperate overland, 7=maritime temperate,
    #oversea (5 is the default)
    prop['klimx'] = 5

    #0 = horizontal polarization, 1 = vertical
    prop['ipol'] = 1

    #Mode of variability: Single Message=0, Accidental=1,
    #Mobile=2, Broadcast=3
    prop['mdvarx'] = 3

    #Percent of time requested for computation
    QT = [50]

    #Percent of locations requested for computation
    QL = [50]

    #Confidence levels of computation
    QC = [50, 90, 10]

    #Initial distance (km) for loop over range
    D0 = 10

    #Max distance 1 (km) for loop over range
    D1 = 150

    #Increment 1 (km) for loop over range
    DS1 = 10

    #Max distance 2 (km) for coarser loop over range (starts beyond D1)
    D2 = 500

    #Increment 2 (km) for coarser loop over range
    DS2 = 50

    #Siting criterion for antenna 1, 0=random, 1= careful, 2= very careful
    KST = [2, 2]

    #Refractivity scaling ens=ens0*exp(-zsys/9460.);
    #(Average system elev above sea level)
    zsys = 0


    #Rescale requested percentages into their corresponding normal distribution arguments
    ZT = qerfi([x / 100 for x in QT])[0]
    ZL = qerfi([x / 100 for x in QL])[0]
    ZC = qerfi([x / 100 for x in QC])

    #The number of confidence intervals requested
    NC = len(QC)

    #Don't allow negative distances
    if (D0 <= 0):
        D0 = DS1

    #Set initial distance to 2 km if D0<=0
    if (D0 <= 0):
        D0= 2

    #If final distance less than initial, only do one distance
    if (D1 <= D0) or (DS1 <= 0):
        ND = 1
        D1 = D0
    #Otherwise compute the number of distance points in the loop
    #and recompute the final distance using this grid
    else:
        DS = DS1
        ND = math.floor((D1 - D0) / DS + 1.75)
        D1 = D0 + (ND - 1) * DS

    #Repeat these corrections for the "coarse" grid in range that follows the fine grid
    if (D2 <= D1 ) or ( DS2 <= 0):
        NDC = 0 #If input parameters are wrong, don't do a coarse grid
    #Otherwise set up appropriate coarse grid
    else:
        NDC = ND
        ND = math.floor((D2 - D1) / DS2 + 0.75)
        D2 = D1 + ND * DS2
        ND = NDC + ND

    #Standard Earth curvature parameter
    prop['gma'] = 157E-9
    #Scale factor for converting Np/km to dB/km
    DB = 8.685890
    #Scale factor to convert km to m
    AKM = 1000

    #Initialize error flag to 0
    prop['kwx'] = 0
    #Initialize the omega_n parameter
    prop['wn'] = prop['fmhz'] / 47.7
    #Initialize the surface refractivity
    prop['ens']  = prop['ens0']

    #Adjust surface refractivity parameter if zsys set by user
    if (zsys != 0):
        prop['ens'] = prop['ens'] * math.exp(-zsys / 9460)

    #Implement refractive effects on Earth curvature
    prop['gme']  = prop['gma'] * (1 - 0.04665 * math.exp(prop['ens'] / 179.3))

    #Initialize lvar parameter (this is used when updating AVAR with new input parameters)
    prop['lvar'] = 0

    #Compute ground effective impedance zq parameter
    zq = complex(prop['eps'], 376.62 * prop['sgm'] / prop['wn'])

    #Compute ground effective impedance z parameter (horizontal pol)
    prop['zgnd'] = math.sqrt(zq.real - 1)

    #Compute ground effective impedance z parameter (vertical pol)
    if (prop['ipol'] != 0):
        prop['zgnd'] = prop['zgnd'] / zq

    #Qlra initializes all the required parameters for area-prediction mode given
    #siting type and other params already set in "prop"
    prop = qlra(KST, prop)

    #Starting distances for loop over range
    D = D0
    #First range step is that of the fine grid
    DT = DS

    FS = []
    DD = []

    output = []

    for JD in range(0, ND): #0-22

        #Ensure that AVAR routines adjust only for distance (not quantiles which are set)
        prop['lvar'] = max(1, prop['lvar'])

        #Compute baseline propagation loss at current range
        prop = lrprop(D * AKM, prop)

        #Compute and store baseline loss
        FS.append(DB * np.log(2 * prop['wn'] * prop['dist']))

        #Store distance at this increment
        DD.append(D)

        #Loop over confidence intervals requested by user
        for JC in range(0, NC): #0-3

            #Get confidence interval
            confidence_level = QC[JC]

            #Compute adjustment for specified confidence levels
            avar1, prop = avar(ZT, ZL, ZC[JC], prop)

            #Store results
            output.append({
                'distance_km': D,
                'confidence_level_%': confidence_level,
                'propagation_loss_dB': FS[JD] + avar1 #Add in the adjustment for this level
                })

        #Switch to the coarse grid increment in range when we get there
        if JD + 1 == NDC:
            DT = DS2

        #Increment range
        D = D + DT

    for result in output:
        if result['distance_km'] == 10 and result['confidence_level_%'] == 50:
            assert result['propagation_loss_dB'] == 111.69200844812511
        if result['distance_km'] == 10 and result['confidence_level_%'] == 90:
            assert result['propagation_loss_dB'] == 121.59437954264777
        if result['distance_km'] == 10 and result['confidence_level_%'] == 10:
            assert result['propagation_loss_dB'] == 101.78963735360244
        if result['distance_km'] == 500 and result['confidence_level_%'] == 50:
            assert result['propagation_loss_dB'] == 215.27421197676375
        if result['distance_km'] == 500 and result['confidence_level_%'] == 90:
            assert result['propagation_loss_dB'] == 221.71014370503855
        if result['distance_km'] == 500 and result['confidence_level_%'] == 10:
            assert result['propagation_loss_dB'] == 208.83828024848896
