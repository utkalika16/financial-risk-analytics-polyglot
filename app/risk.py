from database import get_mongo


def calculate_risk(amount, frequency):
    score = 0
    indicators = []

    if amount > 50000:
        score += 50
        indicators.append("High transaction amount")

    if frequency > 10:
        score += 30
        indicators.append("High transaction frequency")

    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, indicators


def save_risk(customer_id, account_id, score, level, indicators):
    collection = get_mongo()

    collection.insert_one({
        "customer_id": customer_id,
        "account_id": account_id,
        "risk_score": score,
        "risk_level": level,
        "risk_indicators": indicators
    })

    return "Risk result saved"