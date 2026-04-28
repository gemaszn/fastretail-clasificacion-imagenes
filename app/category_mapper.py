CATEGORY_RULES = {
    "Ropa inferior": [
        "pants", "jeans", "trousers", "shorts", "skirt"
    ],
    "Calzado": [
        "shoe", "sneaker", "footwear", "boot", "sandal", "heel"
    ],
    "Bolsos y mochilas": [
        "bag", "backpack", "handbag", "purse", "luggage"
    ],
    "Accesorios": [
        "watch", "hat", "cap", "belt", "sunglasses", "glasses",
        "jewelry", "necklace", "bracelet", "ring"
    ],
    "Ropa superior": [
        "shirt", "t-shirt", "top", "blouse", "sweater", "hoodie",
        "jacket", "coat"
    ],
}


def assign_category(labels):
    """
    Recibe las etiquetas de Amazon Rekognition y devuelve
    una categoría de negocio para FastRetail.
    """

    best_category = "Sin categoría"
    best_confidence = 0

    for label in labels:
        label_name = label["Name"].lower()
        confidence = label["Confidence"]

        for category, keywords in CATEGORY_RULES.items():
            for keyword in keywords:
                if keyword in label_name and confidence > best_confidence:
                    best_category = category
                    best_confidence = confidence

    return best_category, best_confidence