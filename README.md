# AEC 2019 - UNB Team 1
Using wind data and ocean depth to intelligently position offshore wind turbines.
The goal of this system is to provide the user with the best possible combination 
of offshore wind turbine locations. 

A statistical model determines the 'best candidate' locations for turbine placement, 
and determines how many of these locations can be used within a given budget based on
the following attributes:
- IEC class	(more info: https://en.wikipedia.org/wiki/IEC_61400#Wind_Turbine_Generator_(WTG)_classes)
- Rotor diameter (m)	
- Blade length (m)	
- Swept area (m^2)	
- Cut-in wind speed (m/s) (more info: http://www.wind-power-program.com/turbine_characteristics.htm)
- Nominal power at (m/s)	
- Cut-out wind speed (more info: http://www.wind-power-program.com/turbine_characteristics.htm)
- Nominal Power (kW)	
- Cost per meter depth increase	
- Unit Cost (Millions $)	
- Maintenance cost (Millions $/year)	
- Time to construct (years)


### User Guide
From the home page, the parameters of the cost-data sheet from the excel document provided
are loaded in. The user may update any of the values from this screen, or if no changes wish
to be made, the user clicks "calculate" and the system determines the best arrangement of 
wind turbines. 

If the user wishes to export their modified cost data, they can click export and download 
the new file. 

### Techologies Used 
- Web Application: Python, Flask Framework (http://flask.pocoo.org/), Bootstrap Framework (https://getbootstrap.com/)
- Data Manipulation and Analysis: Pandas Library (https://pandas.pydata.org/)
- Persistent Data Storage: Excel

### To Run
- requires python3 and pip3
- install requirements ```pip3 install -r requirements.txt```
- run the app! ```python3 -m flask run```
- in your browser go to ```localhost:5000/app```
