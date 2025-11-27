"""
Calculator Tool Plugin
Perform mathematical calculations
"""

__description__ = "Perform various mathematical calculations and conversions"
__safety_level__ = "safe"
__version__ = "1.0"
__author__ = "System"

import math

class CalculatorTool:
    def __init__(self):
        pass
    
    def calculate(self, expression: str) -> dict:
        """Evaluate a mathematical expression"""
        try:
            # Safe evaluation of basic math expressions
            allowed_chars = set('0123456789+-*/(). ')
            if all(c in allowed_chars for c in expression):
                result = eval(expression)
                return {"success": True, "result": result, "expression": expression}
            else:
                return {"success": False, "error": "Invalid characters in expression"}
        except Exception as e:
            return {"success": False, "error": f"Calculation error: {e}"}
    
    def convert_units(self, value: float, from_unit: str, to_unit: str) -> dict:
        """Convert between units"""
        conversions = {
            # Length
            "meters_feet": 3.28084,
            "feet_meters": 0.3048,
            "km_miles": 0.621371,
            "miles_km": 1.60934,
            # Temperature
            "celsius_fahrenheit": lambda x: (x * 9/5) + 32,
            "fahrenheit_celsius": lambda x: (x - 32) * 5/9,
        }
        
        key = f"{from_unit}_{to_unit}"
        if key in conversions:
            converter = conversions[key]
            if callable(converter):
                result = converter(value)
            else:
                result = value * converter
            return {"success": True, "result": result, "conversion": key}
        else:
            return {"success": False, "error": f"Unsupported conversion: {from_unit} to {to_unit}"}

# Plugin interface function
def execute(command: str, parameters: dict) -> dict:
    """Main plugin execution function"""
    tool = CalculatorTool()
    
    if command == "calculate":
        return tool.calculate(parameters.get("expression", ""))
    elif command == "convert_units":
        return tool.convert_units(
            parameters.get("value", 0),
            parameters.get("from_unit", ""),
            parameters.get("to_unit", "")
        )
    else:
        return {"success": False, "error": f"Unknown command: {command}"}
