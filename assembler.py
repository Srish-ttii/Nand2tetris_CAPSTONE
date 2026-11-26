import os
import sys

BASE_SYMBOLS = {
    "R0": 0, "R1": 1, "R2": 2, "R3": 3, "R4": 4,
    "R5": 5, "R6": 6, "R7": 7, "R8": 8, "R9": 9,
    "R10": 10, "R11": 11, "R12": 12, "R13": 13, "R14": 14, "R15": 15,
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576
}

COMP_CODES = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101"
}

DEST_CODES = {
    "": "000", "M": "001", "D": "010", "MD": "011", "DM": "011",
    "A": "100", "AM": "101", "MA": "101", "AD": "110", "DA": "110",
    "AMD": "111", "ADM": "111"
}

JUMP_CODES = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"
}


def run_assembler(input_file):
    with open(input_file, "r") as f:
        all_lines = f.readlines()

    sym_table = dict(BASE_SYMBOLS)
    label_dict = {}
    var_dict = {}
    code_lines = []
    pc = 0

    # First reading: remove comments and blank lines, and store labels
    for line in all_lines:
        if "//" in line:
            line = line.split("//")[0]
        line = line.strip()
        if not line:
            continue

        if line.startswith("(") and line.endswith(")"):
            lbl = line[1:-1]
            sym_table[lbl] = pc
            label_dict[lbl] = pc
        else:
            code_lines.append(line)
            pc += 1

    # Second reading: translate every line into 16 bits
    next_var_addr = 16
    binary_out = []

    for cmd in code_lines:
        if cmd.startswith("@"):
            item = cmd[1:]
            if item.isdigit():
                num = int(item)
            else:
                if item not in sym_table:
                    sym_table[item] = next_var_addr
                    var_dict[item] = next_var_addr
                    next_var_addr += 1
                num = sym_table[item]
            binary_out.append(format(num, "016b"))
        else:
            d_field = ""
            c_field = cmd
            j_field = ""
            if "=" in c_field:
                d_field, c_field = c_field.split("=", 1)
            if ";" in c_field:
                c_field, j_field = c_field.split(";", 1)
            bit_str = "111" + COMP_CODES[c_field] + DEST_CODES[d_field] + JUMP_CODES[j_field]
            binary_out.append(bit_str)

    hack_file = os.path.splitext(input_file)[0] + ".hack"
    with open(hack_file, "w") as out_f:
        for b in binary_out:
            out_f.write(b + "\n")

    # Extra feature for K = 27 (27 mod 3 = 0):
    # Save all labels and variables with their addresses in symbols.txt
    symbols_path = os.path.join(os.path.dirname(os.path.abspath(input_file)), "symbols.txt")
    with open(symbols_path, "w") as s_f:
        s_f.write("Labels:\n")
        for k, v in label_dict.items():
            s_f.write(f"{k} = {v}\n")
        s_f.write("\nVariables:\n")
        for k, v in var_dict.items():
            s_f.write(f"{k} = {v}\n")

    print(f"Assembled {hack_file} and wrote {symbols_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 assembler.py <filename.asm>")
        sys.exit(1)
    run_assembler(sys.argv[1])
