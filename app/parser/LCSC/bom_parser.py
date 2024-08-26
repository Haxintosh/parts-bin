import re
import csv

from app.api.component.schemas import Component, ComponentList

def lcsc_parser(csv) -> ComponentList:
    reader = csv.DictReader(csv)
    rows = [row for row in reader]
    category_map = {
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

    components = ComponentList(components=[])
    unsorted_components = []

    for row in rows:

        current_component = Component(mpn = str(row["Manufacture Part Number"]), distributor_id=str(row["LCSC Part Number"]), manufacturer = str(row["Manufacturer"]), package=str(row["Package"]), qty=int(row["Order Qty."]), category="undefined", sub_category="undefined", description=str(row["Description"]))
        current_component.parse_type = "OfflineParser"
        original_data = row["Description"]
        if not current_component.data:
            current_component.data = {}

        current_component.data["original_data"] = original_data
        for i in category_map:
            if i in original_data:
                current_component.category = category_map[i]
                break
            else:
                current_component.category = "Other"

        if current_component.category == "Capacitor":
            if "MLCC" in original_data:
                current_component.sub_category="MLCC"

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

        if current_component.category == "Resistor":
            if "Thick Film Resistor" in original_data:
                current_component.sub_category="Thick Film Resistor"

            current_component.data["Voltage Rating"] = re.findall(pattern=res_v_rating_regex, string=original_data)[0]
            current_component.data["Temperature Coefficient"] = re.findall(pattern=res_temp_coef_regex, string=original_data)[0]
            current_component.data["Tolerance"] = re.findall(pattern=res_tolerance_regex, string= original_data)[0]
            current_component.data["Value"] = re.findall(pattern=res_value_regex, string=original_data)[0]
            current_component.value = re.findall(pattern=res_value_regex, string=original_data)[0]
        components.components.append(current_component)
    return components
