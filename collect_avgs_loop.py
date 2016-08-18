#! /usr/bin/env python2

'''Loop over several data sets taking averages and saving them'''

from __future__ import division # make float division the default
import sys
import os.path
############# Edit with proper VisIt path!!! #############
sys.path.append("C:\Program Files\LLNL\VisIt 2.10.2\lib\site-packages")
#############
from visit import *
# visit_utils has several nice helper functions, among them "query" which just
#   returns the numerical output of Query.
from visit_utils import *
import numpy as np

# z ranges from -0.5 to 0.5
z_min = -0.5
z_max = 0.4
z_step = 0.005

def main():
    
    # loop over naming schemes
    for ll in [10,20,30,40]:
        
        path_to_dumps = \
            r"MacrophyteData\viz_IB3d_4towers_Re0.2_len{}\dumps.visit".format(ll)
        assert os.path.isfile(path_to_dumps)
        out_file = \
            r"MacrophyteAvgs\viz_IB3d_4towers_Re0.2_len{}_avgs.txt".format(ll)
        
        # get averages from data
        
        ### This bit just sets a default view of some sort... not really sure ###
        # (I just dumped this straigt in from recording it in VisIt)
        # Begin spontaneous state
        View2DAtts = View2DAttributes()
        View2DAtts.windowCoords = (0, 1, 0, 1)
        View2DAtts.viewportCoords = (0.2, 0.95, 0.15, 0.95)
        View2DAtts.fullFrameActivationMode = View2DAtts.Auto  # On, Off, Auto
        View2DAtts.fullFrameAutoThreshold = 100
        View2DAtts.xScale = View2DAtts.LINEAR  # LINEAR, LOG
        View2DAtts.yScale = View2DAtts.LINEAR  # LINEAR, LOG
        View2DAtts.windowValid = 0
        SetView2D(View2DAtts)
        # End spontaneous state
        
        ### Get a nice angle to watch the data collection if window is not off ###
        # (I just dumped this straigt in from recording it in VisIt)
        View3DAtts = View3DAttributes()
        View3DAtts.viewNormal = (-0.317367, -0.833752, 0.451814)
        View3DAtts.focus = (0, 0, 0)
        View3DAtts.viewUp = (0.0539949, 0.459785, 0.886387)
        View3DAtts.viewAngle = 30
        View3DAtts.parallelScale = 0.53033
        View3DAtts.nearPlane = -1.06066
        View3DAtts.farPlane = 1.06066
        View3DAtts.imagePan = (0, 0)
        View3DAtts.imageZoom = 1
        View3DAtts.perspective = 1
        View3DAtts.eyeAngle = 2
        View3DAtts.centerOfRotationSet = 0
        View3DAtts.centerOfRotation = (0, 0, 0)
        View3DAtts.axis3DScaleFlag = 0
        View3DAtts.axis3DScales = (1, 1, 1)
        View3DAtts.shear = (0, 0, 1)
        View3DAtts.windowValid = 1
        SetView3D(View3DAtts)

        ### Open data, plot x-magnitude, add slice ###
        OpenDatabase("localhost:"+path_to_dumps, 0) #opens data to first time step
        last_time = TimeSliderGetNStates() - 1 #returns the number of time slider states
                                               #   subtract 1 for base 0
        SetTimeSliderState(last_time)
        # Define some new variables
        DefineScalarExpression("U_x_abs", "abs(<U_x>)") # abs of U in x direction
        DefineScalarExpression("U_y_abs", "abs(<U_y>)")
        DefineScalarExpression("U_z_abs", "abs(<U_z>)")
        AddPlot("Pseudocolor", "U_x_abs")
        AddOperator("Slice", 0) # the 0 here means "apply operator only to this plot"
        SetActivePlots(1) # there are two plots now, since levels is auto added

        ### Set slice attributes ###
        SliceAtts = SliceAttributes()
        # Specify the origin via intercept
        SliceAtts.originType = SliceAtts.Intercept  # Point, Intercept, Percent, Zone, Node
        SliceAtts.originPoint = (0, 0, 0)
        SliceAtts.originIntercept = z_min # This is where on the Z Axis we are!
        SliceAtts.originPercent = 0
        SliceAtts.originZone = 0
        SliceAtts.originNode = 0
        SliceAtts.normal = (0, 0, 1)
        # Set plane orthogonal to the Z Axis
        SliceAtts.axisType = SliceAtts.ZAxis  # XAxis, YAxis, ZAxis, Arbitrary, ThetaPhi
        SliceAtts.upAxis = (0, 1, 0)
        SliceAtts.project2d = 0 # Turn off 2D projection!
        SliceAtts.interactive = 1
        SliceAtts.flip = 0
        SliceAtts.originZoneDomain = 0
        SliceAtts.originNodeDomain = 0
        SliceAtts.meshName = "amr_mesh"
        SliceAtts.theta = 0
        SliceAtts.phi = 90
        SetOperatorOptions(SliceAtts, 0) # Apply Slice settings
        DrawPlots() # Draw the plot
        
        z_mesh = np.arange(z_min,z_max+z_step,z_step)
        
        ### Loop over Z-Axis collecting X averages ###
        x_abs_avgs = []
        for val in z_mesh:
            SliceAtts.originIntercept = val
            SetOperatorOptions(SliceAtts, 0) # Operator number 0
            DrawPlots()
            # Get the average value and store it
            x_abs_avgs.append(query("Average Value"))
        x_abs_avgs = np.array(x_abs_avgs) # convert to numpy array
        # Delete this plot since we are done with it
        DeleteActivePlots()

        ### Add y average plot ###
        AddPlot("Pseudocolor", "U_y_abs")
        AddOperator("Slice", 0) # the 0 here means "apply operator only to this plot"
        SetActivePlots(1)

        ### Loop over Z-Axis collecing Y averages ###
        y_abs_avgs = []
        for val in z_mesh:
            SliceAtts.originIntercept = val
            SetOperatorOptions(SliceAtts, 0) # Operator number 0
            DrawPlots()
            # Get the average value and store it
            y_abs_avgs.append(query("Average Value"))
        y_abs_avgs = np.array(y_abs_avgs) # convert to numpy array
        # Delete this plot since we are done with it
        DeleteActivePlots()

        ### Add z average plot ###
        AddPlot("Pseudocolor", "U_z_abs")
        AddOperator("Slice", 0) # the 0 here means "apply operator only to this plot"
        SetActivePlots(1)

        ### Loop over Z-Axis collecing Z averages ###
        z_abs_avgs = []
        for val in z_mesh:
            SliceAtts.originIntercept = val
            SetOperatorOptions(SliceAtts, 0) # Operator number 0
            DrawPlots()
            # Get the average value and store it
            z_abs_avgs.append(query("Average Value"))
        z_abs_avgs = np.array(z_abs_avgs) # convert to numpy array
        # Delete this plot since we are done with it
        DeleteActivePlots()

        ### Calculate dp/dx ###
        DefineScalarExpression("dpdx", "gradient(<P>)[0]")

        ### Get average value of dpdx ###
        AddPlot("Pseudocolor","dpdx")
        SetActivePlots(1)
        DrawPlots()
        dpdx_avg = query("Average Value")

        ### Save averages ###
        np.savetxt(out_file,np.vstack([np.array(z_mesh),
                            x_abs_avgs,y_abs_avgs,z_abs_avgs]))
        with open(out_file[:-8]+'dpdx.txt','w') as fobj:
            fobj.write(str(dpdx_avg))        
                            
        print('Data saved to {}'.format(out_file)+' and {}'.format(
            out_file[:-8]+'dpdx.txt'))
        
        DeleteAllPlots()
        CloseDatabase("localhost:"+path_to_dumps)
        
        
        
        
if __name__ == '__main__':
    Launch()
    main()