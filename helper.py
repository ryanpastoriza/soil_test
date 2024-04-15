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
		required.update({ nutrient : round(deficient, 2) })
	
	return required;

def formatNumber(val):
	return '{:.10f}'.format(val).rstrip('0').rstrip('.')

# conver mg/kg to kg/kg
def toKilogram(milligram):
	return (milligram/1000000)


def toKilogramPerHectare(kilogram, area):
	return (kilogram * area)

def fertilizerRecommendation(recommended_levels, fertilizer_grades):

	nutrient_amounts_per_grade = {grade: {nutrient: 0 for nutrient in recommended_levels} for grade in fertilizer_grades}
	total_kg_per_grade = {grade: 0 for grade in fertilizer_grades}

		# Step 1: Calculate amounts from each fertilizer grade
	for grade, percentages in fertilizer_grades.items():
	    for nutrient in recommended_levels:
	        amount_needed = max(0, recommended_levels[nutrient] - nutrient_amounts_per_grade[grade][nutrient])
	        nutrient_amounts_per_grade[grade][nutrient] += min(amount_needed, (percentages[nutrient] / 100) * sum(recommended_levels.values()))
	    # Calculate total kg/ha for the current fertilizer grade
	    total_kg_per_grade[grade] = sum(nutrient_amounts_per_grade[grade].values())

	# Output the total kg/ha for each fertilizer grade and the resulting nutrient amounts
	print("Total kg/ha for Each Fertilizer Grade:")
	for grade, total_kg in total_kg_per_grade.items():
	    print(f"{grade}: {total_kg} kg/ha")
	    print("Nutrient Amounts (kg/ha):")
	    for nutrient, amount in nutrient_amounts_per_grade[grade].items():
	        print(f"  {nutrient}: {amount}")

	deficit = calculateDeficit(recommended_levels, fertilizer_grades, nutrient_amounts_per_grade)

	print(deficit)

def calculateDeficit(recommended_levels, fertilizer_grades, nutrient_amounts_per_grade):

	deficiency = {};
	print("\nDeficit for Each Nutrient:")
	for nutrient in recommended_levels:
	    deficit = recommended_levels[nutrient] - sum(nutrient_amounts_per_grade[grade][nutrient] for grade in fertilizer_grades)
	    deficiency.update({ nutrient: deficit })
	    print(f"{nutrient}: {deficit} kg/ha")

	return deficiency