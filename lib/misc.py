import re

def subvars(expr, vars):
    for var_name in vars:
        if f'@{var_name}@' in expr:
            expr = re.sub(f'@{var_name}@', str(vars[var_name]), expr)
    return expr