import os

INPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'inputs/submarine_report')


def bin_to_decimal(bin_num):
    """Converts the binary number to a decimal number.

    Args:
        bin_num (str): Binary number.

    Returns:
        int: Decimal number conversion.
    """
    return int(bin_num, 2)


def get_n_bits(report):
    """Gets the number of bits that have each line from the input report.

    Args:
        report (list): Input report that contains a binary number for each line.

    Returns:
        int: How many bits have each binary number.
    """
    return len(report[0])-1


def get_subreport_zeros_and_ones(subreport, n_bits):
    """Gets the number of zeros and ones that have each column within the submarine report.

    Args:
        subreport (): Subset to count from.
        n_bits (int): How many bits have each binary number.
    Returns:
        tuple: Zeros and ones that each column has.
    """
    zeros = [0]*n_bits
    ones = [0]*n_bits

    for bits in subreport:
        for i in range(n_bits):
            if bits[i] == '1':
                ones[i] += 1
            elif bits[i] == '0':
                zeros[i] += 1

    return zeros, ones


def get_subreport(binary_list, least_most_common_bit, bit_position):
    """Gets the report subset that has the least/most common bit within the specified bit position.

    Args:
        binary_list ():
        least_most_common_bit ():
        bit_position ():
    Returns:
        subreport (list): Subset that fulfill the constraint.
    """
    subreport = []

    for bits in binary_list:
        if bits[bit_position] == least_most_common_bit:
            subreport.append(bits)

    return subreport


def gamma_rate(zeros, ones, i):
    return '0' if zeros[i] > ones[i] else '1'


def epsilon_rate(zeros, ones, i):
    return '0' if zeros[i] < ones[i] else '1'


def get_rate(n_bits, zeros, ones, rate):
    rate_list = [' ']*n_bits

    for i in range(n_bits):
        rate_list[i] = rate(zeros, ones, i)

    return bin_to_decimal(''.join(rate_list))


def bit_criteria_o2(zeros, ones, i):
    return '0' if zeros[i] > ones[i] else '1'


def bit_criteria_co2(zeros, ones, i):
    return '1' if ones[i] < zeros[i] else '0'


def get_rating_using_criteria(n_bits, sub_diagnostic_report, bit_criteria):
    zeros, ones = get_subreport_zeros_and_ones(sub_diagnostic_report, n_bits)

    while True:

        for i in range(n_bits):
            least_most_common_bit = bit_criteria(zeros, ones, i)
            sub_diagnostic_report = get_subreport(sub_diagnostic_report, least_most_common_bit, i)
            zeros, ones = get_subreport_zeros_and_ones(sub_diagnostic_report, n_bits)

            if len(sub_diagnostic_report) == 1:
                return bin_to_decimal(''.join(sub_diagnostic_report[0].replace('\n', '')))


def main():
    input_file = open(INPUT_PATH, 'r')
    diagnostic_report = input_file.readlines()
    input_file.close()
    n_bits = get_n_bits(diagnostic_report)
    zeros, ones = get_subreport_zeros_and_ones(diagnostic_report, n_bits)

    gamma_rate_value = get_rate(n_bits, zeros, ones, gamma_rate)
    epsilon_rate_value = get_rate(n_bits, zeros, ones, epsilon_rate)

    print('power_consumption: gamma_rate*epsilon_rate='
          f"{gamma_rate_value}*{epsilon_rate_value}"
          f"={gamma_rate_value*epsilon_rate_value}")

    sub_diagnostic_report_o2 = diagnostic_report.copy()
    sub_diagnostic_report_co2 = diagnostic_report.copy()

    o2_gen_rating = get_rating_using_criteria(n_bits, sub_diagnostic_report_o2, bit_criteria_o2)
    co2_scrubber_rating = get_rating_using_criteria(n_bits, sub_diagnostic_report_co2, bit_criteria_co2)

    print('life support rating: o2_gen_rating*co2_scrubber_rating='
          f"{o2_gen_rating}*{co2_scrubber_rating}={o2_gen_rating*co2_scrubber_rating}")


if __name__ == "__main__":
    main()
