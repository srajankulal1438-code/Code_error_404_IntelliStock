def make_decision(predicted, stock):
    if predicted > stock:
        return f"Restock {int(predicted - stock + 10)} units immediately"
    elif stock > predicted * 2:
        return "Overstock detected – reduce ordering"
    else:
        return "Stock is optimal"