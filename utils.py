def calculate_risk(predicted, stock):
    if stock == 0:
        return "HIGH"

    ratio = predicted / stock

    if ratio > 1:
        return "HIGH"
    elif ratio > 0.7:
        return "MEDIUM"
    else:
        return "LOW"