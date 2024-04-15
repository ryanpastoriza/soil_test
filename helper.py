# 1 hectare (10,000 square meters).
# 1 kilogram per hectare = 0.892 pounds per acre
# 1 pound per acre = 1.121 kilograms per hectare
# 1 kg/ha = 0.8927 pounds per acre

# def kilogramsPerHectare(mg):
# 	kg = (mg/1000000)
# 	return kg * 1

# actual
# desired
# area
def deficiency(actual, desired, area):

	required = {}

	for nutrient, value in actual.items():
		# Convert mg/kg to kg/kg - kg/kg to kg/ha 		
		converted = toKilogramPerHectare(toKilogram(value), area)
		# Compute deficiency actual - desired
		deficient = desired[nutrient] - converted
		required.update({ nutrient : round(deficient, 4) })
	
	return required;

def formatNumber(val):
	return '{:.10f}'.format(val).rstrip('0').rstrip('.')

# conver mg/kg to kg/kg
def toKilogram(milligram):
	return (milligram/1000000)


def toKilogramPerHectare(kilogram, area):
	return (kilogram * area)

def getScore():
	# Define recommended nutrient levels (example values)
	recommended_levels = {
	    'N': 80,  # Recommended nitrogen level in kg/ha
	    'P': 20,  # Recommended phosphorus level in kg/ha
	    'K': 50,  # Recommended potassium level in kg/ha

	}

	# Define actual nutrient levels supplied (example values)
	supplied_levels = {
	    'N': 70,  # Supplied nitrogen level in kg/ha
	    'P': 25,  # Supplied phosphorus level in kg/ha
	    'K': 40,  # Supplied potassium level in kg/ha

	}

	# Define deduction rules
	deductions = {
	    'N': 5,   # Deduct 5 points if N is outside 10% of recommended level
	    'P': 2,   # Deduct 2 points if P is too high
	    'K': 3,   # Deduct 3 points if K is too low
	}

	# Calculate deductions for each nutrient
	total_deductions = 0
	for nutrient, recommended_level in recommended_levels.items():
	    supplied_level = supplied_levels.get(nutrient, 0)  # Get supplied level for the nutrient
	    if nutrient == 'N':
	        if supplied_level < 0.9 * recommended_level or supplied_level > 1.1 * recommended_level:
	            total_deductions += deductions[nutrient]
	    elif nutrient == 'P':
	        if supplied_level > recommended_level:
	            total_deductions += deductions[nutrient]
	    elif nutrient in ['K']:
	        if supplied_level < recommended_level:
	            total_deductions += deductions[nutrient]

	# Calculate final score
	perfect_score = 100
	final_score = max(perfect_score - total_deductions, 0)

	
	print(total_deductions)
	print(f"Final Score: {final_score}")

# def lowest(data):

# 	lowest = float('inf')
# 	key = None
# 	for k, v  in data.items():
# 		val = toKilogram(v)
# 		if v < lowest:
# 			lowest = val
# 			key = k

# 	return lowest

# def findRatio(data):

# 	low = lowest(data)
# 	ratio = {}

# 	for k, v  in data.items():

# 		result = (toKilogram(v)/low)
# 		ratio.update({ k : round(result) })

# 	print(ratio)

