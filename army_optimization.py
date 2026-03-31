#!/usr/bin/env python3
"""
Army Recruitment Optimization

This script solves the problem of maximizing army power given limited resources.
We have three resources: food, wood, and gold.
Three unit types: swordsmen, bowmen, and horsemen with different costs and power.

The problem is a multi-constraint knapsack optimization.
"""

# Unit definitions: (food_cost, wood_cost, gold_cost, power)
UNITS = {
    'swordsman': (60, 20, 0, 70),
    'bowman': (80, 10, 40, 95),
    'horseman': (140, 0, 100, 230)
}

# Available resources
RESOURCES = {
    'food': 1200,
    'wood': 800,
    'gold': 600
}

def calculate_power_and_costs(h, b, s):
    """
    Calculate total power and resource usage for given unit counts.
    
    Args:
        h: number of horsemen
        b: number of bowmen  
        s: number of swordsmen
        
    Returns:
        tuple: (total_power, food_used, wood_used, gold_used)
    """
    food_used = h * UNITS['horseman'][0] + b * UNITS['bowman'][0] + s * UNITS['swordsman'][0]
    wood_used = h * UNITS['horseman'][1] + b * UNITS['bowman'][1] + s * UNITS['swordsman'][1]
    gold_used = h * UNITS['horseman'][2] + b * UNITS['bowman'][2] + s * UNITS['swordsman'][2]
    power = h * UNITS['horseman'][3] + b * UNITS['bowman'][3] + s * UNITS['swordsman'][3]
    
    return power, food_used, wood_used, gold_used

def find_optimal_army():
    """
    Find the optimal army composition by trying all feasible combinations.
    
    Returns:
        dict: optimal composition and stats
    """
    max_power = 0
    optimal_composition = None
    
    # Maximum possible units (rough bounds)
    max_h = min(RESOURCES['food'] // UNITS['horseman'][0], 
                RESOURCES['gold'] // UNITS['horseman'][2]) + 1
    max_b = min(RESOURCES['food'] // UNITS['bowman'][0],
                RESOURCES['wood'] // UNITS['bowman'][1],
                RESOURCES['gold'] // UNITS['bowman'][2]) + 1
    max_s = min(RESOURCES['food'] // UNITS['swordsman'][0],
                RESOURCES['wood'] // UNITS['swordsman'][1]) + 1
    
    # Brute force search
    for h in range(max_h):
        for b in range(max_b):
            for s in range(max_s):
                power, food_used, wood_used, gold_used = calculate_power_and_costs(h, b, s)
                
                # Check resource constraints
                if (food_used <= RESOURCES['food'] and 
                    wood_used <= RESOURCES['wood'] and 
                    gold_used <= RESOURCES['gold']):
                    
                    if power > max_power:
                        max_power = power
                        optimal_composition = {
                            'horsemen': h,
                            'bowmen': b,
                            'swordsmen': s,
                            'power': power,
                            'resources_used': {
                                'food': food_used,
                                'wood': wood_used,
                                'gold': gold_used
                            },
                            'resources_remaining': {
                                'food': RESOURCES['food'] - food_used,
                                'wood': RESOURCES['wood'] - wood_used,
                                'gold': RESOURCES['gold'] - gold_used
                            }
                        }
    
    return optimal_composition

def main():
    """Main function to run the optimization and display results."""
    print("Army Recruitment Optimization")
    print("=" * 40)
    print(f"Available Resources: {RESOURCES}")
    print()
    
    print("Unit Costs and Power:")
    for unit, (food, wood, gold, power) in UNITS.items():
        print(f"  {unit.capitalize()}: {food}🌾 {wood}🪵 {gold}🪙 → {power}💪")
    print()
    
    optimal = find_optimal_army()
    
    if optimal:
        print("Optimal Army Composition:")
        print(f"  Horsemen: {optimal['horsemen']}")
        print(f"  Bowmen: {optimal['bowmen']}")
        print(f"  Swordsmen: {optimal['swordsmen']}")
        print(f"  Total Power: {optimal['power']}💪")
        print()
        print("Resource Usage:")
        for resource, used in optimal['resources_used'].items():
            remaining = optimal['resources_remaining'][resource]
            print(f"  {resource.capitalize()}: {used} used, {remaining} remaining")
    else:
        print("No valid army composition found!")

if __name__ == "__main__":
    main()