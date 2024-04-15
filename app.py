import database
import soiltest
import helper
import data
from itertools import combinations

# def dbInit():
# 		connection = database.connect()
# 		database.create_tables(connection)
# 		database.add_fertilizer(connection, "Urea", "46-0-0", 46, 0, 0)
# 		database.add_fertilizer(connection, "Triple 14 Complete Fertilizer", "14-14-14", 14, 14, 14)
# 		database.add_fertilizer(connection, "Ammonium Sulfate", "21-0-0", 21, 0, 0)
# 		database.add_fertilizer(connection, "Single Superphosphate", "0-18-0", 0, 18, 0)
# 		database.add_fertilizer(connection, "Potassium chloride ", "0-0-60", 0, 0, 60)
# 		database.add_crop(connection, "rice", 90, 20, 40, "kg/ha")

# def getCrop(name):
# 		connection = database.connect()
# 		crop = database.get_crop_by_name(connection, name)

# 		return {
# 			"n" : crop[2],
# 			"p" : crop[3],
# 			"k" : crop[4]
# 		}

# def getFertilizers():
# 		connection = database.connect()
# 		fertilizers = database.get_fertilizers(connection)

# 		return fertilizers

def selectFertilizer(deficient, fertilizer_grades):

	best_grade = None
	best_score = float('inf')

	for grade, nutrient_content in data.fertilizer_grades.items():
		score = 0
		for key, value in deficient.items():
			if nutrient_content[key] > 0:
				# print(f"{value} - {value / (nutrient_content[key]/100)}")
				score += value / (nutrient_content[key]/100)

		print('Score')
		print(grade)
		print(score)
		if( score < best_score ):
			best_grade = grade
			best_score = score

	return best_grade

# Function to calculate nutrient content for a given combination of fertilizer grades
def calculate_nutrient_content(combination):
    total_content = {'N': 0, 'P': 0, 'K': 0}
    for grade in combination:
        for nutrient in total_content:
            total_content[nutrient] += data.fertilizer_grades[grade].get(nutrient, 0)
    return total_content

# Function to evaluate the effectiveness of a combination
def evaluate_combination(combination):
    content = calculate_nutrient_content(combination)
    deficit = {nutrient: max(0, data.crop['Rice']['requirement'][nutrient] - content.get(nutrient, 0)) for nutrient in data.crop['Rice']['requirement']}
    total_deficit = sum(deficit.values())
    return total_deficit, content


def generateCombination():

	all_combinations = []
	for r in range(1, min(4, len(data.fertilizer_grades) + 1)):
	    all_combinations.extend(combinations(data.fertilizer_grades.keys(), r))

	# Initialize variables to store the best combination and its nutrient content
	best_combination = None
	best_difference = float('inf')

	# Iterate through each combination and calculate the nutrient content
	for combination in all_combinations:
	    total_content = {'N': 0, 'P': 0, 'K': 0}
	    for grade in combination:
	        for nutrient in total_content:
	            total_content[nutrient] += data.fertilizer_grades[grade][nutrient]

	    # Calculate the difference from the recommended levels
	    difference = sum(abs(total_content[nutrient] - data.crop['Rice']['requirement'][nutrient]) for nutrient in data.crop['Rice']['requirement'])
	    # Update the best combination if the difference is smaller
	    if difference < best_difference:
	        best_combination = combination
	        best_difference = difference

	return best_combination, best_difference, total_content

