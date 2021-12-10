import subprocess
import os
import re

day3_path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'src/day3.py')
data_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'data')
solutions_path = os.path.join(data_path, 'solutions.yaml')  # create method that loads the required solutions to check


def test_check_day3_output():
    """Checks that the day 3 problem is solved correctly.

    It waits that day3 solution prints following this format:

        r'\D+=\d+\*\d+=\d+'
        r'\D+o2_gen_rating\*co2_scrubber_rating=\d+\*\d+=\d+'

    for example:
        power consumption: gamma_rate*epsilon_rate=2*3=6
        life support rating: o2_gen_rating*co2_scrubber_rating=4*13=52

    In order to do that, the solution is run and it checks if:
        - No errors have occurred
        - Power consumption has the expected value
        - Life support rating has the expected value
    """
    p = subprocess.Popen(f"python3 {day3_path}", shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    result = out.decode("utf-8").split('\n')
    pc_results = re.findall(r'\d+', result[0])
    lsr_results = re.findall(r'\d+', result[1])[-3:]

    assert err is None
    assert pc_results[0] == '394',      'Gamma rate is not correct.'
    assert pc_results[1] == '3701',     'Epsilon rate is not correct.'
    assert pc_results[2] == '1458194',  'Power consumption is not correct.'
    assert lsr_results[0] == '789',     'Oxygen generator rating is not correct.'
    assert lsr_results[1] == '3586',    'CO2 scrubber rating is not correct.'
    assert lsr_results[2] == '2829354', 'Life support rating is not correct.'
