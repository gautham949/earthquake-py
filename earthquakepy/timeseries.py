import numpy as np
from .singledof import *


class TimeSeries:
    '''
    TimeSeries object class
    Defines time series
    '''
    def __init__(self, t, y):
        '''
        Time series object initiation with
        t and y as lists or 1D arrays.
        If t is a scalar, then the array is
        autogenerated with scalar value as dt.
        '''
        if (type(t) == float) or (type(t) == int):
            t = np.arange(0.0, len(y)*t-1E-5*t, t)
        self.t = t
        self.y = y

    def __repr__(self):
        a = ""
        for key, val in vars(self).items():
            a += "{:10s}:{}\n".format(key, val)
        return a

    def set_tunit(self, unit):
        '''
        Set unit for T(time) coordinates.
        Unit should be a string.
        '''
        self.tunit = unit

    def set_yunit(self, unit):
        '''
        Set unit for y coordinates.
        Unit should be a string.
        '''
        self.yunit = unit

    def set_t(self, coords):
        '''
        Set T(time) coordinates.
        Should be a list or numpy array (1D)
        '''
        self.t = coords

    def set_eqname(self, name):
        ''' Set earthquake name '''
        self.eqName = name

    def set_eqdate(self, date):
        ''' Set earthquake date '''
        self.eqDate = date

    def set_station(self, station):
        ''' Recording station '''
        self.station = station

    def set_component(self, comp):
        ''' Directional component of record '''
        self.component = comp

    def set_dt(self, dt):
        ''' Time step between data points '''
        self.dt = dt

    def set_npts(self, npts):
        ''' Total number of points in the record '''
        self.npts = npts

    def set_filepath(self, filepath):
        ''' Record filepath '''
        self.filepath = filepath

    def get_response_spectra(self, T=np.arange(0.1, 20.01, 1.0), xi=0.05):
        """
        Calculates linear elastic response spectra associated with the timeseries.
        Inputs:
        Tstart and Tend (floats): Periods corresponding to spectrum width
        dT (float): Step size for period
        xi (float): damping ratio
        """
        specLength = len(T)
        Sd = np.empty(specLength)
        for i in range(specLength):
            s = Sdof(T=T[i], xi=xi)
            r = s.get_response(self, tsType="baseExcitation")
            D = np.max(np.abs(r.y[0]))
            Sd[i] = D
            # Sv = (2*np.pi/T)*Sd
            # Sa = (2*np.pi/T)*Sv
        return ResponseSpectra(T, Sd)


class ResponseSpectra:
    def __init__(self, T, Sd):
        """
        Class for storing response spectra
        Inputs:
        T (array of float): Natural period
        Sd, Sv(not implemented), Sa(not implemented) (array of float): Spectral displacement, velocity and acceleration, respectively.
        """
        self.T = T
        self.Sd = Sd
        # self.Sv = Sv
        # self.Sa = Sa
