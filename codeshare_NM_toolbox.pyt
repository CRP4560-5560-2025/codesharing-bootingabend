import arcpy
import matplotlib.pyplot as plt
import os

class Toolbox(object):
    def __init__(self):
        self.label = "CSV + GeoJSON Join & Plot Toolbox"
        self.alias = "csv_geojson_toolbox"
        self.tools = [CSVGeoJSONJoinPlot]

class CSVGeoJSONJoinPlot(object):
    def __init__(self):
        self.label = "Join CSV + GeoJSON and Plot"
        self.description = "Converts GeoJSON to feature class, joins with CSV, displays symbology, and creates a Matplotlib graph."

    def getParameterInfo(self):
        params = []

        csv_file = arcpy.Parameter(
            displayName="Select CSV File",
            name="csv_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        geojson_file = arcpy.Parameter(
            displayName="Select GeoJSON File",
            name="geojson_file",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")

        output_gdb = arcpy.Parameter(
            displayName="Select Output Geodatabase",
            name="output_gdb",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")

        join_field = arcpy.Parameter(
            displayName="Attribute name to join on (CSV + Feature Class)",
            name="join_field",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        display_field = arcpy.Parameter(
            displayName="Field to display / symbolize",
            name="display_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        display_field.parameterDependencies = ["csv_file"]

        graph_output = arcpy.Parameter(
            displayName="Choose where to save graph PNG",
            name="graph_output",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")

        params.extend([csv_file, geojson_file, output_gdb, join_field, display_field, graph_output])
        return params

    def execute(self, parameters, messages):
        csv_file = parameters[0].valueAsText
        geojson_file = parameters[1].valueAsText
        output_gdb = parameters[2].valueAsText
        join_field = parameters[3].valueAsText
        display_field = parameters[4].valueAsText
        graph_output = parameters[5].valueAsText

        arcpy.AddMessage("Converting GeoJSON to Feature Class...")
        fc_path = os.path.join(output_gdb, "geojson_features")
        arcpy.conversion.JSONToFeatures(geojson_file, fc_path)

        arcpy.AddMessage("Creating table from CSV...")
        # csv_table = arcpy.management.MakeTableView(csv_file, "csv_table").name
        csv_table = "csv_table"
        arcpy.management.MakeTableView(csv_file, csv_table)


        #   arcpy.AddMessage("Joining CSV to Feature Class...")
        #   arcpy.management.AddJoin(fc_path, join_field, csv_table, join_field)

        arcpy.AddMessage("Joining CSV to Feature Class...")

        # Create a feature layer for joining
        if arcpy.Exists("fc_layer"):
            arcpy.management.Delete("fc_layer")

        arcpy.management.MakeFeatureLayer(fc_path, "fc_layer")

        # Create CSV table view
        if arcpy.Exists("csv_table"):
            arcpy.management.Delete("csv_table")

        arcpy.management.MakeTableView(csv_file, "csv_table")

        # Perform join
        arcpy.management.AddJoin("fc_layer", join_field, "csv_table", join_field)

        # Debug: show number of matched records
        count = int(arcpy.GetCount_management("fc_layer")[0])
        arcpy.AddMessage(f"Matched rows after join: {count}")


        count = arcpy.GetCount_management("fc_layer")
        arcpy.AddMessage(f"Layer count: {count}")

        matched_count = arcpy.GetCount_management("fc_layer")
        arcpy.AddMessage(f"Matched row count after join: {matched_count}")


        arcpy.AddMessage("Exporting joined Feature Class...")
        joined_fc = os.path.join(output_gdb, "joined_output")
        #   arcpy.management.CopyFeatures(fc_path, joined_fc)
        arcpy.management.CopyFeatures("fc_layer", joined_fc)

        arcpy.AddMessage("Fields in joined feature class:")
        for f in arcpy.ListFields(joined_fc):
            arcpy.AddMessage(f.name)


        arcpy.AddMessage("Plotting graph using Matplotlib...")
        values = []
        with arcpy.da.SearchCursor(joined_fc, [display_field]) as cursor:
            for row in cursor:
                if row[0] is not None:
                    values.append(row[0])

        plt.figure(figsize=(8, 5))
        plt.plot(values)
        plt.xlabel("Record Index")
        plt.ylabel(display_field)
        plt.title(f"Plot of {display_field}")
        plt.savefig(graph_output)
        plt.close()

        arcpy.AddMessage("Process Complete. Output saved.")
