import csv
import re
from openai import OpenAI
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
        self.parse_type = ""


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
    unsorted_components = []

    for row in rows:
        current_component = Component(str(row["Manufacture Part Number"]), str(row["LCSC Part Number"]), str(row["Manufacturer"]), str(row["Package"]), int(row["Order Qty."]), str(row["RoHS"]))
        current_component.parse_type = "OfflineParser"
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
        unsorted_components.append(current_component.__dict__)
    return components, unsorted_components

def ai_parser_unsafe(components, openai_client): # unsafe to push directly into database without verification mechanism
    component_types = ["Capacitor", "Resistor", "Inductor", "Diode", "Transistor", "LED", "Crystal", "Connector", "Switch", "Fuse", "Relay", "Voltage Regulators", "Specialized ICs", "Other"]
    response_template = {
        "Capacitor": [
                {
                    "mpn": "the manufacturer part number of the component",
                    "distributor_id": "the distributor part number of the component",
                    "manufacturer": "the manufacturer of the component",
                    "qty": "the quantity of the component",
                    "isRoHS": "whether the component is RoHS compliant",
                    "package": "the package of the component, eg 0603, QFN36, etc",
                    "type": "Type of the component among the provided list",
                    "sub_type": "The sub type of the component",
                    "data": {"key1": "value1", "key2": "value2", "key3": "value3... etc"},
                    "original_data": "The original data string",
                    "data_prediction_certainty": "How sure you are of the electrical characteristics being correct (High, Medium, Low)"
                }
        ],
        "Resistor": [
                {
                    "mpn": "the manufacturer part number of the component",
                    "distributor_id": "the distributor part number of the component",
                    "manufacturer": "the manufacturer of the component",
                    "qty": "the quantity of the component",
                    "isRoHS": "whether the component is RoHS compliant",
                    "package": "the package of the component, eg 0603, QFN36, etc",
                    "type": "Type of the component among the provided list",
                    "sub_type": "The sub type of the component",
                    "data": {"key1": "value1", "key2": "value2", "key3": "value3... etc"},
                    "original_data": "The original data string",
                    "data_prediction_certainty": "How sure you are of the electrical characteristics being correct (High, Medium, Low)"
                }
        ]
    }
    key_characteristics = {
        "Capacitor": ["Voltage Rating", "Dieletric", "Value", "Tolerance"],
        "Resistor": ["Voltage Rating", "Temperature Coefficient", "Tolerance", "Value"],
        "Inductor": ["Current Rating", "Value", "Tolerance", "DCR"],
        "Diode": ["Reverse Breakdown Voltage", "Forward Voltage Drop", "Current Rating"],
        "LED" : ["Current Rating", "Color", "Wavelength", "Luminous Intensity", "Forward Voltage", "Viewing Angle"],
        "Crystal": ["Frequency", "Load Capacitance", "Frequency Tolerance", "Frequency Stability"],
        "Connector": ["Current Rating", "Number of Pins", "Pitch"],
        "Voltage Regulators": ["Input Voltage", "Output Voltage", "Output Current", "Efficiency", "Switching Frequency"],
    }
    prompt = (
        f"Here's an array of electrical components: {components}.\n\n"
        f"Please categorize all the components its type among the following list: {component_types}.\n"
        f"Additionally, identify its sub-category (e.g., MLCC or Tantalum for capacitors).\n"
        f"Extract and list its key electrical characteristics in the 'data' portion of the JSON response.\n\n"
        f"The expected JSON format is as follows:\n"
        f"{response_template}\n\n"
        f"The accepted key characteristics for each type are:\n"
        f"{key_characteristics}\n\n"
        f"If certain electrical characteristics cannot be determined, leave them as null.\n"
        f"Leave the data field null if the component's type is not in the list of key characteristics.\n"
    )

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract an electrical component's data and categorize it."},
            {"role": "user", "content": prompt}
        ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content

def ai_parser_single(component, openai_client):
    component_types = ["Capacitor", "Resistor", "Inductor", "Diode", "Transistor", "LED", "Crystal", "Connector", "Switch", "Fuse", "Relay", "Voltage Regulators", "Specialized ICs", "Other"]
    response_template = {
        "package": "the package of the component, eg 0603, QFN36, etc",
        "type": "Type of the component among the provided list",
        "sub_type": "The sub type of the component",
        "data": {"key1": "value1", "key2": "value2", "key3": "value3... etc"},
        "data_prediction_certainty": "How sure you are of the electrical characteristics being correct (High, Medium, Low)"
    }
    key_characteristics = {
        "Capacitor": ["Voltage Rating", "Dieletric", "Value", "Tolerance"],
        "Resistor": ["Voltage Rating", "Temperature Coefficient", "Tolerance", "Value"],
        "Inductor": ["Current Rating", "Value", "Tolerance", "DCR"],
        "Diode": ["Reverse Breakdown Voltage", "Forward Voltage Drop", "Current Rating"],
        "LED" : ["Current Rating", "Color", "Wavelength", "Luminous Intensity", "Forward Voltage", "Viewing Angle"],
        "Crystal": ["Frequency", "Load Capacitance", "Frequency Tolerance", "Frequency Stability"],
        "Connector": ["Current Rating", "Number of Pins", "Pitch"],
        "Voltage Regulators": ["Input Voltage", "Output Voltage", "Output Current", "Efficiency", "Switching Frequency"],
    }
    prompt = (
        f"Here's an electrical component: {component}.\n\n"
        f"Please categorize the component and its type among the following list: {component_types}.\n"
        f"Additionally, identify its sub-category (e.g., MLCC or Tantalum for capacitors).\n"
        f"Extract and list its key electrical characteristics in the 'data' portion of the JSON response.\n\n"
        f"The expected JSON format is as follows:\n"
        f"{response_template}\n\n"
        f"The accepted key characteristics for each type are:\n"
        f"{key_characteristics}\n\n"
        f"If certain electrical characteristics cannot be determined, leave them as null.\n"
        f"Leave the data field null if the component's type is not in the list of key characteristics.\n"
    )

    completion = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={ "type": "json_object" },
        messages=[
            {"role": "system", "content": "You are a helpful assistant designed to extract an electrical component's data and categorize it."},
            {"role": "user", "content": prompt}
        ]
    )

    response = completion.choices[0].message.content
    original_data = component["data"]["original_data"]
    component["type"] = response["type"]
    component["sub_type"] = response["sub_type"]
    component["data"] = response["data"]
    component["data_prediction_certainty"] = response["data_prediction_certainty"]
    component["data"]["original_data"] = original_data

    return component
