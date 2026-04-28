def evaluate_predictions(test_cases):
    """
    Recibe casos de prueba con categoría real y predicha.
    
    Formato:
    [
        {"real": "Calzado", "predicted": "Calzado"},
        {"real": "Accesorios", "predicted": "Sin categoría"}
    ]
    """

    total = len(test_cases)

    if total == 0:
        return {
            "total": 0,
            "correct": 0,
            "accuracy": 0
        }

    correct = 0

    for case in test_cases:
        if case["real"] == case["predicted"]:
            correct += 1

    accuracy = correct / total

    return {
        "total": total,
        "correct": correct,
        "accuracy": round(accuracy * 100, 2)
    }