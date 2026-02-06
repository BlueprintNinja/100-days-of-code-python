import art
print(art.logo)
print("BID SECRETLY. STRIKE BOLDLY.")

bids = {}
new_bids = ""
# TODO-1: Ask the user for input
while new_bids != "n":
    name = input("What is your name? ")
    bid = input("How much would you like to bid?")

    # TODO-2: Save data into dictionary {name: price}

    bids[name] = int(bid)
    # TODO-3: Whether if new bids need to be added
    new_bids = input("Would you like to add a new bid? (y/n) ")


# TODO-4: Compare bids in dictionary
winning_amount = 0
winning_bid = ""
for key, value in bids.items():
    if value > winning_amount:
        winning_amount = value
        winning_bid = key

print(f"{winning_bid} won the auction for {winning_amount} bids")
