#starting effects

image dim_overlay:
    xysize (config.screen_width, config.screen_height)
    Solid("#000000") 
    alpha 0.0      
    linear 1.0 alpha 0.6 

image light_turning_on_effect:
    Solid("#FFFFFF") 
    alpha 0.0
    xysize (config.screen_width, config.screen_height)
    linear 0.05 alpha 0.6 
    pause 0.1
    linear 0.15 alpha 0.0
image light_turning_on_effect:
    Solid("#FFFFFF") 
    alpha 0.0
    xysize (config.screen_width, config.screen_height)
    linear 0.1 alpha 0.6 
    pause 0.1
    linear 0.35 alpha 0.0    
init python:
    # Add a custom layer for dimming effects if it doesn't exist
    if 'dimming_layer' not in config.layers:
        try:
            master_index = config.layers.index('master')
            config.layers.insert(master_index + 1, 'dimming_layer')
        except ValueError:
            config.layers.append('dimming_layer')
        