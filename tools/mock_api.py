import json
import random
import time
from .schemas import TOOL_SCHEMAS

class MockAPIEnvironment:
    """
    Simulates API execution and handles failure injection.
    Crucially tests the 'Language-Tool Boundary' by rejecting non-canonical input.
    """
    
    def __init__(self):
        self.schemas = {schema['name']: schema for schema in TOOL_SCHEMAS}
        self.valid_cities = ["Dhaka", "Kolkata", "Delhi", "Mumbai", "London", "New York"]
        self.valid_currencies = ["USD", "BDT", "INR", "EUR", "GBP"]
        
    def execute(self, tool_name: str, parameters: dict, inject_failure: str = None) -> dict:
        """
        Executes a tool call in the mock environment.
        Supports deterministic failure injection to test model recovery mechanisms.
        """
        # --- 1. Validate Tool Existence ---
        if tool_name not in self.schemas:
            return {"status": "error", "message": f"Tool '{tool_name}' is not recognized."}
            
        schema = self.schemas[tool_name]
        
        # --- 2. Systemic Failure Injection ---
        if inject_failure == "timeout_simulation":
            time.sleep(1)  # Simulating network latency
            return {"status": "error", "message": "API request timed out (504 Gateway Timeout). Please try again."}
            
        if inject_failure == "tool_unavailable":
            return {"status": "error", "message": f"Service '{tool_name}' is currently down for maintenance (503 Service Unavailable)."}

        # --- 3. Schema & Requirement Validation ---
        missing_fields = [req for req in schema["parameters"]["required"] if req not in parameters]
        if missing_fields or inject_failure == "missing_parameter":
            return {"status": "error", "message": f"Missing required parameters: {', '.join(missing_fields) if missing_fields else 'unknown field'}."}

        # --- 4. Language-Tool Boundary (Localization Validation) ---
        # The API specifically only accepts canonical English formats.
        
        if inject_failure == "wrong_format":
            return {"status": "error", "message": "Invalid parameter format. Expected standard string or numerical value."}
            
        # Check for localization leakage (e.g., passing Bengali script instead of English)
        for key, value in parameters.items():
            if isinstance(value, str) and not value.isascii():
                if inject_failure == "unsupported_language":
                     return {"status": "error", "message": f"Parameter '{key}' contains unsupported characters. The API only accepts English inputs."}
                return {"status": "error", "message": f"Invalid value '{value}' for parameter '{key}'. Value must be localized to canonical English."}

        # --- 5. Tool-Specific Logic & Mock Responses ---
        if tool_name == "get_weather":
            city = parameters.get("city")
            if inject_failure == "invalid_city" or (city not in self.valid_cities and city):
                return {"status": "error", "message": f"City '{city}' not found in weather database. Please provide a canonical city name."}
            return {"status": "success", "data": {"weather": "Sunny", "temperature": "28C"}}
            
        elif tool_name == "create_calendar_event":
            return {"status": "success", "data": {"event_id": f"evt_{random.randint(1000, 9999)}", "status": "scheduled"}}
            
        elif tool_name == "send_email":
            return {"status": "success", "data": {"message": "Email successfully queued for delivery."}}
            
        elif tool_name == "order_food":
            return {"status": "success", "data": {"order_id": f"ord_{random.randint(100, 999)}", "eta": "30 mins"}}
            
        elif tool_name == "book_ride":
            return {"status": "success", "data": {"driver": "John Doe", "vehicle": "Toyota Prius", "eta": "5 mins"}}
            
        elif tool_name == "search_flights":
            return {"status": "success", "data": {"flights": [{"flight_no": "BG-101", "price": "$250"}]}}
            
        elif tool_name == "currency_convert":
            from_c = parameters.get("from_currency", "").upper()
            to_c = parameters.get("to_currency", "").upper()
            if from_c not in self.valid_currencies or to_c not in self.valid_currencies:
                return {"status": "error", "message": "Invalid or unsupported 3-letter currency code."}
            converted = float(parameters.get("amount", 0)) * 1.5  # Fixed mock conversion rate
            return {"status": "success", "data": {"converted_amount": converted}}

        return {"status": "success", "data": {"message": "Executed successfully"}}
