# This method uses the "Point Count Periods" data
MAX_NUM_SURVEYS = 18

def calculate_completeness(data, d):
    """
    Calculates completeness as (number of surveys on day d)/18 (the
    maximum number of surveys per day.)

    Parameters:
        data: the dataset with all the surveys.
        d: the date for which to find completeness.
    """
    num_on_day_d = len(data[data['Date'] == d])
    return num_on_day_d / MAX_NUM_SURVEYS