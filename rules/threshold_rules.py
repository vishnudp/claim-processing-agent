def validate_threshold(claim):

    amount = claim["claim_amount"]

    return {

        "amount": amount,

        "hitl": amount > 10000
    }