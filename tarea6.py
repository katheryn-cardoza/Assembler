def to_binary(value, num_bits=16):
    return format(value, f'0{num_bits}b')


symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576,
    "ITSR0": 17  # Se Agrega ITSR0 a la tabla de símbolos con la dirección indicada
}

dest_dict = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp_dict = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "!D": "0001101",
    "!A": "0110001",
    "-D": "0001111",
    "-A": "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",
    "M": "1110000",
    "!M": "1110001",
    "-M": "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

jump_dict = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111",
    "ITSR0": "000"  # Agregar la etiqueta ITSR0 al diccionario
}

next_available_address = [16]  # Asigna la variable next_available_address


def parse_A_instruction(instruction):
    global next_available_address
    if instruction.isdigit():
        # Aqui se utilizara un ancho de 16 bits
        return to_binary(int(instruction), 16)
    else:
        symbol = instruction[1:]
        if symbol not in symbol_table:
            symbol_table[symbol] = next_available_address
            next_available_address += 1
        # Aqui utilizara un ancho de 16 bits
        return to_binary(symbol_table[symbol], 16)


def parse_C_instruction(instruction):
    if "(" in instruction:  #Omite las etiquetas
        return None

    if "=" in instruction:
        dest, rest = instruction.split("=")
    else:
        dest = ""
        rest = instruction

    if ";" in rest:
        comp, jump = rest.split(";")
    else:
        comp = rest
        jump = ""

    if jump and jump.startswith('('):  # Verificar si es una etiqueta
        # Salto vacío
        return "111" + comp_dict["0"] + dest_dict.get(dest, "000") + jump_dict.get("", "000")
    elif jump:  # Si hay una parte de salto en la instrucción
        return "111" + comp_dict["0"] + dest_dict.get(dest, "000") + jump_dict.get(jump, "000")
    else:
        return "111" + comp_dict[comp] + dest_dict.get(dest, "000") + jump_dict.get(jump, "000")


def first_pass(lines):
    global next_available_address
    next_available_address = 16  # Asigna el valor a la variable next_available_address en 16
    address = 0
    for line in lines:
        line = line.strip()
        if line.startswith("//") or line == "":
            continue
        elif line.startswith("("):
            label = line[1:-1]
            symbol_table[label] = address
        else:
            address += 1


def assemble(asm_file, hack_file):
    with open(asm_file, "r") as f:
        lines = f.readlines()

    first_pass(lines)

    binary_lines = []
    for line in lines:
        line = line.strip()
        if line.startswith("//") or line == "":
            continue
        elif line.startswith("("):

            continue
        elif line.startswith("@"):
            binary_line = parse_A_instruction(line)
        else:
            binary_line = parse_C_instruction(line)

        if binary_line is not None:
            binary_lines.append(binary_line)
            print(binary_line)  # Este codigo binario imprime y crea los archivos.Hack

    with open(hack_file, "w") as f:
        for line in binary_lines:
            f.write(line + "\n")


if __name__ == "__main__":
    assemble("PongL.asm", "PongL.hack")
