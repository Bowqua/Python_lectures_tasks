def long_division(dividend, divider):
    quotient = dividend // divider
    lines = [f"{str(dividend)}|{divider}"]

    if dividend < divider:
        lines.append(f"{str(dividend)}|{str(quotient)}")
        return "\n".join(lines)

    index = 0
    part = int(str(dividend)[index])
    while part < divider:
        index += 1
        part = part * 10 + int(str(dividend)[index])

    first_part_len = index + 1
    first_substract = (part // divider) * divider
    left = str(first_substract).rjust(first_part_len)
    lines.append(left.ljust(len(str(dividend))) + "|" + str(quotient))
    part -= first_substract

    printed = False
    for i in range(index + 1, len(str(dividend))):
        part = part * 10 + int(str(dividend)[i])
        part_string = str(part)
        if part < divider:
            if i == len(str(dividend)) - 1:
                lines.append(" " * (len(str(dividend)) - len(part_string)) + part_string)
            continue

        sub = (part // divider) * divider
        sub_string = str(sub)
        offset = i - len(part_string) + 1

        lines.append(f"{part_string.rjust(offset + len(part_string))}")
        lines.append(f"{sub_string.rjust(offset + len(sub_string))}")
        part -= sub
        printed = True

    if printed: lines.append(" " * (len(str(dividend)) - len(str(part))) + str(part))
    else: pass
    return "\n".join(lines)

print(long_division(12345, 25))
