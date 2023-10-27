New Bas MAP, 
Modification: 
- Ramp connection to zipper with forced merge
(could not change visibility nut default is 100m)
- set the clear option to False
- Changed the geametry to straight
- Lane change:
	- krauss +ACC  lcStrategic="10" lcCooperative="0.9" lcSpeedGainLookahead="5"
 	- CACCC  lcStrategic="100" lcCooperative="1" lcSpeedGainLookahead="5"

Run CMD:

TO run 

"sumo.exe -c I75_FInal.sumocfg -r [routefile name] --step-length 0.1 --no-warnings"

To convert the xml file to csv

python xml2csv.py [xml filename]


input_files1 = r"ssm_k.xml"  -- gives ssm param of krauss
input_files2 = r"ssm_a.xml"  -- for av
input_files3 = r"ssm_c.xml"  -- cacc


input_files4 = r"traveltime.xml" -- gives traffic mean flow and travel tie
input_files5 =  r"loop.xml"  -- loop detector 

input_files6=r"fcd.xml"
input_files7=r"stat.xml"