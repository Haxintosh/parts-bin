import csv
import re
class Component:
    def __init__(self, mpn, dist_id, manufacturer, package, qty, isRoHS):
        self.mpn = mpn
        self.distributor_id = dist_id
        self.manufacturer = manufacturer
        self.package = package
        self.qty = qty
        self.isRoHS = isRoHS
        self.type = None
        self.sub_type = None
        self.value = None
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
    res_value_regex = re.compile(r"[0-9]+\.*[0-9]*[p|n|u|μ|m|k|M|G|T]*Ω")

    components = {}

    for row in rows:
        current_component = Component(str(row["Manufacture Part Number"]), str(row["LCSC Part Number"]), str(row["Manufacturer"]), str(row["Package"]), int(row["Order Qty."]), str(row["RoHS"]))
        original_data = row["Description"]
        current_component.data["original_data"] = original_data

        for i in type_map:
            if i in original_data:
                current_component.type = type_map[i]
                break
            else:
                current_component.type = "Other"

        if current_component.type == "Capacitor":
            if "MLCC" in original_data:
                current_component.sub_type="MLCC"

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
            if "Thick Film Resistor" in original_data:
                current_component.sub_type="Thick Film Resistor"

            current_component.data["Voltage Rating"] = re.findall(pattern=res_v_rating_regex, string=original_data)[0]
            current_component.data["Temperature Coefficient"] = re.findall(pattern=res_temp_coef_regex, string=original_data)[0]
            current_component.data["Tolerance"] = re.findall(pattern=res_tolerance_regex, string= original_data)[0]
            current_component.data["Value"] = re.findall(pattern=res_value_regex, string=original_data)[0]
            current_component.value = re.findall(pattern=res_value_regex, string=original_data)[0]
        if current_component.type not in components:
            components[current_component.type] = []
        components[current_component.type].append(current_component.__dict__)
        print(components)
    return components

