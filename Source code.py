from MFIS_Read_Functions import *
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as skf


def plot_degree_function(fuzzySets, fuzzy_data):
    """ Plots the functions of the fuzzy sets """
    for fs in fuzzySets.values():
        for var in {fs.var}:
            plt.figure()
            plt.title(f'Functions for {var}')
            plt.xlabel(var)
            plt.ylabel('Degree')
            for label, fuzzy_set in fuzzySets.items():
                if fuzzy_set.var == var:
                    plt.plot(fuzzy_set.x, fuzzy_set.y, label=label)
                    if label in fuzzy_data:
                        degree = fuzzy_data[label]
                        plt.fill_between(fuzzy_set.x, 0.0, fuzzy_set.y, where=(fuzzy_set.y <= degree), alpha=0.3)
            plt.legend()
            plt.grid(True)
            plt.show()


def fuzzify(fuzzy_sets, data):
    fuzzy_data = {}  # Dictionary to store degree for each fuzzy set
    for var, value in data:  # Loop through each variable-value
        # Find fuzzy sets corresponding to the variable
        for fuzzy_set_key, fuzzy_set in fuzzy_sets.items():
            if fuzzy_set.var == var:  # Check the variable is the one we want
                degree = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, value)  # Calculate degree
                fuzzy_data[fuzzy_set_key] = degree  # Store the degree in the dictionary
    return fuzzy_data


def apply_rules(rules_List, fuzzy_data):
    """ Apply the inference rules to the fuzzified data """
    degrees = []  # List to store rule strengths
    for rule in rules_List:  # Read each rule
        antecedent_degrees = []  # Empty list to store the degrees of the antecedents
        for antecedent in rule.antecedent:
            if antecedent in fuzzy_data:  # Check if the variable exists
                antecedent_degrees.append(fuzzyData[antecedent])
        if antecedent_degrees:  # Determine rule degree
            rule_degree = min(antecedent_degrees)  # Use minimum for AND logic
            degrees.append((rule.consequent, rule_degree))  # Add to the list
    return degrees


def defuzzify(rule_strengths):
    risks = np.arange(0, 100.1, 0.1)  # Create an array ranging from 0 to 100
    results = {'LowR': 0, 'MediumR': 0, 'HighR': 0}

    for rule, degree in rule_strengths:
        if rule == 'Risk=LowR':
            results['LowR'] = max(results['LowR'], degree)  # Get the max degree from this label
        elif rule == 'Risk=MediumR':
            results['MediumR'] = max(results['MediumR'], degree)  # Get the max degree from this label
        elif rule == 'Risk=HighR':
            results['HighR'] = max(results['HighR'], degree)  # Get the max degree from this label

    max_degrees = [results['LowR'], results['MediumR'], results['HighR']]  # Array with the final max degrees values

    # We get the trapezoidal function graph for each risk
    low_risk = skf.trapmf(risks, [-20, -10, 30, 50])
    medium_risk = skf.trapmf(risks, [10, 40, 70, 90])
    high_risk = skf.trapmf(risks, [50, 70, 100, 111])

    # Calculate the area for each trapezoidal function
    weighted_functions = [
        low_risk * max_degrees[0],
        medium_risk * max_degrees[1],
        high_risk * max_degrees[2]
    ]
    combined_function = np.sum(weighted_functions, axis=0)  # Sum of all area
    centroid = skf.defuzz(risks, combined_function, 'centroid')  # Get centroid
    return centroid


# MAIN FUNCTION
fuzzySets = readFuzzySetsFile('Files/InputVarSets.txt')  # Read the fuzzy sets
rulesList = readRulesFile()  # Read Inference Rules
application = readApplicationsFile()  # Read Loan Applications

result = []  # Empty list to store the results
for app in application:
    fuzzyData = fuzzify(fuzzySets, app.data)  # Fuzzify the input data
    rule_degrees = apply_rules(rulesList, fuzzyData)  # Apply the inference rules
    final_centroid = defuzzify(rule_degrees)  # De-fuzzify the output to get the risk score
    result.append((app.appId, final_centroid))  # Store the result (application ID and risk score)
    plot_degree_function(fuzzySets, fuzzyData)  # Show graph of each variable for each application

with open("Files/Results.txt", "w") as output_file:  # Write results to a file
    for app_id, risk in result:
        output_file.write(f"{app_id}, {risk:.2f}\n")
