import random
import string
from config import first_names, last_names, org_structure, org_names


def mask_gender(account_number, length, extra_params):
    allowed_values = extra_params.get("allowed_values")
    return random.choice(allowed_values)


def mask_first_name(account_number, length, extra_params):
    return random.choice(first_names)


def mask_last_name(account_number, length, extra_params):
    return random.choice(last_names)


def mask_any_name(account_number, length, extra_params):
    separator = extra_params.get("separator", " ")
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    return f"{first_name}{separator}{last_name}"


def mask_org_name(account_number, length, extra_params):
    separator = extra_params.get("separator", " ")
    first_name = random.choice(org_names)
    last_name = random.choice(org_structure)
    return f"{first_name}{separator}{last_name}"


def mask_acct(account_number, length, extra_params):
    if len(account_number) == length:
        return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
    else:
        return account_number


def mask_sin(account_number, length, extra_params):
    return "".join(random.choices(string.digits, k=length))


def mask_default(account_number, length, extra_params):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


mask_functions = {
    "GENDER": mask_gender,
    "FIRST_NAME": mask_first_name,
    "LAST_NAME": mask_last_name,
    "ANY_NAME": mask_any_name,
    "ORG_NAME": mask_org_name,
    "ACCT": mask_acct,
    "SIN": mask_sin,
}

columns_to_mask = {
    "ACCT": ("VARCHAR", 10, None),
    "GENDER": ("VARCHAR", 1, {"allowed_values": ["F", "M"]}),
    "ID1": ("INTEGER", 4, None),
    "ID2": ("INTEGER", None, None),
    "DECIMAL_COLUMN": ("DECIMAL", (5, 4), None),
    "DATE_COLUMN": ("DATE", None, None),
    "FIRST_NAME": ("VARCHAR", 8, None),
    "LAST_NAME": ("VARCHAR", 8, None),
    "ANY_NAME": ("VARCHAR", 16, {"separator": " "}),
    "ORG_NAME": ("VARCHAR", 206, {"separator": " "}),
    "FULL_NAME": ("VARCHAR", 45, None),
    "CAL": ("VARCHAR", 45, None),
    "SIN": ("VARCHAR", 5, None),
    "NARROW": ("VARCHAR", 4, None),
}
