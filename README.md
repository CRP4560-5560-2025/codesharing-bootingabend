README


Author name - Naomi Mauss


Date created - 12.03.2025

Purpose of the code

The purpose of this code is to generate a graph stored as a png which
displays data from a csv file. 
This is done by joining a geojson file containing spatial data
with a csv file taken from the census bureau and modified in excel.
The project files here produce a png with marriage rates for Story county.
However, the output can be changed by modifying the
  .csv for information on a different variable or the
  .json for different spatial information

Data accessed – like name of census tables and such.
The marriage data was taken from table S1201 of the ACS,
and the spatial data was for Story County.

Brief explanation of how to run the code package.
To run the package, add the .pyt file as a toolbox to arcgis desktop.
Ensure the csv and json files are both accessible by arcgis
  (preferably, both files would be on your local computer).
Run the toolbox with the proper inputs
  (select the csv file to be used as the csv  file arcgis reads,
  do the same thing for the json file,
  you very likely want to use the opened arcgis project as the target .gdb,
  join the two files on the NAME attribute,
  and write the display field as 
    export_2025_11_29T21_03_00_112Z_csv_ + [target variable]
  for example, if the target variable is marriedpoppercent, use:
    export_2025_11_29T21_03_00_112Z_csv_marriedpoppercent
  and then create a pathway for the png file to be created.)