def fertilizerRecommendation():
	# Define recommended nutrient levels
	recommended_levels = data.crop['Rice']['requirement']

	fertilizer_grades = data.fertilizer_grades

	# Generate all possible combinations of fertilizer grades (up to 3 grades per combination)
	
	best_combination, best_difference, total_content = generateCombination()
	# Output the best combination and its nutrient content
	print("Best Combination:", best_combination)
	print("Best Combination:", best_difference)
	print("Total Nutrient Content:")
	for nutrient in recommended_levels:
	    print(f"{nutrient}: {total_content[nutrient]}")


	# Initialize variables to store the proportion of each grade in the best combination
	proportions = {}

	# Calculate the total nutrient content for the best combination
	total_content = {'N': 0, 'P': 0, 'K': 0}
	for grade in best_combination:
	    for nutrient in total_content:
	        total_content[nutrient] += fertilizer_grades[grade][nutrient]

	print(total_content)
	print('----')
	# Calculate the proportion of each grade in the best combination
	for grade in best_combination:
	    proportions[grade] = sum(fertilizer_grades[grade][nutrient] for nutrient in recommended_levels) / total_content['N']

	print(proportions)
	print('----')
	# Calculate the amount of each fertilizer grade needed (in kg/ha)
	amounts = {}
	for grade, proportion in proportions.items():
	    amounts[grade] = round(proportion * recommended_levels['N'], 2)

	# Output the amount of each fertilizer grade needed
	print("Amount of Each Fertilizer Grade Needed (kg/ha):")
	for grade, amount in amounts.items():
	    print(f"{grade}: {amount}")
	# Output the recommended and supplied nutrient levels
	print("Recommended Nutrient Levels:")
	for nutrient, level in recommended_levels.items():
	    print(f"{nutrient}: {level} kg/ha")
	    
	print("\nSupplied Nutrient Levels:")
	for nutrient, level in total_content.items():
	    print(f"{nutrient}: {level} kg/ha")

	# Calculate the deficit for each nutrient
	deficit = {}
	for nutrient, level in recommended_levels.items():
	    deficit[nutrient] = max(0, level - total_content.get(nutrient, 0))

	# Output the deficit for each nutrient
	print("\nDeficit for Each Nutrient:")
	for nutrient, value in deficit.items():
	    print(f"{nutrient}: {value} kg/ha")

	# Adjust proportions of grades in the best combination
	adjusted_combination = best_combination  # Start with the initially identified best combination
	print(adjusted_combination)
	# # Adjust proportions as needed
	# # Example: adjusted_combination = ('46-0-0', '14-14-14', '21-0-0')

	# # Calculate nutrient content and deficit for the adjusted combination
	adjusted_deficit, adjusted_content = evaluate_combination(adjusted_combination)
	print("Adjusted Combination Nutrient Content:", adjusted_content)
	print("Adjusted Combination Total Deficit:", adjusted_deficit)

	# Explore alternative combinations
	# alternative_combinations = adjusted_combination
	# Generate and evaluate alternative combinations
	# for combination in alternative_combinations:
	#     total_deficit, content = evaluate_combination(combination)
    # Compare with the adjusted combination or other combinations
    # Choose the combination that minimizes the deficit or meets the requirements satisfactorily


# Recommendations are expressed in Kilograms per acre (kg/acre)
def initialize():
	# dbInit()

	# 50 kg = 1 bag
	bag = 50

	# define area in Hectares
	area = 1

	# get NPK value from sensor
	# Convert Actual Nutrient Level from mg/kg to kg/ha
	actual = {
		'N': soiltest.nitrogen(),
		'P' : soiltest.phosphorus(),
		'K' : soiltest.potassium(),
	}

	# helper.findRatio(actual)

	print("Measured NPK in mg/kg")
	print(actual)
	print()

	# Determine Desired Nutrient Level
	# get ideal NPK value for crop x
	print("Desired Nutrient Level in kg/ha")
	print(f"{data.crop['Rice']['requirement']}")
	print()

	
	# Compute Deficiency and Find Nutrient Requirements
	deficient = helper.deficiency(actual, data.crop['Rice']['requirement'], area)

	print("Nutrient Requirements")
	print(f"{deficient}")
	print()


	first_grade = selectFertilizer(deficient, data.fertilizer_grades)

	# Check if the first fertilizer grade is sufficient
	is_enough = all(data.fertilizer_grades[first_grade][nutrient] >= deficient[nutrient] 
                for nutrient in deficient)

	# print(is_enough)

	# second_grade =  selectFertilizer(deficient, data.fertilizer_grades)

	# more = {}
	# for key, value in deficient.items():
	# 	# print(deficient[key])
	# 	if data.fertilizer_grades[first_grade][key] < deficient[key]:
	# 		print(f"Warning: {key} deficiency detected.")
	# 	elif data.fertilizer_grades[first_grade][key] > deficient[key]:
	# 		print(f"Warning: {key} excess detected.")

	# helper.getScore()

	fertilizerRecommendation()


initialize()
# Fertilizer recommendations given in kg/ha.
# Conduct Sensor Reading
	# Retrieve NPK Value
		# N (X kg/ha)
		# P (X kg/ha)
		# K (X kg/ha)

# Interpret fertilizer recommendation

# Compare nutrient level to crop requirement
	

		
	# Compute for the Deficiency
		# Deficiency = Recommended N Level - Measured N Level

# Interpret fertilizer recommendation
	# 


# Amount of Required Nutrient
 	# N (90 to 120 kg/ha)
	# P (20 to 40 kg/ha)
	# K (40 to 80 kg/ha)


# Convert Actual Nutrient Level from mg/kg to kg/ha
# Determine Desired Nutrient Level
# Compute Deficiency:
# Adjust for Area: