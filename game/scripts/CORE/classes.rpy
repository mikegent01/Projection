init python:
    roll_queue = []  
    class GameCharacter:
        
        def __init__(self, name, starting_stats, starting_emotions, starting_proficiencies=None):
            self.name = name
            self.stats = starting_stats
            self.emotions = starting_emotions
            self.sanity = 100
            self.inventory = Inventory(owner=self, capacity=20)
          
            self.health = {
                "head": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 74},
                "body": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 70},
                "left_arm": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 74},
                "right_arm": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 70},
                "left_leg": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 73},
                "right_leg": {"status": "fine", "health": 100, "conditions": [], "temperature": 70, "cleanliness": 72}
            }
            self.relationships = {
                "Samuel": {"trust": 60, "friendship": 70, "hostility": 10, "met": True},  
                "Barns": {"trust": 40, "friendship": 20, "hostility": 10, "met": True}, 
            }
            self.proficiencies = starting_proficiencies 
            self._initialize_stats()
            self._initialize_proficiencies()
            total_levels = sum(data["level"] for data in self.stats.values())
        def _initialize_proficiencies(self):
            for stat_name, profs in self.proficiencies.items():
                for prof_name, data in profs.items():
                    level = data.get("level", 1)
                    data["current_value"] = (level * random.randint(1, 3) )  

        def add_experience_proficiency(self, stat_name, prof_name, amount):
            if stat_name in self.proficiencies and prof_name in self.proficiencies[stat_name]:
                prof = self.proficiencies[stat_name][prof_name]
                prof["current_xp"] += amount
                if prof["current_xp"] >= prof["max_xp"]:
                    self.level_up_proficiency(stat_name, prof_name)

        def level_up_proficiency(self, stat_name, prof_name):
            if stat_name in self.proficiencies and prof_name in self.proficiencies[stat_name]:
                prof = self.proficiencies[stat_name][prof_name]
                prof["level"] += 1
                prof["current_xp"] = 0
                prof["max_xp"] = round(prof["max_xp"] + random.randint(10, 30))
                prof["current_value"] += random.randint(1, 6)
                renpy.notify(f"{self.name}'s {prof_name.capitalize()} (under {stat_name}) increased to level {prof['level']}!")

        def perform_roll(self, skill_name, base_chance=30, circumstance_bonus=0, min_chance=5, max_chance=95, proficiency_name=None, show_display=True):
            global roll_queue  # Declare global to modify the global roll_queue

            # If proficiency_name is not provided, check if the skill_name is actually a proficiency
            if proficiency_name is None:
                found_proficiency = False
                for stat, profs in self.proficiencies.items():
                    if skill_name in profs:
                        proficiency_name = skill_name
                        skill_name = stat  # Set skill_name to the parent stat
                        found_proficiency = True
                        break
                if found_proficiency:
                    renpy.notify(f"Detected '{proficiency_name}' as proficiency under '{skill_name}'.")
                elif skill_name not in self.stats:
                    renpy.notify(f"System Error: Skill or proficiency '{skill_name}' not found for {self.name}!")
                    return {'success': False, 'roll': 0, 'threshold': 0, 'total_chance': 0}

            if skill_name not in self.stats:
                renpy.notify(f"System Error: Skill '{skill_name}' not found for {self.name}!")
                return {'success': False, 'roll': 0, 'threshold': 0, 'total_chance': 0}

            skill_value = self.stats[skill_name].get("current_value", 0)
            
            proficiency_bonus = 0
            if proficiency_name:
                if skill_name in self.proficiencies and proficiency_name in self.proficiencies[skill_name]:
                    proficiency_bonus = self.proficiencies[skill_name][proficiency_name].get("current_value", 0)
                else:
                    renpy.notify(f"Warning: Proficiency '{proficiency_name}' not found under skill '{skill_name}' for {self.name}. Using base skill only.")
            
            emotion_bonus, emotion_bonuses_list = self._get_emotion_bonus(skill_name if proficiency_name is None else proficiency_name)  # Use proficiency for emotions if specified
            
            total_chance = base_chance + skill_value + proficiency_bonus + emotion_bonus + circumstance_bonus
            
            total_chance = max(min_chance, min(total_chance, max_chance))
            
            threshold = 101 - total_chance 
            
            roll = renpy.random.randint(1, 100)
            
            success = (roll >= threshold)
            
            # Add XP based on success/failure
            xp_amount = 10 if success else 5
            self.add_experience(skill_name, xp_amount)
            if proficiency_name and skill_name in self.proficiencies and proficiency_name in self.proficiencies[skill_name]:
                self.add_experience_proficiency(skill_name, proficiency_name, xp_amount)
            
            # Notify via existing method, including proficiency if provided
            notify_message = f"{skill_name.capitalize()} Roll: {'Success' if success else 'Failure'}! (Rolled {roll} {'≥' if success else '<'} {threshold})"
            if proficiency_name:
                notify_message += f" - Proficiency: {proficiency_name.capitalize()}"
            renpy.notify(notify_message)
                
            # Queue the roll data
            roll_data = {
                "skill": skill_name,
                "proficiency": proficiency_name,
                "roll": roll,
                "threshold": threshold,
                "total_chance": total_chance,
                "success": success,
                "emotion_bonuses": emotion_bonuses_list
            }
            roll_queue.append(roll_data)
            if len(roll_queue) > 15:  
                roll_queue.pop(0)
            
            # Show the history screen (full queue with scrollbar)
            if show_display and nenvershowrolls:
                renpy.show_screen("roll_history_screen")
            
            return {'success': success, 'roll': roll, 'threshold': threshold, 'total_chance': total_chance}
        def modify_emotion(self, emotion_name, amount, default_bonus=None):

            if default_bonus is None:
                default_bonus = {}  # Default empty bonus dict

            # Initialize if it doesn't exist
            if emotion_name not in self.emotions:
                self.emotions[emotion_name] = {"value": 0, "bonus": default_bonus}

            # Modify and clamp the value
            current_value = self.emotions[emotion_name]["value"]
            new_value = max(0, min(100, current_value + amount))  # Clamp to 0-100
            self.emotions[emotion_name]["value"] = new_value
        def heal(self, part, amount):
            if part in self.health:
                self.health[part]["health"] = min(self.health[part]["health"] + amount, self.max_health)
                renpy.notify(f"{self.name}'s {part.replace('_', ' ')} restored by {amount} points.")

        def take_damage(self, part, amount):
            if part in self.health:
                self.modify_cleanliness(part, -1)
                self.health[part]["health"] = max(self.health[part]["health"] - amount, 0)
                if self.health[part]["health"] == 0 and part == "head": renpy.jump("gameover")
        def has_item(self, item_name):
            return item_name in self.items
        def calculate_averages(self):
            body_part_count = len(self.health)
            if body_part_count == 0:
                return 0, 0, 0
            total_health = sum(status['health'] for status in self.health.values())
            total_cleanliness = sum(status['cleanliness'] for status in self.health.values())
            total_temperature = sum(status['temperature'] for status in self.health.values())
            return round(total_health / body_part_count), round(total_cleanliness / body_part_count), round(total_temperature / body_part_count)
        def is_stat_higher(self, stat_name, value_to_compare):
            """Checks if a character's stat is higher than a given value."""
            if stat_name in self.stats:
                return self.stats[stat_name]["current_value"] > value_to_compare
            return False
        def get_relationship_description(self, person_name):
            """Gets the relationship status description for a specific person."""
            if person_name not in self.relationships:
                return "Stranger"
            
            rel = self.relationships[person_name]
            trust = rel.get("trust", 0)
            friendship = rel.get("friendship", 0)
            hostility = rel.get("hostility", 0)     

            if trust > 80 and friendship > 80: return "Best Friend"
            if trust > 70 and friendship > 70: return "Close Friend"
            if friendship > 50: return "Friend"
            if hostility > 70: return "Enemy"
            if hostility > 50: return "Adversary"
            if trust > 50: return "Trusted Associate"
            return "Acquaintance"        
        def add_condition(self, part, new_condition):
            if part in self.health and new_condition not in self.health[part]["conditions"]:
                self.health[part]["conditions"].append(new_condition)
                self.max_health = max(0, self.max_health - 10)
                self.take_damage(part, 10)
                renpy.notify(f"{self.name} is now afflicted with {new_condition}.")

        def remove_condition(self, part, condition):
            if part in self.health and condition in self.health[part]["conditions"]:
                self.health[part]["conditions"].remove(condition)
                self.max_health = min(100, self.max_health + 10)
                self.heal(part, 10)
                renpy.notify(f"{condition.capitalize()} has been cured for {self.name}.")

        def has_condition(self, part, condition):
            return condition in self.health.get(part, {}).get("conditions", [])

        def modify_cleanliness(self, part, amount):
            if part in self.health:
                self.health[part]['cleanliness'] = max(0, min(100, self.health[part]['cleanliness'] + amount))
                self._check_cleanliness_and_adjust_temp(part)

        def _check_cleanliness_and_adjust_temp(self, part):
            cleanliness = self.health[part]['cleanliness']
            if cleanliness > 90: self.health[part]['temperature'] -= 2
            elif cleanliness > 75: self.health[part]['temperature'] -= 1
            elif cleanliness < 50: self.health[part]['temperature'] += 1
            elif cleanliness < 25: self.health[part]['temperature'] += 2

        def check_body_temperatures(self):
            for part, data in self.health.items():
                temp = data['temperature']
                if temp > 90 and not self.has_condition(part, "overheating"): self.add_condition(part, "overheating")
                elif temp < 45 and not self.has_condition(part, "hypothermia"): self.add_condition(part, "hypothermia")
                elif 45 <= temp <= 90:
                    if self.has_condition(part, "overheating"): self.remove_condition(part, "overheating")
                    if self.has_condition(part, "hypothermia"): self.remove_condition(part, "hypothermia")

        def apply_room_temperature(self, room_temp):
            for part in self.health:
                variation = random.uniform(-3, 3)
                if part == "body": variation += random.uniform(7, 12)
                if part == "head": variation += random.uniform(3, 7)
                self.health[part]['temperature'] = round(room_temp + variation)
            self.check_body_temperatures()

        def use_medkit_item(self, part, item_name):
            if item_name not in medkit_contents:
                renpy.notify(f"You don't have {item_name.capitalize()} in your medkit!")
                return
            healing_info = medkit_contents[item_name]
            for condition in healing_info.get("conditions", []):
                if self.has_condition(part, condition): self.remove_condition(part, condition)
            self.heal(part, healing_info.get("healing", 0))
            del medkit_contents[item_name]
            renpy.notify(f"Used {item_name.capitalize()} on {self.name}'s {part.replace('_', ' ')}.")            
      
        def _get_emotion_bonus(self, skill_name):
            sorted_emotions = sorted(self.emotions.items(), key=lambda x: x[1]["value"], reverse=True)
            if not sorted_emotions:
                return 0, []        

            bonuses = []
            total_bonus = 0
            multipliers = [1.0, 0.8, 0.6, 0.4, 0.2]  # Progressive reduction for top 5
            
            for i in range(min(5, len(sorted_emotions))):
                emo, data = sorted_emotions[i]
                base_bonus = data.get("bonus", {}).get(skill_name, 0)
                value_scale = data["value"] / 50.0  # Scale: 0 -> 0x, 50 -> 1x, 100 -> 2x
                scaled_bonus = int(base_bonus * value_scale)
                effective_bonus = int(scaled_bonus * multipliers[i])
                if effective_bonus != 0:
                    bonuses.append((emo, effective_bonus))
                total_bonus += effective_bonus
                
            return total_bonus, bonuses

        def _initialize_stats(self):
            for stat_name, data in self.stats.items():
                level = data.get("level", 1)
                data["current_value"] = (level * 4) + random.randint(1, 6)

        def add_experience(self, stat_name, amount):
            if stat_name in self.stats:
                stat = self.stats[stat_name]
                stat["current_xp"] += amount
                if stat["current_xp"] >= stat["max_xp"]:
                    self.level_up(stat_name)

        def level_up(self, stat_name):
            if stat_name in self.stats:
                stat = self.stats[stat_name]
                stat["level"] += 1
                stat["current_xp"] = 0
                stat["max_xp"] = round(stat["max_xp"] + random.randint(10, 35))
                stat["current_value"] += random.randint(1, 8)
                renpy.notify(f"{self.name}'s {stat_name.capitalize()} increased to level {stat['level']}!")

        def take_damage(self, part, amount):
            if part in self.health:
                self.health[part]['health'] -= amount
                renpy.notify(f"{self.name} took {amount} damage to the {part}.")
                if self.health[part]['health'] <= 0:
                    self.health[part]['health'] = 0

        def heal(self, part, amount):
            if part in self.health:
                max_health = 100
                self.health[part]['health'] += amount
                if self.health[part]['health'] > max_health:
                    self.health[part]['health'] = max_health

        def get_top_emotions(self):
            sorted_emotions = sorted(self.emotions.items(), key=lambda x: x[1]["value"], reverse=True)
            return sorted_emotions[:3]    
    class Inventory:
        def __init__(self, owner, capacity=20):
            self.owner = owner
            self.capacity = capacity
            self.items = []  # List of dicts: [{"name": str, "current_durability": int, "broken": bool}, ...]
            self.equipment = {
                "head": None, "body": None, "left_arm": None, "right_arm": None,
                "left_hand": None, "right_hand": None, "left_leg": None, "right_leg": None
            }
            self.liquids = [
                {"name": "Water", "amount": 100}, {"name": "Ethanol", "amount": 50},
                {"name": "Oil", "amount": 30}, {"name": "Glue", "amount": 30}
            ]
            self.containers = [
                {"name": "Regular Bottle", "capacity": 100, "current_amount": 0, "contents": []},
                {"name": "Water Bottle", "capacity": 500, "current_amount": 0, "contents": []},
            ]

        def calculate_total_weight(self):
            return sum(items_database.get(item["name"], {}).get("weight", 1) for item in self.items)
        
        def get_item_amount(self, liquid_name):
            for liquid in self.liquids:
                if liquid["name"] == liquid_name:
                    return liquid["amount"]
            return 0
        
        def has_stirring_tool(self, tool):
            return any(item["name"].lower() == tool.lower() for item in self.items)

        def get_item_weight(self, item_name):
            return items_database.get(item_name, {}).get("weight", 1)
        
        @property
        def max_weight(self):
            strength_value = self.owner.stats.get("strength", {}).get("current_value", 0)
            return 50 + (strength_value * 5)  # Example formula; adjust as needed
        
        def get_total_weight(self):
            return sum(self.get_item_weight(item["name"]) for item in self.items)

        def add_item(self, item_name):
            if item_name not in items_database:
                renpy.notify(f"System Error: Item '{item_name}' does not exist.")
                return False
            if len(self.items) >= self.capacity:
                renpy.notify("Inventory is full.")
                return False
            
            item_data = items_database[item_name]
            max_dur = item_data.get("max_durability", -1)  # Default to indestructible
            current_dur = max_dur if max_dur >= 0 else -1  # Start at max or infinite
            
            self.items.append({"name": item_name, "current_durability": current_dur, "broken": False})
            renpy.notify(f"Added '{item_name}' to inventory (Durability: {current_dur if current_dur >= 0 else 'Infinite'}).")
            return True

        def remove_item(self, item_name):
            for i, item in enumerate(self.items):
                if item["name"] == item_name:
                    del self.items[i]
                    return True
            return False
    
        def equip(self, item_name, slot):
            for item in self.items:
                if item["name"] == item_name:
                    if item.get("broken", False):
                        renpy.notify(f"Cannot equip broken {item_name}.")
                        return
                    if slot not in self.equipment:
                        renpy.notify(f"System Error: Invalid slot '{slot}'.")
                        return
                    if self.equipment[slot] is not None:
                        self.unequip(slot)
                    self.equipment[slot] = item  # Store the full item dict
                    self.items.remove(item)
                    renpy.notify(f"Equipped {item_name}.")
                    return
            renpy.notify(f"Cannot equip: {item_name} not in inventory.")
            return

        def unequip(self, slot):
            if slot not in self.equipment or self.equipment[slot] is None:
                renpy.notify(f"Nothing to unequip from {slot}.")
                return
            item = self.equipment[slot]
            self.equipment[slot] = None
            self.items.append(item)
            # Optional: Decrease durability on unequip (e.g., wear from use)
            self.decrease_durability(item["name"], amount=1)
            renpy.notify(f"Unequipped {item['name']}.")

        def use_item(self, item_name):
            for item in self.items:
                if item["name"] == item_name:
                    if item.get("broken", False):
                        renpy.notify(f"Cannot use broken {item_name}.")
                        return
                    self.decrease_durability(item_name, amount=1)
                    if item_name == "Classified Mission Sheet":
                        renpy.show_screen("scp_memo")
                    elif item_name == "First aid kit":
                        self.remove_item(item_name)
                        renpy.show_screen("heal_menu")
                    elif item_name == "Radio":
                        renpy.show_screen("radio_ui")
                    elif item_name == "Tissue":
                        self.remove_item(item_name)
                        self.add_item("Wet Tissue")
                        renpy.notify("You blow your nose.")
                    else:
                        renpy.notify(f"You can't use the {item_name} right now.")
                    return
            return
        def decrease_durability_func(self,item_name,num): #this is really stupid but it works
            self.decrease_durability(item_name, amount=num)
            

        def is_broken(self, item_name):
            for item in self.items:
                if item["name"] == item_name:
                    return item.get("broken", False)
            for slot, equipped_item in self.equipment.items():
                if equipped_item and equipped_item["name"] == item_name:
                    return equipped_item.get("broken", False)
            return False

        def has_item(self, item_name):
            if any(item["name"] == item_name for item in self.items):
                return True
            for slot, equipped_item in self.equipment.items():
                if equipped_item and equipped_item["name"] == item_name:
                    return True
            return False

        # New: Decrease durability for an item (e.g., on use)
        def decrease_durability(self, item_name, amount=1):
            for item in self.items:
                if item["name"] == item_name:
                    if item["current_durability"] < 0:  # Indestructible
                        return True
                    item["current_durability"] = max(0, item["current_durability"] - amount)
                    if item["current_durability"] <= 0:
                        self.handle_breakage(item_name)
                    elif item["current_durability"] <= 10:  # Low durability warning
                        renpy.notify(f"Warning: {item_name} durability low ({item['current_durability']}).")
                    else:
                        renpy.notify(f"{item_name} durability decreased to {item['current_durability']}.")
                    return True
            # Check equipped items too
            for slot, equipped in self.equipment.items():
                if equipped and equipped["name"] == item_name:
                    if equipped["current_durability"] < 0:
                        return True
                    equipped["current_durability"] = max(0, equipped["current_durability"] - amount)
                    if equipped["current_durability"] <= 0:
                        self.handle_breakage(item_name)  # Could auto-unequip here if desired
                    elif equipped["current_durability"] <= 10:
                        renpy.notify(f"Warning: Equipped {item_name} durability low ({equipped['current_durability']}).")
                    else:
                        renpy.notify(f"Equipped {item_name} durability decreased to {equipped['current_durability']}.")
                    return True
            return False  # Item not found

        # New: Increase/repair durability
        def increase_durability(self, item_name, amount=1, max_override=None):
            for item in self.items:
                if item["name"] == item_name:
                    max_dur = max_override or items_database[item_name].get("max_durability", -1)
                    if max_dur < 0 or not items_database[item_name].get("repairable", False):
                        renpy.notify(f"{item_name} cannot be repaired.")
                        return False
                    item["current_durability"] = min(max_dur, item["current_durability"] + amount)
                    if item.get("broken", False) and item["current_durability"] > 0:
                        item["broken"] = False
                        renpy.notify(f"{item_name} repaired and usable again.")
                    else:
                        renpy.notify(f"{item_name} durability increased to {item['current_durability']}.")
                    return True
            # Check equipped items too
            for slot, equipped in self.equipment.items():
                if equipped and equipped["name"] == item_name:
                    max_dur = max_override or items_database[equipped["name"]].get("max_durability", -1)
                    if max_dur < 0 or not items_database[equipped["name"]].get("repairable", False):
                        renpy.notify(f"{equipped['name']} cannot be repaired.")
                        return False
                    equipped["current_durability"] = min(max_dur, equipped["current_durability"] + amount)
                    if equipped.get("broken", False) and equipped["current_durability"] > 0:
                        equipped["broken"] = False
                        renpy.notify(f"Equipped {equipped['name']} repaired and usable again.")
                    else:
                        renpy.notify(f"Equipped {equipped['name']} durability increased to {equipped['current_durability']}.")
                    return True
            return False

        def handle_breakage(self, item_name):
            renpy.notify(f"{item_name} has broken! (Durability reached 0).")
            for item in self.items:
                if item["name"] == item_name:
                    item["broken"] = True
                    return
            for slot, equipped in self.equipment.items():
                if equipped and equipped["name"] == item_name:
                    equipped["broken"] = True
                    self.unequip(slot)
                    return