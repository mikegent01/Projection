init python:
    import random
    items_database = {
        "MG41": {
            "type": "weapon", 
            "weight": 10, 
            "description": "A powerful machine gun...",
            "max_durability": 200,  # High durability for a weapon
            "repairable": True
        },
        "Tissue": {
            "type": "junk", 
            "weight": 2, 
            "description": "A Tissue to wipe away my sorrows..",
            "max_durability": 3, 
            "repairable": False 
        },
        "Wet Tissue": {
            "type": "junk", 
            "weight": 2, 
            "description": "A Wet Tissue...yuck!",
            "max_durability": 1,  
            "repairable": False
        },
        "Crumpled Paper": {
            "type": "junk", 
            "weight": 1, 
            "description": "A paper i discarded.",
            "max_durability": 1,  
            "repairable": False
        },        
        "Pencil": {
            "type": "tool", 
            "weight": 1, 
            "description": "Used to write my thoughts down...",
            "max_durability": 1500,  
            "repairable": True
        },
        "Paper": {
            "type": "tool", 
            "weight": 1, 
            "description": "I can write stuff on this...",
            "max_durability": 10,  
            "repairable": False
        },
        "Laser range finder": {
            "type": "tool", 
            "weight": 1, 
            "description": "Used to measure the distance...",
            "max_durability": 100,  
            "repairable": True
        },
        "Compass": {
            "type": "tool", 
            "weight": 1, 
            "description": "A military grade compass...",
            "max_durability": -1, 
            "repairable": False
        },
        "Radio": {
            "type": "radio", 
            "weight": 2, 
            "description": "A military grade radio...",
            "max_durability": 550,  
            "repairable": True
        },
        "Classified Mission Sheet": {
            "type": "note", 
            "weight": 2, 
            "description": "A sheet I should not have...",
            "max_durability": -1,  
            "repairable": False
        },
        "First aid kit": {
            "type": "consumable", 
            "weight": 1, 
            "description": "Used to heal minor injuries.",
            "max_durability": 5, 
            "repairable": True 
        },
        "Tactical flashlight": {
            "type": "tool", 
            "weight": 1, 
            "description": "This light can survive explosions...",
            "max_durability": 300, 
            "repairable": True
        },
        "Water Bottle": {
            "type": "consumable", 
            "weight": 1, 
            "description": "Used to hold water...",
            "max_durability": 100, 
            "repairable": False
        },
        "Sissor": {
            "type": "tool", 
            "weight": 1, 
            "description": "Used to cut things.",
            "max_durability": 80,  
            "repairable": True
        },
        "Report 001": {
            "type": "document", 
            "weight": 300, 
            "description": "A report of something...",
            "max_durability": -1,  
            "repairable": False
        },
        "Pistol": {
            "type": "weapon", 
            "weight": 2, 
            "description": "A standard issue sidearm...",
            "max_durability": 150,  
            "repairable": True
        }
    }

    medkit_contents = {
        "Bandage": {"conditions": ["bleeding", "cut"], "healing": 10},
        "Phenergan": {"conditions": ["nausea"], "healing": 5},
        "Antibiotics": {"conditions": ["infection"], "healing": 20},
        "Morphine": {"conditions": [], "healing": 30},
        "Water Gel": {"conditions": ["burn"], "healing": 15},
        "Acetaminophen": {"conditions": [], "healing": 10},
        "Diphenhydramine": {"conditions": ["pain"], "healing": 10},
        "SOFT-T": {"conditions": ["hemorrhage", "fracture", "bleeding"], "healing": 10},
        "Naproxen": {"conditions": ["headache"], "healing": 10}
    }    