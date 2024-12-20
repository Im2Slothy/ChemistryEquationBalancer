from sympy import symbols, Eq, solve

def balance_equation(equation):
    # Split the equation into reactants and products
    reactants, products = equation.split('->')

    # Parse the reactants and products into lists of (element, count) tuples
    def parse_side(side):
        elements = []
        current_element = ''
        current_count = 0
        for char in side:
            if char.isalpha():
                if current_element:
                    elements.append((current_element, current_count if current_count else 1))
                current_element = char
                current_count = 0
            elif char.isdigit():
                current_count = current_count * 10 + int(char)
        elements.append((current_element, current_count if current_count else 1))
        return elements

    reactants = parse_side(reactants)
    products = parse_side(products)

    # Create symbols for the stoichiometric coefficients
    a, b, c, d = symbols('a b c d')

    # Set up equations based on the number of atoms of each element
    equations = []
    for element in set([elem for elem, _ in reactants] + [elem for elem, _ in products]):
        reactant_count = sum([count for elem, count in reactants if elem == element])
        product_count = sum([count for elem, count in products if elem == element])
        equations.append(Eq(a * reactant_count, c * product_count))

    # Solve the system of equations
    solution = solve(equations)

    # Find the least common multiple (LCM) of the denominators in the solution
    lcm = 1
    for val in solution.values():
        if val.as_numer_denom()[1] != 1:
            lcm = sympy.lcm(lcm, val.as_numer_denom()[1])

    # Multiply the coefficients by the LCM to get integer values
    coefficients = [int(coeff * lcm) for coeff in solution.values()]

    # Construct the balanced equation
    balanced_equation = ' + '.join([f'{coeff if coeff > 1 else ""}{elem}' for coeff, (elem, _) in zip(coefficients, reactants)])
    balanced_equation += ' -> '
    balanced_equation += ' + '.join([f'{coeff if coeff > 1 else ""}{elem}' for coeff, (elem, _) in zip(coefficients, products)])

    return balanced_equation

#put your equation here :p EX:
unbalanced_equation = "Fe2O3 + Fe -> O2"

# Balance the equation
balanced_equation = balance_equation(unbalanced_equation)

# Print the balanced equation
print(balanced_equation)
