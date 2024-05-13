from MFIS_Read_Functions import *
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as skf


def plot_membership_function(fuzzySets):
    """Plots the membership functions of the fuzzy sets."""
    for fuzzy_set_key, fuzzy_set in fuzzySets.items():
        plt.figure()
        plt.plot(fuzzy_set.x, fuzzy_set.y, label=fuzzy_set.label)
        plt.xlabel(fuzzy_set.var)
        plt.ylabel('Membership Degree')
        plt.title(f'Membership Function: {fuzzy_set.label}')
        plt.legend()
        plt.grid(True)
        plt.show()


'''def trapezoidal_func(x, fuzzy_set):  # a, b, c, d):
    """ Calculates the degree given a value x """
    # return skf.trapmf(x, [a, b, c, d])
    a, b, c, d = fuzzy_set.x[-4:]
    print(f"a={a}, b={b}, c={c}, d={d}, x={x}")
    degrees = skf.trapmf(x, [a, b, c, d])
    print("Membership degrees:", degrees)
    return degrees'''


def fuzzify(fuzzySets, data):
    fuzzy_data = {}  # Dictionary to store degree for each fuzzy set
    for var, value in data:  # Loop through each variable-value
        # Find fuzzy sets corresponding to the variable
        for fuzzy_set_key, fuzzy_set in fuzzySets.items():
            if fuzzy_set.var == var:
                degree = skf.interp_membership(fuzzy_set.x, fuzzy_set.y, value)
                fuzzy_data[fuzzy_set_key] = degree  # Store the degree in the dictionary
                # print(f"Fuzzify {fuzzy_set_key}: Value={value}, Degree={degree}")  # Debug print
    return fuzzy_data


def apply_rules(rules_List, fuzzyData):
    """ Apply the inference rules to the fuzzified data """
    rule_strengths = []  # List to store rule strengths
    for rule in rules_List:  # Read each rule
        antecedent_strengths = []  # Empty list to store the strengths of the antecedents
        for antecedent in rule.antecedent:
            # print(f"Antecedent: {antecedent}")
            if antecedent in fuzzyData:
                antecedent_strengths.append(fuzzyData[antecedent])
        # print("antecedent strenght: ", antecedent_strengths)
        if antecedent_strengths:  # Determine rule strength
            rule_strength = min(antecedent_strengths)  # Use minimum for AND logic
        rule_strengths.append((rule.consequent, rule_strength))
        # print(f"Rule: {rule.ruleName}, Antecedents: {rule.antecedent}, Consequent: {rule.consequent}, Rule Strength: {rule_strength}")  # Debug print
    # print(f"Rule strenghts: {rule_strengths}")
    return rule_strengths


def defuzzify(rule_strengths):
    risk = np.arange(0, 100.1, 0.1)  # creates an array ranging from 0 to 100

    '''low_risk = skf.trapmf(risk, [-20, -10, 30, 50])
    medium_risk = skf.trapmf(risk, [10, 40, 70, 90])
    high_risk = skf.trapmf(risk, [50, 70, 100, 111])

    low_risk_degree = np.zeros_like(risks)
    medium_risk_degree = np.zeros_like(risks)
    high_risk_degree = np.zeros_like(risks)'''
    result = {'LowR': 0, 'MediumR': 0, 'HighR': 0}

    for rule, degree in rule_strengths:
        if rule == 'Risk=LowR':
            result['LowR'] = max(result['LowR'], degree)
        elif rule == 'Risk=MediumR':
            result['MediumR'] = max(result['MediumR'], degree)
        elif rule == 'Risk=HighR':
            result['HighR'] = max(result['HighR'], degree)
        # print(f"Rule: {rule}, Degree: {degree}")

    aggregated_strengths = [result['LowR'], result['MediumR'], result['HighR']]
    print("list max strenght: ", aggregated_strengths )
    centroid = skf.defuzz(risk, skf.trimf(risk, [0, 100, 100]), 'centroid')   #, aggregated_strengths)
    print("centroid: ", centroid)
    return centroid


def process_applications(fuzzySets, rules_List, applications):
    """ Process loan applications """
    result = []
    for app in applications:
        print(f"Processing Application ID: {app.appId}")  # Debug print
        print(f"Application data: {app.data}")
        fuzzyData = fuzzify(fuzzySets, app.data)  # Fuzzify the input data
        print(f"fuzzy data: {fuzzyData}")
        rule_strengths = apply_rules(rules_List, fuzzyData)  # Apply the inference rules
        print(f"rule_strengths: {rule_strengths}")
        risks = defuzzify(rule_strengths)  # De-fuzzify the output to get the risk score
        print(f"risks: {risks}")
        result.append((app.appId, risks))  # Store the result (application ID and risk score)
        print(f"result: {result}")
    return result


# MAIN FUNCTION
fuzzy_sets = readFuzzySetsFile('Files/InputVarSets.txt')  # Read the fuzzy sets
# fuzzySetsDict.printFuzzySetsDict()
rulesList = readRulesFile()  # Read Inference Rules
application = readApplicationsFile()  # Read Loan Applications
results = process_applications(fuzzy_sets, rulesList, application)
# plot_membership_function(fuzzy_sets)

# Write results to a file
with open("Files/Results.txt", "w") as output_file:
    for app_id, risk in results:
        output_file.write(f"{app_id}, {risk:.2f}\n")
