import json
import random

seeds = []
seed_id = 1

def add_seed(lang, cat, tool, query, gt_params, diff, clarif=False, failure=None, context=None):
    global seed_id
    seeds.append({
        "id": f"seed_{seed_id:04d}",
        "language": lang,
        "category": cat,
        "tool": tool,
        "user_query": query,
        "conversation_context": context or [],
        "ground_truth": {
            "tool_name": tool,
            "parameters": gt_params
        },
        "difficulty": diff,
        "requires_clarification": clarif,
        "failure_type_injected": failure
    })
    seed_id += 1

# Cities
cities = [
    ("Dhaka", "ঢাকা"), ("Kolkata", "কলকাতা"), 
    ("Mumbai", "মুম্বাই"), ("Delhi", "দিল্লি"), 
    ("London", "লন্ডন")
]

# --- 1. get_weather (Target ~50) ---
for c_en, c_bn in cities:
    for date_en, date_bn in [("today", "আজ"), ("tomorrow", "আগামীকাল")]:
        add_seed("english", "English Baseline", "get_weather", f"What's the weather in {c_en} {date_en}?", {"city": c_en, "date": date_en}, "easy")
        add_seed("bangla", "Pure Multilingual", "get_weather", f"{date_bn} {c_bn} এর আবহাওয়া কেমন?", {"city": c_en, "date": date_en}, "medium")
        add_seed("bangla-english", "Code-switching", "get_weather", f"{date_en} {c_en} er weather kemon?", {"city": c_en, "date": date_en}, "medium")
        add_seed("bangla-english", "Transliteration", "get_weather", f"{c_en} er weather report daw {date_en}.", {"city": c_en, "date": date_en}, "medium")
        add_seed("bangla", "Parameter Localization", "get_weather", f"{c_bn} শহরের তাপমাত্রা কত?", {"city": c_en}, "hard")

for _ in range(10):
    add_seed("english", "Ambiguous Requests", "get_weather", "What's the weather like?", {}, "hard", clarif=True)
    add_seed("bangla", "Failure Recovery", "get_weather", "Rajshahi er weather kemon?", {"city": "Rajshahi"}, "hard", failure="invalid_city")

# --- 2. book_ride (Target ~50) ---
locations = [("Airport", "এয়ারপোর্ট"), ("Dhanmondi", "ধানমন্ডি"), ("Gulshan", "গুলশান")]
for p_en, p_bn in locations:
    for d_en, d_bn in locations:
        if p_en == d_en: continue
        add_seed("english", "English Baseline", "book_ride", f"Book a ride from {p_en} to {d_en}.", {"pickup": p_en, "destination": d_en}, "easy")
        add_seed("bangla", "Pure Multilingual", "book_ride", f"{p_bn} থেকে {d_bn} এ একটা রাইড বুক করো।", {"pickup": p_en, "destination": d_en}, "medium")
        add_seed("bangla-english", "Transliteration", "book_ride", f"{p_en} theke {d_en} er jonno cab book koro.", {"pickup": p_en, "destination": d_en}, "medium")
        add_seed("bangla-english", "Code-switching", "book_ride", f"Bhai, {p_en} theke {d_en} jabo, ride lagbe.", {"pickup": p_en, "destination": d_en}, "medium")

for _ in range(10):
    add_seed("english", "Ambiguous Requests", "book_ride", "Get me a taxi to the airport.", {"destination": "Airport"}, "hard", clarif=True)
    add_seed("bangla", "Failure Recovery", "book_ride", "Dhaka theke Chittagong ride daw.", {"pickup": "Dhaka", "destination": "Chittagong"}, "hard", failure="timeout_simulation")

# --- 3. order_food (Target ~50) ---
foods = [("Kacchi Biryani", "কাচ্চি বিরিয়ানি"), ("Pizza", "পিজা"), ("Burger", "বারগার")]
rests = ["Star Kabab", "Domino's", "KFC"]
for food_en, food_bn in foods:
    for rest in rests:
        for qty in [1, 2, 3]:
            add_seed("english", "English Baseline", "order_food", f"Order {qty} {food_en} from {rest}.", {"restaurant": rest, "item": food_en, "quantity": qty}, "easy")
            add_seed("bangla", "Pure Multilingual", "order_food", f"{rest} থেকে {qty} টা {food_bn} অর্ডার করো।", {"restaurant": rest, "item": food_en, "quantity": qty}, "medium")
            add_seed("bangla-english", "Code-switching", "order_food", f"{rest} theke {qty} ta {food_en} order daw.", {"restaurant": rest, "item": food_en, "quantity": qty}, "medium")

