"""
The ``write_scec`` module contains several functions useful for converting binary output from a
simulation to the text file format used by the SCEC Rupture Code Verification group. Functions are
written for on fault, off fault, and front data types, and there are versions for both 2D and 3D
problems. The functions take several common optional arguments, including ``depthsign`` (indicates
whether depth is positive or negative), ``author`` (the person who is submitting the results),
``version`` (the code version used to run the simulation), and ``grid_spacing`` (the resolution
of the simulation, in the event you are submitting data for multiple grid spacings).

Each function writes a text file in the current directory following the file naming convention used
by the server for the Code Verification group. More information on the file outputs are given
in the documentation for each function.
"""

import numpy as np
import fdfault
import datetime
from scipy.integrate import cumtrapz

def write_off_fault(problem, station, depthsign = 1., author = "", version = "", grid_spacing = ""):
    """
    Converts code output units for off-fault station from a 3D simulation into a formatted text file
    for SCEC website

    This function converts off fault data from binary (written by the C++ code) to ASCII text
    for a 3D benchmark simulation. Required inputs are the problem name (string) and station
    (tuple of strings in the format ``(strike, across, depth)``). Optional inputs include depthsign
    (1. by default, changes sign on depth coordinate if -1.), and author, verision, and grid spacing
    strings which will be inserted into the header of the output file.
    
    The text file is written to ``{problem}_body{across}st{strike}dp{depth}.txt`` in the current
    directory.

    :param problem: Problem name to write to file
    :type problem: str
    :param station: Coordinates in 3D of output station (tuple of 3 strings)
    :type station: tuple
    :param depthsign: Sign of depth output, must be ``1.`` or ``-1.`` (optional, default is ``1.``)
    :type depthsign: float
    :param author: Person who ran the simulation (optional, default is ``""``)
    :type author: str
    :param version: Code version used in simulation (optional, default is ``""``)
    :type version: str
    :param grid_spacing: Grid spacing used in simulation (optional, default is ``""``)
    :type grid_spacing: str
    :returns: None
    """

    stationstr = 'body'+station[1]+'st'+station[0]+'dp'+station[2]

    h_vel = fdfault.output(problem,stationstr+'-h-vel')
    h_vel.load()
    n_vel = fdfault.output(problem,stationstr+'-n-vel')
    n_vel.load()
    v_vel = fdfault.output(problem,stationstr+'-v-vel')
    v_vel.load()

    assert(h_vel.nt == v_vel.nt)
    assert(h_vel.nt == n_vel.nt)
    assert(depthsign == 1. or depthsign == -1.)

    h_disp = cumtrapz(h_vel.vx, h_vel.t, initial=0.)
    n_disp = cumtrapz(n_vel.vy, n_vel.t, initial=0.)
    v_disp = cumtrapz(v_vel.vz, v_vel.t, initial=0.)

    f = open(problem+'_'+stationstr+'.txt','w')

    f.write('# problem='+problem+'\n')
    f.write('# author='+author+'\n')
    f.write('# date='+datetime.date.today().strftime("%y/%m/%d")+"\n")
    f.write('# code=fdfault\n')
    f.write('# version='+version+'\n')
    f.write('# element_size='+grid_spacing+'\n')
    f.write('# time_step='+str(h_vel.t[1]-h_vel.t[0])+' s\n')
    f.write('# num_time_steps='+str(h_vel.nt)+'\n')
    f.write('# location='+str(h_vel.x)+' km strike, '+str(h_vel.y)+' km across, '+
            str(depthsign*h_vel.z)+' km depth\n')
    f.write('# Column #1 = Time (s)\n')
    f.write('# Column #2 = horizontal displacement (m)\n')
    f.write('# Column #3 = horizontal velocity (m/s)\n')
    f.write('# Column #4 = vertical displacement (m)\n')
    f.write('# Column #5 = vertical velocity (m/s)\n')
    f.write('# Column #6 = normal displacement (m)\n')
    f.write('# Column #7 = normal velocity (m/s)\n')
    f.write('#\n')
    f.write('t h-disp h-vel v-disp v-vel n-disp n-vel\n')
    f.write('#\n')

    for i in range(h_vel.nt):
        f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(h_vel.t[i], h_disp[i], h_vel.vx[i],
                                                               depthsign*v_disp[i], depthsign*v_vel.vz[i], n_disp[i], n_vel.vy[i]))

    f.close()

