""" test to see if runmodel functions as expected """

from beans.run_model import runmodel
from beans.burstrain import *
import numpy as np
from beans.get_data import get_obs
import pathlib

def test_run_model():

    numburstssim = 3 # this needs to be an integer value of half the number of bursts you want to simulate. I.e. simulate this many from the reference burst in either direction. Don't forget to account for missed bursts!
    numburstsobs = 4  # number of observed bursts in your dataset
    numburstssim = 3

    theta = 0.5, 0.015, 0.2, 2.1, 3.5, 0.108, 0.90, 0.5, 1.4, 11.2

    path_to_data_file_obs = (
            pathlib.Path(__file__).resolve().parent.parent / "data" / "1808_obs.txt"
        )

    path_to_data_file_bursts = (
            pathlib.Path(__file__).resolve().parent.parent / "data" / "1808_bursts.txt"
        )

    path_to_data_file_gti = (
            pathlib.Path(__file__).resolve().parent.parent / "data" / "1808_gti.txt"
        )


    bstart, fluen, obs, obs_err, pflux, pfluxe, tobs, st, et = get_obs(ref_ind=1, bc=2.21, gti_checking=1, obsname=path_to_data_file_obs, burstname=path_to_data_file_bursts, gtiname=path_to_data_file_gti)

    ref_ind = 1
    tref = bstart[ref_ind]
    gti_checking =1
    # this is for emcee:
    y = obs
    yerr = obs_err
    x = 0 # in our case, we do not require x (independent variables), however for input into MCMC we need to define a x

    test, valid = runmodel(theta,y,tref,bstart,pflux, pfluxe, tobs,numburstssim,ref_ind,gti_checking)

    exp = [  0.37596756  , 2.57382977 ,  3.6951732  ,  5.22042564 ,  5.49339669, 5.76917402  , 7.5398804  ,129.9739876,  139.81100404 ,155.46956035]

    result = np.allclose(test, exp)

    assert result

    return