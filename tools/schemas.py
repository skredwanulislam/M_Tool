TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a specific city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city in canonical English (e.g., 'Dhaka', 'Kolkata')."
                },
                "date": {
                    "type": "string",
                    "description": "The date for the weather forecast in ISO format (YYYY-MM-DD) or canonical English 'tomorrow', 'today'."
                }
            },
            "required": ["city"]
        }
    },
    {
        "name": "create_calendar_event",
        "description": "Create an event in the calendar.",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title or name of the event."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the event in ISO format (YYYY-MM-DD)."
                },
                "time": {
                    "type": "string",
                    "description": "The time of the event in 24-hour format (HH:MM)."
                }
            },
            "required": ["title", "date", "time"]
        }
    },
    {
        "name": "send_email",
        "description": "Send an email to a specific recipient.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "The email address or name of the recipient."
                },
                "subject": {
                    "type": "string",
                    "description": "The subject of the email."
                },
                "body": {
                    "type": "string",
                    "description": "The main text body of the email."
                }
            },
            "required": ["recipient", "body"]
        }
    },
    {
        "name": "order_food",
        "description": "Order a food item from a restaurant.",
        "parameters": {
            "type": "object",
            "properties": {
                "restaurant": {
                    "type": "string",
                    "description": "The name of the restaurant."
                },
                "item": {
                    "type": "string",
                    "description": "The name of the food item in English."
                },
                "quantity": {
                    "type": "integer",
                    "description": "The number of items to order."
                }
            },
            "required": ["restaurant", "item"]
        }
    },
    {
        "name": "book_ride",
        "description": "Book a ride or taxi from a pickup location to a destination.",
        "parameters": {
            "type": "object",
            "properties": {
                "pickup": {
                    "type": "string",
                    "description": "The pickup location in English."
                },
                "destination": {
                    "type": "string",
                    "description": "The destination location in English."
                },
                "time": {
                    "type": "string",
                    "description": "The time for the ride in 24-hour format or 'now'."
                }
            },
            "required": ["pickup", "destination"]
        }
    },
    {
        "name": "search_flights",
        "description": "Search for available flights between two cities.",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "The origin city in English."
                },
                "destination": {
                    "type": "string",
                    "description": "The destination city in English."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the flight in ISO format (YYYY-MM-DD)."
                }
            },
            "required": ["origin", "destination", "date"]
        }
    },
    {
        "name": "currency_convert",
        "description": "Convert an amount from one currency to another.",
        "parameters": {
            "type": "object",
            "properties": {
                "amount": {
                    "type": "number",
                    "description": "The amount of money to convert."
                },
                "from_currency": {
                    "type": "string",
                    "description": "The 3-letter currency code to convert from (e.g., 'USD', 'BDT', 'INR')."
                },
                "to_currency": {
                    "type": "string",
                    "description": "The 3-letter currency code to convert to."
                }
            },
            "required": ["amount", "from_currency", "to_currency"]
        }
    }
]
