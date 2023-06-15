import pandas as pd
import random
import sys
import os
from datetime import datetime, timedelta
from masking_functions import (
    mask_functions,
    mask_default,
    first_names,
    last_names,
    columns_to_mask,
)


class DataMasker:
    def __init__(self):
        self.first_names = first_names
        self.last_names = last_names

    def random_decimal(self, precision, scale):
        integer_part = random.randint(0, 10 ** (precision - scale) - 1)
        decimal_part = random.randint(10 ** (scale - 1), 10**scale - 1)
        return float(f"{integer_part}.{decimal_part}")

    def random_date(self, start_date="1900-01-01", end_date="2099-12-31"):
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        random_date = start + timedelta(days=random.randint(0, (end - start).days))
        return random_date.strftime("%Y-%m-%d")

    def mask_account_number(
        self, column_name, account_number, data_type, length, extra_params=None
    ):
        if extra_params is None:
            extra_params = {}

        column_name = column_name.upper()

        if data_type.upper() in ["CHAR", "VARCHAR"]:
            account_number = str(account_number)
            mask_function = mask_functions.get(column_name, mask_default)
            masked_number = mask_function(account_number, length, extra_params)
        elif data_type.upper() == "DECIMAL":
            precision, scale = length
            masked_number = self.random_decimal(precision, scale)
        elif data_type.upper() == "DATE":
            masked_number = self.random_date()
        elif data_type.upper() == "INTEGER":
            if length is not None:
                min_value = 10 ** (length - 1)
                max_value = 10**length - 1
            else:
                min_value = extra_params.get("min_value", 0)
                max_value = extra_params.get("max_value", 2**31 - 1)
            masked_number = random.randint(min_value, max_value)
        else:
            masked_number = account_number
        return masked_number

    def mask_csv(self, input_file, output_file, columns_to_mask, ignore_lines="NO"):
        with open(input_file, "r") as f:
            lines = f.readlines()

        if ignore_lines == "NF":
            first_line = lines[0]
            lines = lines[1:]
        elif ignore_lines == "NL":
            last_line = lines[-1]
            lines = lines[:-1]
        elif ignore_lines == "NFL":
            first_line = lines[0]
            last_line = lines[-1]
            lines = lines[1:-1]

        with open("temp.csv", "w") as f:
            f.writelines(lines)

        df = pd.read_csv("temp.csv", sep="|")

        for column_name, (data_type, length, extra_params) in columns_to_mask.items():
            if column_name != "FULL_NAME" and column_name in df.columns:
                print(f"Masking data in column: {column_name}")
                df[column_name] = df[column_name].apply(
                    lambda x: self.mask_account_number(
                        column_name, x, data_type, length, extra_params
                    )
                )

        if "FULL_NAME" in df.columns:
            df["FULL_NAME"] = df["FIRST_NAME"] + " " + df["LAST_NAME"]

        df.to_csv("temp.csv", index=False, sep="|")

        with open("temp.csv", "r") as f:
            lines = f.readlines()

        if ignore_lines == "NF":
            lines.insert(0, first_line)
        elif ignore_lines == "NL":
            lines.append(last_line)
        elif ignore_lines == "NFL":
            lines.insert(0, first_line)
            lines.append(last_line)

        with open(output_file, "w") as f:
            f.writelines(lines)

        os.remove("temp.csv")


if __name__ == "__main__":
    input_file = sys.argv[2]
    output_file = sys.argv[3]

    data_masker = DataMasker()
    data_masker.mask_csv(
        input_file, output_file, columns_to_mask, ignore_lines=sys.argv[1]
    )
