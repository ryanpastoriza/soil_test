# import database
# import soiltest
import helper
import data
# from itertools import combinations
# from tkinter import *
# import customtkinter
import serial

def selectFertilizer(deficient, fertilizer_grades):

	best_grade = None
	best_score = float('inf')

	for grade, nutrient_content in data.fertilizer_grades.items():
		score = 0
		for key, value in deficient.items():
			if nutrient_content[key] > 0:
				# print(f"{value} - {value / (nutrient_content[key]/100)}")
				score += value / (nutrient_content[key]/100)

		# print('Score')
		# print(grade)
		# print(score)
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

# Recommendations are expressed in Kilograms per acre (kg/acre)
def initialize():

	# customtkinter.set_appearance_mode("dark")
	# customtkinter.set_default_color_theme("dark-blue")

	# root = customtkinter.CTk()
	# root.title("Soil Test App")
	# root.geometry('400x400')
	# root.mainloop()
	# 50 kg = 1 bag
	bag = 50

	# define area in Hectares
	area = 1

	# get NPK value from sensor
	# Convert Actual Nutrient Level from mg/kg to kg/ha
	# actual = {
	# 	'N': soiltest.nitrogen(),
	# 	'P' : soiltest.phosphorus(),
	# 	'K' : soiltest.potassium(),
	# }

	actual = {
		'N': 53,
		'P' : 40,
		'K' : 20,
	}


	# helper.findRatio(actual)

	print("Measured NPK in mg/kg")
	print(actual)
	print()

	# Determine Desired Nutrient Level
	# get ideal NPK value for crop x
	print("Desired Nutrient Level in kg/ha")
	print(f"{data.crop['Rice']['requirement']} in {data.crop['Rice']['unit']} ")
	print()

	
	# Compute Deficiency and Find Nutrient Requirements
	deficient = helper.deficiency(actual, data.crop['Rice']['requirement'], area)

	print("Nutrient Requirements")
	print(f"{deficient}")
	print()

	
	

	uart0 = serial.Serial(port='/dev/ttyUSB0', baudrate = 4800, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)
	# uart0.open()

	
	
	while True:
		nitro = bytes.fromhex('01 03 00 1e 00 01 e4 0c')
		phos = bytes.fromhex('01 03 00 1f 00 01 b5 cc')
		pota = bytes.fromhex('01 03 00 20 00 01 85 c0')

		if uart0.write(nitro):
			Tx_Nitro = uart0.write(nitro)
			print("Sent Data : " + str(Tx_Nitro))
			Rx_Nitro = uart0.readline()
			print("Received data : " + str(Rx_Nitro))
			print(Rx_Nitro)
			# Nitrogen_Value = ((int.from_bytes(Rx_Nitro[3], 'big')) << 8) + (int.from_bytes(Rx_Nitro[4], 'big'))
			Rx_Nitro = uart0.read(7)
			print("Received data : " + str(Rx_Nitro))
			n_value = int.from_bytes(Rx_Nitro[3:5], 'big')
			print(n_value)
		else:
			print("No Data")

		
	# if uart0.write(nitro):
	# 	Rx_Nitro = uart0.read(7)
	# 	print("Received data : " + str(Rx_Nitro))
	# else:
	# 	print("No Data")
	# all_combinations = []
	# for r in range(1, min(4, len(data.fertilizer_grades) + 1)):
	#     all_combinations.extend(combinations(data.fertilizer_grades.keys(), r))


	# for combintion in all_combinations:
	# 	print(combintion)
	# 	print()

	# helper.fertilizerRecommendation(deficient, data.fertilizer_grades)
	# soiltest.nitrogen()



	# all_combinations = []
	# for r in range(1, min(4, len(data.fertilizer_grades) + 1)):
	#     all_combinations.extend(combinations(data.fertilizer_grades.keys(), r))


	# for combination in all_combinations:

	# Calculate the needed kg/ha for each fertilizer grade in the selected combination
	# needed_kg_per_grade = {}
	# for grade, proportion in proportions.items():
	#     needed_kg_per_grade[grade] = {nutrient: round(proportion * recommended_levels[nutrient], 2) for nutrient in recommended_levels}

	# # Output the needed kg/ha for each fertilizer grade
	# print("\nNeeded kg/ha for Each Fertilizer Grade:")
	# for grade, nutrient_levels in needed_kg_per_grade.items():
	#     print(f"{grade}:")
	#     for nutrient, level in nutrient_levels.items():
	#         print(f"  {nutrient}: {level} kg/ha")

	# print(len(all_combinations))

	# first_grade = selectFertilizer(deficient, data.fertilizer_grades)
	# print(first_grade)
	# Check if the first fertilizer grade is sufficient
	# is_enough = all(data.fertilizer_grades[first_grade][nutrient] >= deficient[nutrient] 
 #                for nutrient in deficient)

	# print(is_enough)

	# second_grade =  selectFertilizer(deficient, data.fertilizer_grades)

	# print(second_grade)

	# more = {}
	# for key, value in deficient.items():
	# 	# print(deficient[key])
	# 	if data.fertilizer_grades[first_grade][key] < deficient[key]:
	# 		print(f"Warning: {key} deficiency detected.")
	# 	elif data.fertilizer_grades[first_grade][key] > deficient[key]:
	# 		print(f"Warning: {key} excess detected.")

	# helper.getScore()

	# fertilizerRecommendation()


initialize()