def write_off_fault_2d(problem, station, depthsign = 1., author = "", version = "", grid_spacing = ""):
    """
    Converts code output units for off-fault station into a formatted text file for SCEC website

    This function converts off fault data from binary (written by the C++ code) to ASCII text
    for a 3D benchmark simulation. Required inputs are the problem name (string) and station
    (tuple of strings in the format ``(strike, across, depth)``). Optional inputs include depthsign
    (1. by default, changes sign on depth coordinate if -1.), and author, verision, and grid spacing
    strings which will be inserted into the header of the output file.
    
    The text file is written to ``{problem}_body{across}st{strike}dp{depth}.txt`` in the current
    directory.

    :param problem: Problem name to write to file
    :type problem: str
    :param station: Coordinates in 2D of output station (tuple of 3 strings, but ``strike`` should be ``'0'``)
    :type station: tuple
    :param depthsign: Sign of depth output, must be ``1.`` or ``-1.`` (optional, default is ``1.``)
    :type depthsign: float
    :param author: Person who ran the simulation (optional, default is ``""``)
    :type author: str
    :param version: Code version used in simulation (optional, default is ``""``)
    :type version: str
    :param grid_spacing: Grid spacing used in simulation (optional, default is ``""``)
    :type grid_spacing: str
    :returns: None
    """

    stationstr = 'body'+station[1]+'st'+station[0]+'dp'+station[2]

    n_vel = fdfault.output(problem,stationstr+'-n-vel')
    n_vel.load()
    v_vel = fdfault.output(problem,stationstr+'-v-vel')
    v_vel.load()

    assert(n_vel.nt == v_vel.nt)
    assert(depthsign == 1. or depthsign == -1.)

    n_disp = cumtrapz(n_vel.vx, n_vel.t, initial=0.)
    v_disp = cumtrapz(v_vel.vy, v_vel.t, initial=0.)

    f = open(problem+'_'+stationstr+'.txt','w')

    f.write('# problem='+problem+'\n')
    f.write('# author='+author+'\n')
    f.write('# date='+datetime.date.today().strftime("%y/%m/%d")+"\n")
    f.write('# code=fdfault\n')
    f.write('# version='+version+'\n')
    f.write('# element_size='+grid_spacing+'\n')
    f.write('# time_step='+str(v_vel.t[1]-v_vel.t[0])+' s\n')
    f.write('# num_time_steps='+str(v_vel.nt)+'\n')
    f.write('# location= 0 km strike, '+str(v_vel.x)+' km across, '+
            str(depthsign*v_vel.y)+' km depth\n')
    f.write('# Column #1 = Time (s)\n')
    f.write('# Column #2 = horizontal displacement (m)\n')
    f.write('# Column #3 = horizontal velocity (m/s)\n')
    f.write('# Column #4 = vertical displacement (m)\n')
    f.write('# Column #5 = vertical velocity (m/s)\n')
    f.write('# Column #6 = normal displacement (m)\n')
    f.write('# Column #7 = normal velocity (m/s)\n')
    f.write('#\n')
    f.write('t h-disp h-vel v-disp v-vel n-disp n-vel\n')
    f.write('#\n')

    for i in range(v_vel.nt):
        f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(v_vel.t[i], 0., 0.,
                                                               depthsign*v_disp[i], depthsign*v_vel.vy[i], n_disp[i], n_vel.vx[i]))

    f.close()

def write_on_fault(problem, station, depthsign = 1., normal = True, author = "",
                   version = "", grid_spacing = ""):
    """
    Converts code output units for on-fault station into a formatted text file for SCEC website

    This function converts on fault data from binary (written by the C++ code) to ASCII text
    for a 3D benchmark simulation. Required inputs are the problem name (string) and station
    (tuple of strings in the format ``(strike, depth)``). Optional inputs include depthsign
    (1. by default, changes sign on depth coordinate if -1.), and author, verision, and grid spacing
    strings which will be inserted into the header of the output file.
    
    The text file is written to ``{problem}_faultst{strike}dp{depth}.txt`` in the current
    directory.

    :param problem: Problem name to write to file
    :type problem: str
    :param station: Coordinates of output station (tuple of 2 strings for strike and depth coordinates)
    :type station: tuple
    :param depthsign: Sign of depth output, must be ``1.`` or ``-1.`` (optional, default is ``1.``)
    :type depthsign: float
    :param author: Person who ran the simulation (optional, default is ``""``)
    :type author: str
    :param version: Code version used in simulation (optional, default is ``""``)
    :type version: str
    :param grid_spacing: Grid spacing used in simulation (optional, default is ``""``)
    :type grid_spacing: str
    :returns: None
    """

    stationstr = 'faultst'+station[0]+'dp'+station[1]

    h_slip = fdfault.output(problem,stationstr+'-h-slip')
    h_slip.load()
    h_slip_rate = fdfault.output(problem,stationstr+'-h-slip-rate')
    h_slip_rate.load()
    h_shear_stress = fdfault.output(problem,stationstr+'-h-shear-stress')
    h_shear_stress.load()
    v_slip = fdfault.output(problem,stationstr+'-v-slip')
    v_slip.load()
    v_slip_rate = fdfault.output(problem,stationstr+'-v-slip-rate')
    v_slip_rate.load()
    v_shear_stress = fdfault.output(problem,stationstr+'-v-shear-stress')
    v_shear_stress.load()

    assert(h_slip.nt == h_slip_rate.nt)
    assert(h_slip.nt == h_shear_stress.nt)
    assert(h_slip.nt == v_slip.nt)
    assert(h_slip.nt == v_slip_rate.nt)
    assert(h_slip.nt == v_shear_stress.nt)
    assert(depthsign == 1. or depthsign == -1.)

    if normal:
        n_stress = fdfault.output(problem,stationstr+'-n-stress')
        n_stress.load()        

    f = open(problem+'_'+stationstr+'.txt','w')

    f.write('# problem='+problem+'\n')
    f.write('# author='+author+'\n')
    f.write('# date='+datetime.date.today().strftime("%y/%m/%d")+"\n")
    f.write('# code=fdfault\n')
    f.write('# version='+version+'\n')
    f.write('# element_size='+grid_spacing+'\n')
    f.write('# time_step='+str(h_slip.t[1]-h_slip.t[0])+' s\n')
    f.write('# num_time_steps='+str(h_slip.nt)+'\n')
    f.write('# location='+str(h_slip.x)+' km strike, '+str(h_slip.y)+' km across, '+
            str(depthsign*h_slip.z)+' km depth\n')
    f.write('# Column #1 = Time (s)\n')
    f.write('# Column #2 = horizontal slip (m)\n')
    f.write('# Column #3 = horizontal slip rate (m/s)\n')
    f.write('# Column #4 = horizontal shear stress (MPa)\n')
    f.write('# Column #5 = vertical slip (m)\n')
    f.write('# Column #6 = vertical slip rate (m/s)\n')
    f.write('# Column #7 = vertical shear stress (MPa)\n')
    if normal:
        f.write('# Column #8 = normal stress (MPa)\n')
    f.write('#\n')
    if normal:
        f.write('t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress\n')
    else:
        f.write('t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress\n')
    f.write('#\n')

    for i in range(h_slip.nt):
        if normal:
            f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(h_slip.t[i], h_slip.Ux[i], h_slip_rate.Vx[i],
                                                               h_shear_stress.Sx[i], v_slip.Uz[i], v_slip_rate.Vz[i],
                                                                     v_shear_stress.Sz[i], n_stress.Sn[i]))
        else:
            f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(h_slip.t[i], h_slip.Ux[i], h_slip_rate.Vx[i],
                                                               h_shear_stress.Sx[i], v_slip.Uz[i], v_slip_rate.Vz[i],
                                                                     v_shear_stress.Sz[i]))

    f.close()

