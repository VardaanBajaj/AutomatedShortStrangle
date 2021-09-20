# AutomatedShortStrangle
This repository automates the implementation of weekly banknifty option trading strategy mentioned here: https://www.youtube.com/watch?v=_t-vfmCG3Mo

# Constraints
Following are the constraints:

0. Find premiums with values close to 115 on both Ce and Pe and create strangle
1. Exit the trade as soon as profit >= 4000 before expiry morning, else exit on expiry morning
2. If difference between premiums is more than 50% during the day, square off position with lower premium and
    start a new position with premimum which is 80%-95% of thr higher premium
3. If difference between premiums is more than 20% when markets are about to close, square off position with lower premium
    and start a new position with premimum which is 80%-95% of thr higher premium
4. If strike price of CE <= strike price of PE, exit the trade

Feel free to try it out and raise a PR in case any bugs are found.
