def bonus(score, target):
    x = max(0,(((score-target)/target)*5))
    result = min(5,x)
    return result

print(bonus(450, 300)) #Output: 2.5
