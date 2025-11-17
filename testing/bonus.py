def bonus(score, target):
    x = max(0,(((score-target)/target)*5))
    result = min(5,x)
    return result

print(bonus(450, 300)) #Output: 2.5


# TODO (TASK 7) - Rewrite this function so that it calculates the player's gold reward *recursively*.
#   The recursion should progress through each step of the reward process (base reward, bonus for overkill, etc.)
#   by calling itself with updated parameters or stages instead of using loops.
#   Each recursive call should handle a single part of the reward logic, and the final base case should
#   return the total combined reward once all calculations are complete.
#   The function must include:
#     - Base gold depending on blind type (SMALL=4, BIG=8, BOSS=10)
#     - Recursive calculation of the overkill bonus (based on how much score exceeds the target)
#     - A clear base case to stop recursion when all parts are done
#   Avoid any for/while loops — recursion alone must handle the repetition.
def calculate_gold_rewards(self, playerInfo, stage=0):
    print("Entered calculate_gold_reward")
    print(playerInfo.score)
    print(playerInfo.roundScore)
    print(stage)
    target_score = playerInfo.score  # SMALL=300, BIG=600, BOSS=900
    player_score = playerInfo.roundScore  # Total score after player finishes a round
    base_reward = 0
    #Stage 1: Base Reward
    #Stage 2: Bonus
    #Base Case 3: Total

    #Bonus
    if player_score > target_score:
        return bonus(player_score, target_score) + calculate_gold_rewards(self, playerInfo=target_score, stage=stage)
    else:
        # Base Rewards
        if stage == 0:  # [0] = SMALL
            base_reward = 4
        if stage == 1:  # [1] = BIG
            base_reward = 8
        if stage == 2:  # [2] = BOSS
            base_reward = 10
        return base_reward
