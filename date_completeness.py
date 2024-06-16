def calculate_completeness(data, d):
    """
    Calculates completeness as (number of surveys on day d)/18 (the
    maximum number of surveys per day.)
    """
    num_on_day_d = len(data[data['Date'] == d])
    return num_on_day_d / 18