# CHART_L
Catchment-scale Hazard Assessment of Rainfall Triggered Landslides
CHART_L – Catchment-scale Hazard Assessment of Rainfall Triggered Landslides is a script implemented in GRASS GIS for estimating the hazard of rain-induced landslides at the catchment scale.
It takes into account the susceptibility to landslides (HL – Hazard Landslide), usually assessed at the basin scale using statistical techniques or Machine or Deep Learning taking into account geospatial predisposing factors intrinsic to the phenomenon, and the hazard triggered by rainfall (HR – Hazard Rainfall), assessed by defining rainfall thresholds. The overall hazard (CHART_L) of the area is expressed on a scale from 0 to 0.95, combining HR and HL.

Input data:

• Raster map of observed or forecasted rainfall, associated with a specific time period (1, 3, 6, 12, or 24 hours).

• Raster map of susceptibility to landslides; regardless of the methodology used to create it, it must be divided into 6 classes, representing the probability of occurrence as described below:
0 = very low (areas where a landslide is extremely unlikely to occur, e.g., flat areas or areas with a slope < 1° or built-up areas) 
1 = low 
2 = medium-low
3 = medium
4 = high
5 = very high

• Rain thresholds, entered via a .csv file or directly in the script window, formatted as follows:
Period,Max_1,Max_2,Max_3,Max_4
1,4,5,6,8
3,7,9,10,16
6,10,13,16,25
12,16,20,24,40
24,25,32,38,63
where:
- Period indicates the time for which the cumulative amount is considered (1, 3, 6, 12, and 24 hours, respectively); 
- Max_1, Max_2, Max_3, Max_4 indicate the threshold values between the 5 HR classes.

It is also necessary that the input maps have the same resolution and extension, or that the latter is determined using a mask. Furthermore, it may be advisable to exclude urbanized areas.

CHART_L estimation

Each landslide susceptibility class is assigned a hazard level (HL) value according to the following criteria:
Very low landslide susceptibility 	 = 0 => HL = 0
Low landslide susceptibility		 = 1 => HL = 0.3
Medium-low landslide susceptibility = 2 => HL = 0.45
Medium landslide susceptibility	 = 3 => HL = 0.6
High landslide susceptibility 		 = 4 => HL = 0.75
Very high landslide susceptibility 	 = 5 => HL = 0.95

Each rainfall threshold class, for a given duration, is assigned a hazard value HR, according to the following criteria:
rainfall < Max_1 		=> HR=0
Max_1 <= rainfall < Max_2 	=> HR=0.75
Max_2 <= rainfall < Max_3 	=> HR=0.85
Max_3 <= rainfall < Max_4 	=> HR=0.90
Max_4 <= rainfall 		=> HR=0.95

The total hazard value CHART_L is expressed as follows:

If HL = 0 => CHART_L =0
If HR = 0 => CHART_L =0
If HL and HR > 0 => CHART_L = WHR * HR + WHL*HL

where WHR and WHL are the weights given to the two hazard components, HR and HL respectively. 
The proposed weight values, assigned as default values but easily modifiable, are:
WHR=0.3
WHL=0.7

The CHART_L map, named: CHART_L_“period”h, is colored according to the following color rule:
    0 white
0,3	green
0,5 yellow
0,7 orange
0,9 red
1 	purple
Areas in which the estimated hazard is equal to zero, because the rainfall for assigned period is lower than the first threshold or the landslide susceptibility is estimated as very low, is not coloured, and can be masked. 