def write_on_fault_2d(problem, station, depthsign = 1., normal = True, author = "",
                   version = "", grid_spacing = ""):
    """
    Converts code output units for on-fault station into a formatted text file for SCEC website

    This function converts on fault data from binary (written by the C++ code) to ASCII text
    for a 2D benchmark simulation. Required inputs are the problem name (string) and station
    (tuple of strings in the format ``(strike, depth)``, with values chosen appropriately for a 2D
    simulation). Optional inputs include depthsign (1. by default, changes sign on depth
    coordinate if -1.), and author, verision, and grid spacing strings which will be inserted into the
    header of the output file.
    
    The text file is written to ``{problem}_faultst{strike}dp{depth}.txt`` in the current
    directory.

    :param problem: Problem name to write to file
    :type problem: str
    :param station: Coordinates of output station (tuple of 2 strings for strike and depth coordinates)
    :type station: tuple
    :param depthsign: Sign of depth output, must be ``1.`` or ``-1.`` (optional, default is ``1.``)
    :type depthsign: float
    :param author: Person who ran the simulation (optional, default is ``""``)
    :type author: str
    :param version: Code version used in simulation (optional, default is ``""``)
    :type version: str
    :param grid_spacing: Grid spacing used in simulation (optional, default is ``""``)
    :type grid_spacing: str
    :returns: None
    """

    stationstr = 'faultst'+station[0]+'dp'+station[1]

    v_slip = fdfault.output(problem,stationstr+'-v-slip')
    v_slip.load()
    v_slip_rate = fdfault.output(problem,stationstr+'-v-slip-rate')
    v_slip_rate.load()
    v_shear_stress = fdfault.output(problem,stationstr+'-v-shear-stress')
    v_shear_stress.load()

    assert(v_slip.nt == v_slip_rate.nt)
    assert(v_slip.nt == v_shear_stress.nt)
    assert(depthsign == 1. or depthsign == -1.)

    if normal:
        n_stress = fdfault.output(problem,stationstr+'-n-stress')
        n_stress.load()        

    f = open(problem+'_'+stationstr+'.txt','w')

    f.write('# problem='+problem+'\n')
    f.write('# author='+author+'\n')
    f.write('# date='+datetime.date.today().strftime("%y/%m/%d")+"\n")
    f.write('# code=fdfault\n')
    f.write('# version='+version+'\n')
    f.write('# element_size='+grid_spacing+'\n')
    f.write('# time_step='+str(v_slip.t[1]-v_slip.t[0])+' s\n')
    f.write('# num_time_steps='+str(v_slip.nt)+'\n')
    f.write('# location= 0 km strike, '+str(v_slip.x)+' km across, '+
            str(depthsign*v_slip.y)+' km depth\n')
    f.write('# Column #1 = Time (s)\n')
    f.write('# Column #2 = horizontal slip (m)\n')
    f.write('# Column #3 = horizontal slip rate (m/s)\n')
    f.write('# Column #4 = horizontal shear stress (MPa)\n')
    f.write('# Column #5 = vertical slip (m)\n')
    f.write('# Column #6 = vertical slip rate (m/s)\n')
    f.write('# Column #7 = vertical shear stress (MPa)\n')
    if normal:
        f.write('# Column #8 = normal stress (MPa)\n')
    f.write('#\n')
    if normal:
        f.write('t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress n-stress\n')
    else:
        f.write('t h-slip h-slip-rate h-shear-stress v-slip v-slip-rate v-shear-stress\n')
    f.write('#\n')

    for i in range(v_slip.nt):
        if normal:
            f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(v_slip.t[i], 0., 0.,
                                                               0., depthsign*v_slip.Uy[i], depthsign*v_slip_rate.Vy[i],
                                                                     depthsign*v_shear_stress.Sy[i], n_stress.Sn[i]))
        else:
            f.write("{:.12E} {:E} {:E} {:E} {:E} {:E} {:E}\n".format(v_slip.t[i], 0., 0.,
                                                               0., depthsign*v_slip.Uy[i], depthsign*v_slip_rate.Vy[i],
                                                                     depthsign*v_shear_stress.Sy[i]))

    f.close()

def write_front(problem, iface = 0, depthsign = 1., author = "", version = "", grid_spacing = ""):
    """
    Converts code output units for rupture front times into a formatted text file for SCEC website

    This function converts rupture time data from binary (written by the C++ code) to ASCII text
    for a 3D benchmark simulation. Required inputs are the problem name (string). Optional
    inputs include the interface to write to file (default is ``0``), depthsign (1. by default, changes
    sign on depth coordinate if -1.), and author, verision, and grid spacing strings which will be
    inserted into the header of the output file.
    
    The text file is written to ``{problem}_cplot.txt`` in the current
    directory.

    :param problem: Problem name to write to file
    :type problem: str
    :param iface: Interface to be written to file (default is ``0``)
    :type station: int
    :param depthsign: Sign of depth output, must be ``1.`` or ``-1.`` (optional, default is ``1.``)
    :type depthsign: float
    :param author: Person who ran the simulation (optional, default is ``""``)
    :type author: str
    :param version: Code version used in simulation (optional, default is ``""``)
    :type version: str
    :param grid_spacing: Grid spacing used in simulation (optional, default is ``""``)
    :type grid_spacing: str
    :returns: None
    """

    assert(depthsign == 1. or depthsign == -1.)

    frt = fdfault.front(problem, iface)
    frt.load()

    f = open(problem+'_'+'cplot.txt','w')

    f.write('# problem='+problem+'\n')
    f.write('# author='+author+'\n')
    f.write('# date='+datetime.date.today().strftime("%y/%m/%d")+"\n")
    f.write('# code=fdfault\n')
    f.write('# version='+version+'\n')
    f.write('# element_size='+grid_spacing+'\n')
    f.write('# Column #1 = horizontal coordinate, distance along strike (m)\n')
    f.write('# Column #2 = vertical coordinate, distance down-dip (m)\n')
    f.write('# Column #3 = rupture time (s)\n')
    f.write('#\n')
    f.write('j k t\n')
    f.write('#\n')

    for i in range(frt.nx):
        for j in range(frt.ny):
            if (frt.t[i,j] < 0.):
                f.write("{:E} {:E} {:E}\n".format(frt.x[i,j]*1000., depthsign*frt.z[i,j]*1000., 1.e9))
            else:
                f.write("{:E} {:E} {:E}\n".format(frt.x[i,j]*1000., depthsign*frt.z[i,j]*1000., frt.t[i,j])) 

    f.close()

    
