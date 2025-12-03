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


        # arcpy.AddMessage("Plotting graph using Matplotlib...")
        # values = []
        # with arcpy.da.SearchCursor(joined_fc, [display_field]) as cursor:
        #     for row in cursor:
        #         if row[0] is not None:
        #             values.append(row[0])

        # plt.figure(figsize=(8, 5))
        # plt.plot(values)
        # plt.xlabel("Record Index")
        # plt.ylabel(display_field)
        # plt.title(f"Plot of {display_field}")
        # plt.savefig(graph_output)
        # plt.close()

        # arcpy.AddMessage("Process Complete. Output saved.")


        arcpy.AddMessage("Plotting graph using Matplotlib...")

        # tracts = []
        # values = []

        # # Replace these with your actual field names:
        # tract_field = "NAME"   # or whatever field contains "Census Tract X"
        # value_field = display_field   # CSV % field

        # with arcpy.da.SearchCursor(joined_fc, [tract_field, value_field]) as cursor:
        #     for tract, val in cursor:
        #         if tract and val:

        #             # --- CLEAN VALUE ---
        #             # Remove % symbols, ± ranges, commas, spaces
        #             val = str(val)
        #             val = val.replace("%", "").strip()

        #             # Keep only the numeric portion before ±
        #             if "±" in val:
        #                 val = val.split("±")[0].strip()

        #             try:
        #                 y = float(val)
        #             except:
        #                 continue   # skip invalid rows

        #             tr = tract.replace("Census Tract", "").strip()

        #             try:
        #                 x = float(tr)
        #             except:
        #                 x = tr   # fallback: keep string label

        #             tracts.append(x)
        #             values.append(y)

        # # --- SORT BY TRACT ---
        # sorted_pairs = sorted(zip(tracts, values), key=lambda p: p[0])
        # sorted_tracts, sorted_values = zip(*sorted_pairs)

        # # --- PLOT ---
        # plt.figure(figsize=(10, 6))
        # plt.plot(sorted_tracts, sorted_values, marker="o")
        # plt.xlabel("Census Tract")
        # plt.ylabel(display_field)
        # plt.title(f"Plot of {display_field}")
        # plt.grid(True)
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.savefig(graph_output)
        # plt.close()

        # arcpy.AddMessage("Plotting graph using Matplotlib...")

        arcpy.AddMessage("Plotting graph using Matplotlib...")

        tracts = []
        values = []

        # Replace these with your actual field names:
        tract_field = "NAME"   # or whatever field contains "Census Tract X"
        value_field = display_field   # CSV % field

        with arcpy.da.SearchCursor(joined_fc, [tract_field, value_field]) as cursor:
            for tract, val in cursor:
                if tract and val:
                    # --- CLEAN VALUE ---
                    val = str(val)
                    val = val.replace("%", "").strip()
                    
                    # Keep only the numeric portion before ±
                    if "±" in val:
                        val = val.split("±")[0].strip()
                    
                    try:
                        y = float(val)
                    except:
                        continue   # skip invalid rows
                    
                    # --- KEEP TRACT AS STRING (CATEGORICAL) ---
                    tr = tract.replace("Census Tract", "").strip()
                    
                    tracts.append(tr)
                    values.append(y)

        # Check if we have data
        if not tracts:
            arcpy.AddError("No valid data to plot!")
            return

        # --- SORT BY TRACT NUMBER (for sensible ordering) ---
        # Try to sort numerically if possible, otherwise alphabetically
        try:
            sorted_pairs = sorted(zip(tracts, values), key=lambda p: float(p[0]))
        except:
            sorted_pairs = sorted(zip(tracts, values), key=lambda p: p[0])

        sorted_tracts, sorted_values = zip(*sorted_pairs)

        # Convert to lists for plotting
        sorted_tracts = list(sorted_tracts)
        sorted_values = list(sorted_values)

        arcpy.AddMessage(f"Plotting {len(sorted_tracts)} data points...")

        # --- PLOT AS BAR CHART (CATEGORICAL X-AXIS) ---
        plt.figure(figsize=(12, 6))
        plt.bar(sorted_tracts, sorted_values, color='steelblue', edgecolor='black', linewidth=0.7)
        plt.xlabel("Census Tract", fontsize=12)
        plt.ylabel("Percent Married (%)", fontsize=12)
        plt.title(f"Percent Married by Census Tract", fontsize=14, fontweight='bold')
        plt.grid(axis='y', alpha=0.3, linestyle='--')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(graph_output, dpi=150)
        plt.close()

        arcpy.AddMessage("Process Complete. Graph saved.")
