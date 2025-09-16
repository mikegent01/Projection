default nenvershowrolls = True
init python:
    import random
    import time
    import hashlib
    import pygame
    import os
    import sys 
    rng = random.randint(1, 100)       
    # --- Initialize Persistent Data ---
    if not hasattr(persistent, 'journal_entries') or persistent.journal_entries is None:
        persistent.journal_entries = []
    if not hasattr(persistent, 'missions') or persistent.missions is None:
        persistent.missions = {"active": [], "completed": []}
    def label_callback(name, abnormal):
        store.last_label = name
    config.label_callback = label_callback
    # --- Bool
    last_label = None
    if 'screenshot' in config.keymap:
         bindings = config.keymap['screenshot']
         if 's' in bindings: bindings.remove('s')  # Remove plain 'S'
         if 'shift_K_s' in bindings: bindings.remove('shift_K_s')  # Remove Shift+S
         if 'alt_shift_K_s' in bindings: bindings.remove('alt_shift_K_s')  # Remove Alt+Shift+S
         if 'noshift_K_s' in bindings: bindings.remove('noshift_K_s')  # Remove noshift variant if present
         if 'alt_K_s' in bindings: bindings.remove('alt_K_s')  # Remove Alt+S if present


label gameover:
    "You have died..."
    "Why don't you try loading a save..."
