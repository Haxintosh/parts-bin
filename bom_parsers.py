import csv
import re
class Component:
    def __init__(self, mpn, dist_id, manufacturer, package, qty, isRoHS):
        self.mpn = mpn,
        self.distributor_id = dist_id,
        self.manufacturer = manufacturer,
        self.package = package,
        self.qty = qty,
        self.isRoHS = isRoHS
        self.type = None,
        self.value = None,
        self.data = {}


def parse_csv(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = [row for row in reader]
        return rows

def lcsc_parser(rows):
    type_map = {
        "Capacitor" : "Capacitor",
        "Resistor" : "Resistor",
        "Inductor" : "Inductor",
        "Diode" : "Diode",
        "Transistor" : "Transistor",
        "LED" : "LED",
        "Crystal" : "Crystal",
        "Connector" : "Connector",
        "Switch" : "Switch",
        "Fuse" : "Fuse",
        "Relay" : "Relay",
        "DC-DC Converter": "DC-DC Converter",
    }

    res_v_rating_regex = re.compile(r"[0-9]+V|[0-9]+kV")
    res_temp_coef_regex = re.compile(r"±[0-9]+ppm\/℃")
    res_tolerance_regex = re.compile(r"±[0-9]+%")
    res_value_regex = re.compile(r"^\s*[0-9]+(?:\.[0-9]+)?\s*(p|n|u|μ|m|k|M|G|T)?Ω\s*$")

    for row in rows:
        current_component = Component(row["Manufacture Part Number"], row["LCSC Part Number"], row["Manufacturer"], row["Package"], row["Order Qty."], row["RoHS"])
        original_data = row["Description"]
        current_component.data["original_data"] = original_data

        for i in type_map:
            if i in original_data:
                current_component.type = type_map[i]
                break
            else:
                current_component.type = "Other"

        if current_component.type == "Capacitor":
            for i, val in enumerate(original_data.split(" ")):
                match i:
                    case 0:
                        current_component.data["Voltage Rating"] = val
                    case 1:
                        current_component.data["Value"] = val
                        current_component.value = val
                    case 2:
                        current_component.data["Dielectric"] = val
                    case 3:
                        current_component.data["Tolerance"] = val
                    case _:
                        pass
        if current_component.type == "Resistor":


        print(current_component.__dict__)