for _ in range(5):
    add_seed("english", "Ambiguous Requests", "order_food", "I want to order a Burger.", {"item": "Burger"}, "hard", clarif=True)

# --- 4. send_email (Target ~50) ---
people = [("Rahul", "রাহুল"), ("Boss", "বস"), ("Team", "টিম")]
for p_en, p_bn in people:
    for topic in ["Meeting", "Report", "Leave"]:
        add_seed("english", "English Baseline", "send_email", f"Send an email to {p_en} about the {topic}.", {"recipient": p_en, "subject": topic, "body": f"Regarding the {topic}"}, "easy")
        add_seed("bangla", "Pure Multilingual", "send_email", f"{p_bn} কে {topic} নিয়ে একটা ইমেইল পাঠাও।", {"recipient": p_en, "subject": topic, "body": f"Regarding the {topic}"}, "medium")
        add_seed("bangla-english", "Transliteration", "send_email", f"{p_en} ke {topic} er bepare email koro.", {"recipient": p_en, "subject": topic, "body": f"Regarding the {topic}"}, "medium")
        add_seed("bangla-english", "Code-switching", "send_email", f"{p_en} ke email daw je {topic} is ready.", {"recipient": p_en, "subject": topic, "body": f"{topic} is ready."}, "medium")

# --- 5. create_calendar_event (Target ~50) ---
for topic in ["Meeting", "Doctor", "Lunch"]:
    for day in ["Monday", "Tuesday", "Friday"]:
        for time in ["10:00", "14:00", "18:00"]:
            add_seed("english", "English Baseline", "create_calendar_event", f"Schedule {topic} on {day} at {time}.", {"title": topic, "date": day, "time": time}, "easy")
            add_seed("bangla-english", "Code-switching", "create_calendar_event", f"{day} te {time} er dike {topic} fix koro.", {"title": topic, "date": day, "time": time}, "medium")
            add_seed("bangla-english", "Transliteration", "create_calendar_event", f"{day} te {time} baje {topic} schedule koro.", {"title": topic, "date": day, "time": time}, "medium")

for _ in range(10):
    add_seed("english", "Failure Recovery", "create_calendar_event", "Set a meeting.", {"title": "meeting"}, "hard", failure="tool_unavailable")

# --- 6. search_flights (Target ~50) ---
for c_en1, c_bn1 in cities[:3]:
    for c_en2, c_bn2 in cities[2:]:
        if c_en1 == c_en2: continue
        add_seed("english", "English Baseline", "search_flights", f"Flights from {c_en1} to {c_en2} tomorrow.", {"origin": c_en1, "destination": c_en2, "date": "tomorrow"}, "easy")
        add_seed("bangla", "Parameter Localization", "search_flights", f"{c_bn1} থেকে {c_bn2} ফ্লাইট খুঁজুন।", {"origin": c_en1, "destination": c_en2}, "medium")
        add_seed("bangla-english", "Transliteration", "search_flights", f"{c_en1} theke {c_en2} er flight dekhaw next week.", {"origin": c_en1, "destination": c_en2, "date": "next week"}, "medium")

for _ in range(10):
    add_seed("english", "Ambiguous Requests", "search_flights", "Find flights to London.", {"destination": "London"}, "hard", clarif=True)

# --- 7. currency_convert (Target ~50) ---
curs = [("USD", "ডলার"), ("BDT", "টাকা"), ("INR", "রুপি")]
for c1_en, c1_bn in curs:
    for c2_en, c2_bn in curs:
        if c1_en == c2_en: continue
        for amt in [100, 500, 1000]:
            add_seed("english", "English Baseline", "currency_convert", f"Convert {amt} {c1_en} to {c2_en}.", {"amount": amt, "from_currency": c1_en, "to_currency": c2_en}, "easy")
            add_seed("bangla", "Pure Multilingual", "currency_convert", f"{amt} {c1_bn} সমান কত {c2_bn}?", {"amount": amt, "from_currency": c1_en, "to_currency": c2_en}, "medium")
            add_seed("bangla-english", "Code-switching", "currency_convert", f"{amt} {c1_en} ke {c2_en} e convert koro.", {"amount": amt, "from_currency": c1_en, "to_currency": c2_en}, "medium")

# Write to file
with open('data/raw/seed_dataset.jsonl', 'w', encoding='utf-8') as f:
    for s in seeds:
        f.write(json.dumps(s, ensure_ascii=False) + '\n')

print(f"Generated {len(seeds)} total seeds across 7 tools.")
