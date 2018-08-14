"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
import random 


GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    "*** REPLACE THIS LINE ***"

    score, each = 0, 0
    pigout = False 

    for x in range(num_rolls):
        each = dice()
        if each == 1:
            pigout = True 
        score = score + each

    if pigout: 
        return 1
    else: 
        return score


    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2
    "*** REPLACE THIS LINE ***"

    if num_rolls == 0:
        return 1 + max(opponent_score // 10, opponent_score % 10)
    else:
        return roll_dice(num_rolls, dice)


    # END Question 2

def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    "*** REPLACE THIS LINE ***"

    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided


    # END Question 3

def is_swap(score0, score1):
    """Return True if ending a turn with SCORE0 and SCORE1 will result in a
    swap.

    Swaps occur when the last two digits of the first score are the reverse
    of the last two digits of the second score.
    """
    # BEGIN Question 4
    "*** REPLACE THIS LINE ***"

    if score0 >= 100:
        score0 = score0 - 100
    if score1 >= 100:
        score1 = score1 - 100

    return (score0 // 10 == score1 % 10) & (score0 % 10 == score1 // 10)


    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    # BEGIN Question 5
    "*** REPLACE THIS LINE ***"
    temp_for_swap = 0
    

    while (score0 < goal) & (score1 < goal):
        
        dice = select_dice(score0, score1)

        if who == 0:
            score0 += take_turn(strategy0(score0,score1), score1, dice)

        else: 
            score1 += take_turn(strategy1(score1,score0), score0, dice)
    

        if is_swap(score0, score1):
            temp_for_swap = score0
            score0 = score1
            score1 = temp_for_swap


        who = other(who)

    # END Question 5
    return score0, score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    # BEGIN Question 6
    "*** REPLACE THIS LINE ***"

    def average(*args):
        sum = 0
        for x in range(num_samples):
            sum += fn(*args)

        return sum / num_samples

    return average

    # END Question 6

def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7
    "*** REPLACE THIS LINE ***"

    number_of_dice = 1
    highest_average_turn_score = 0
    

    for x in range(1,11):
        average_turn_score = make_averaged(roll_dice, num_samples)(x,dice)
        if average_turn_score > highest_average_turn_score:
            highest_average_turn_score = average_turn_score
            number_of_dice = x

    return number_of_dice



    # END Question 7

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))    


    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    if 1 + max(opponent_score // 10, opponent_score % 10) >= margin:
        return 0
    
    return num_rolls 
    # END Question 8

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS if rolling 0 dice results in a harmful swap. It also
    rolls 0 dice if that gives at least MARGIN points and rolls NUM_ROLLS
    otherwise.
    """
    # BEGIN Question 9
    "*** REPLACE THIS LINE ***"
    rolling_zero = 1 + max(opponent_score // 10, opponent_score % 10)
    bacond_score = score + rolling_zero


    if bacond_score > GOAL_SCORE:
        return num_rolls


    if (bacond_score//10 == opponent_score%10) & (bacond_score%10 == opponent_score//10):
    # If the scores can be swapped when rolling zero dice,    
        if opponent_score > bacond_score:
            return 0 # Swap it when losing the game

        elif bacond_score > opponent_score:
            return num_rolls # Don't swap it when leading the game       

        else: # If the scores are tie by rolling zero dice,
              # Compare which one is greater between rolling_zero and margin.
            if rolling_zero > margin: 
                return 0
            else:
                return num_rolls

    else: # Otherwise, follow the bacon strategy.
        return bacon_strategy(score, opponent_score, margin, num_rolls)


    # END Question 9


def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***

    This strategy is based on Bacon Strategy with optimized number of dice and margin.
    When closed to the goal, it takes safe strategy not to be pigged out.
    If far behind, it becomes risk-taker.
    Also the system to take advantage of Swine Swap Rule and Hog Wild Rule is embedded.


    """
    # BEGIN Question 10
    "*** REPLACE THIS LINE ***"
    
    super_safety = 2
    safety = 4
    best_num = 6
    best_margin = 9
    risk = 8
    gap = 65


    rolling_zero = 1 + max(opponent_score // 10, opponent_score % 10)
    bacond_score = score + rolling_zero # The score when rolling zero dice.




    # Avoid pig-out when closed to the goal
    if score > 83:
        return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=super_safety)

    if score > 62:
        return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=safety)

    


    # Leading score -> as safe as possible
    if (score - opponent_score) > gap:
        return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=safety)

    # Losing score -> be a risk-taker
    if (opponent_score - score) > gap:
        return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=risk)
    



    # Take advantage of Swine Swap Rule
    if (bacond_score//10 == opponent_score%10) & (bacond_score%10 == opponent_score//10):
        if opponent_score > bacond_score:
            return 0
        return best_num
       


    # Leave the opponent with 4-sided dices
    if (bacond_score + opponent_score) % 7 == 0:
        return 0

    # When Hog-wilded, roll fewer dices.
    if (score + opponent_score) % 7 == 0:
        return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=safety)



    # Default Strategy
    return bacon_strategy(score, opponent_score,margin=best_margin,num_rolls=best_num)


    # END Question 10


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--final', action='store_true',
                        help='Display the final_strategy win rate against always_roll(5)')
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
    elif args.final:
        from hog_eval import final_win_rate
        win_rate = final_win_rate()
        print('Your final_strategy win rate is')
        print('    ', win_rate)
        print('(or {}%)'.format(round(win_rate * 100, 2)))
