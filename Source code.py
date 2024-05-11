from MFIS_Read_Functions import *
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as skf


def trapezoidal_func(x, a, b, c, d):
    """ Calculates the degree given a value x """
    if x <= a:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)  # Linear increase
    elif b <= x <= c:
        return 1  # Constant
    elif c < x < d:
        return (d - x) / (d - c)  # Linear decrease
    elif d <= x:
        return 0


def fuzzify(fuzzySets, application):
    data = {}  # Dictionary to store degree for each fuzzy set
    # Loop through each variable-value
    for var, value in application.data:
        # Find fuzzy sets corresponding to the variable
        for fuzzy_set_key, fuzzy_set in fuzzySets.items():
            if fuzzy_set.var == var:
                #if len(fuzzy_set.x) >= 4:
                # Calculate the degree for the given value
                    #a, b, c, d = fuzzy_set.x[0], fuzzy_set.x[1], fuzzy_set.x[2], fuzzy_set.x[3]
                a, b, c, d = fuzzy_set.x[:4]
                degree = trapezoidal_func(value, a, b, c, d)
                # Store the degree in the dictionary
                data[fuzzy_set_key] = degree
                print(f"Fuzzify {fuzzy_set_key}: {degree}")  # Debug print

    return data


def apply_rules(rules_List, fuzzyData):
    """ Returns a list of (consequent, strength) pairs """
    rule_strengths = []  # List to store rule strengths
    # Read each rule
    for rule in rules_List:
        # Calculate the minimum degree among the rule's antecedents
        antecedent_strengths = []  # Empty list to store the strengths of the antecedents
        for antecedent in rule.antecedent:
            if antecedent in fuzzyData:
                antecedent_strengths.append(fuzzyData[antecedent])

        # Determine rule strength based on the minimum degree
        if antecedent_strengths:
            rule_strength = min(antecedent_strengths)  # Use minimum for AND logic
        else:
            rule_strength = 0  # Default to 0

        print(f"Rule: {rule.ruleName}, Strength: {rule_strength}")  # Debug print
        rule_strengths.append((rule.consequent, rule_strength))
    return rule_strengths


def defuzzify(rule_strengths):
    strengths = []
    # Extract strengths from rule_strengths
    for _, strength in rule_strengths:
        strengths.append(strength)  # Append the strength to the list

    # Find the maximum strength (the strongest output among all rules)
    if strengths:
        risks = np.max(strengths)  # Use the maximum rule strength
    else:
        risks = 0  # Default to zero risk

    print(f"Final Risk: {risks}")  # Debug print
    return risks


def process_applications(fuzzySets, rules_List, applications):
    """ Process loan applications """
    result = []
    for app in applications:
        fuzzyData = fuzzify(fuzzySets, app)  # Fuzzify the input data
        rule_strengths = apply_rules(rules_List, fuzzyData)  # Apply the inference rules
        risks = defuzzify(rule_strengths)  # Defuzzify the output to get the risk score
        result.append((app.appId, risks))  # Store the result (application ID and risk score)
    return result


fuzzy_sets = readFuzzySetsFile('Files/InputVarSets.txt')  # Read the fuzzy sets
# fuzzySetsDict.printFuzzySetsDict()
rulesList = readRulesFile()  # Read Inference Rules
application = readApplicationsFile()  # Read Loan Applications
results = process_applications(fuzzy_sets, rulesList, application)

# Write results to a file
with open("Files/Results.txt", "w") as output_file:
    for app_id, risk in results:
        output_file.write(f"{app_id}, {risk:.2f}\n")


