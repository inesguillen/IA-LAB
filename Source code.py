from MFIS_Read_Functions import *
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as skf


def plot_membership_function(fuzzy_sets):
    """Plots the membership functions of the fuzzy sets."""
    for fuzzy_set_key, fuzzy_set in fuzzy_sets.items():
        plt.figure()
        plt.plot(fuzzy_set.x, fuzzy_set.y, label=fuzzy_set.label)
        plt.xlabel(fuzzy_set.var)
        plt.ylabel('Membership Degree')
        plt.title(f'Membership Function: {fuzzy_set.label}')
        plt.legend()
        plt.grid(True)
        plt.show()


def trapezoidal_func(x, fuzzy_set):  #a, b, c, d):
    """ Calculates the degree given a value x """
    # return skf.trapmf(x, [a, b, c, d])
    a, b, c, d = fuzzy_set.x[-4:]
    print(f"a={a}, b={b}, c={c}, d={d}, x={x}")
    degrees = skf.trapmf(x, [a, b, c, d])
    print("Membership degrees:", degrees)
    return degrees


def fuzzify(fuzzySets, data):
    fuzzy_data = {}  # Dictionary to store degree for each fuzzy set
    for var, value in data:  # Loop through each variable-value
        # Find fuzzy sets corresponding to the variable
        for fuzzy_set_key, fuzzy_set in fuzzySets.items():
            if fuzzy_set.var == var:
                # a, b, c, d = fuzzy_set.x[0], fuzzy_set.x[1], fuzzy_set.x[2], fuzzy_set.x[3]
                a, b, c, d = fuzzy_set.x[:4]
                degree = trapezoidal_func(np.array([value]), fuzzy_set)[0]  # a, b, c, d)[0]
                fuzzy_data[fuzzy_set_key] = degree  # Store the degree in the dictionary
                # print(f"Fuzzify {fuzzy_set_key}: {degree}")  # Debug print
                print(f"Fuzzify {fuzzy_set_key}: Value={value}, Degree={degree}")  # Debug print

    return fuzzy_data


def apply_rules(rules_List, fuzzyData):
    """ Apply the inference rules to the fuzzified data """
    rule_strengths = []  # List to store rule strengths
    for rule in rules_List:  # Read each rule
        antecedent_strengths = []  # Empty list to store the strengths of the antecedents
        for antecedent in rule.antecedent:
            if antecedent in fuzzyData:
                antecedent_strengths.append(fuzzyData[antecedent])
        if antecedent_strengths:  # Determine rule strength
            rule_strength = min(antecedent_strengths)  # Use minimum for AND logic
        # else:
        #  rule_strength = 0  # Default to 0
        rule_strengths.append((rule.consequent, rule_strength))
        # print(f"Rule: {rule.ruleName}, Strength: {rule_strength}")  # Debug print
        print(f"Rule: {rule.ruleName}, Antecedents: {rule.antecedent}, Rule Strength: {rule_strength}")  # Debug print
    return rule_strengths


def defuzzify(rule_strengths):
    strengths = []
    for _, strength in rule_strengths:   # Extract strengths from rule_strengths
        strengths.append(strength)  # Append the strength to the list
    if strengths:  # Find the maximum strength (the strongest output among all rules)
        return max(strengths)  # risks


def process_applications(fuzzySets, rules_List, applications):
    """ Process loan applications """
    result = []
    for app in applications:
        print(f"Processing Application ID: {app.appId}")  # Debug print
        fuzzyData = fuzzify(fuzzySets, app.data)  # Fuzzify the input data
        rule_strengths = apply_rules(rules_List, fuzzyData)  # Apply the inference rules
        risks = defuzzify(rule_strengths)  # De-fuzzify the output to get the risk score
        result.append((app.appId, risks))  # Store the result (application ID and risk score)
    return result


# MAIN FUNCTION
fuzzy_sets = readFuzzySetsFile('Files/InputVarSets.txt')  # Read the fuzzy sets
# fuzzySetsDict.printFuzzySetsDict()
rulesList = readRulesFile()  # Read Inference Rules
application = readApplicationsFile()  # Read Loan Applications
results = process_applications(fuzzy_sets, rulesList, application)
plot_membership_function(fuzzy_sets)

# Write results to a file
with open("Files/Results.txt", "w") as output_file:
    for app_id, risk in results:
        output_file.write(f"{app_id}, {risk:.2f}\n")
