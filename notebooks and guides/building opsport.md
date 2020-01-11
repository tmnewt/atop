# Building the OpsPort class

This is primarily for development purposes and showing how the values for option strategies are calculated and plotted. 

There are 4 possible assets (the `call option`, the `put option`, the `underlying`, and a `zero-coupon risk-free`) each which have 2 different positions (`Long` or `Short`). 



The call and put options can be described as having 2 necessary input components: 1) the `strike` and 2) the premium `price` of the option. We can extend these characteristics to the underlying asset whose payoff value follows a linear 1:1 relationship (we ignore exotic underlying assets)  so that it has also has a `strike` (technically the price paid for it) plus a premium `price` (typically a broker's fee). Lastly the risk-free asset (traditionally a risk-free note) has only 1 input value, the `risk-free` rate.  

Overall the assets and their inputs can be described as: 

* **Call Long <---  (`strike`, `price`)**
* **Call Short <--- (`strike`, `price`)**
* **Put Long  <---    (`strike`, `price`)**
* **Put Short <--- (`strike`, `price`)**
* **Underlying Long <--- (`strike`, `price`)**
* **Underlying Short<--- (`strike`, `price`)**
* **zero_coupon risk-free Long <--- (`risk_free_rate`)**
* **zero_coupon risk-free Short <--- (`risk_free_rate`)**

These assets, the features inherent to them, and the possible positions taken describe market completeness.

Every asset can be described in terms of either gross or net payoff. We mostly focus on net payoff as it describes profits. Taking every possible payoff of an asset for a given underlying value and plotting the resulting set of payoffs on a graph allows us visualize the payoff structure of the asset. Extending this, by combining the payoff sets of various assets allows for visualizing the payoff structure of a portfolio of different options on the same underlying asset.

The following payoff descriptions are intended to translate into logical code. These logical descriptions follow from the standard understanding of the asset's structure:

## When the asset is a Call:
* If a Long Call: at all underlying values less than or equal to the strike the net payoff is the price paid (that is, a negative profit). Else, at all underlying values greater than the strike the net payoff is underlying minus strike minus price paid.

* If a Short Call: at all underlying values less than or equal to the strike the net payoff is the price earned for selling (a.k.a the premium earned for writing the call option). Else, at all underlying values greater than the strike the net payoff is the price earned for selling minus underlying minus strike

Reiterated in *PSEUDO* python code (again, not the actual code!) the process for finding the net payoff values (to be used in plotting the diagram) of a call option can be described in two functions:
```Python
def net_long_call_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:     
            payoff = 0 - price
        else:       
            payoff = (underlying - strike) - price  
        payoff_list.append(payoff)
    return payoff_list


def net_short_call_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = price
        else:
            payoff = price - (underlying - strike)
        payoff_list.append(payoff)
    return payoff_list
```
> By the way, note this method uses a bunch of values to build the plot. That's unnecessary. Though this approach works, there are more efficient ways which produce the same results! For instance, the internal logic can be condensed to using a max function without loss of results: consider for a long call the payoffs can be found using `max(-price, underlying-strike-price)`. That's only 1 example of efficiencies to be gained... but thats not the primary concern.

## When the asset is a Put:

* If a Long Put: at all underlying values less than or equal to the strike the net payoff is the strike minus underlying minus price. Else, at all underlying values greater than the strike the net payoff is the price paid (that is, a negative profit).

* If a Short Put: at all underlying values less than or equal to the strike the net payoff is the price earned for selling minus the strike minus underlying. Else, at all underlying values greater than the strike the net payoff is the `price earned for selling (a.k.a the premium earned for writing the put option).

Reiterated in *PSEUDO* python code the process for finding the net payoff values (to be used in plotting the diagram) of a put option can be described in two functions:

```Python
def net_long_put_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = (strike - underlying) - price
        else:
            payoff = -price
        payoff_list.append(payoff)
    return payoff_list


def net_short_put_payoffs(strike, price):
    payoff_list = []
    for underlying in range(101):
        if underlying <= strike:
            payoff = price - (strike - underlying)
        else:
            payoff = price
        payoff_list.append(payoff)
    return payoff_list
```

## When the asset is the underlying asset itself and is 'stock' like:
* If Long Stock: at all underlying values the net payoff is the underlying minus the purchase price minus any broker fees.
* If Short Stock: at all underlying values the net payoff is the cash earned for shorting minus the underlying price minus any broker fees

```Python
def net_stock_long_payoffs(buy_price, broker_fee):
    payoff_list = []
    for underlying in range(101):
        payoff = underlying - buy_price - broker_fee
        payoff_list.append(payoff)
    return payoff_list

def net_stock_short_payoffs(short_price, broker_fee):
    payoff_list = []
    for underlying in range(101):
        payoff = short_price - underlying - broker_fee
        payoff_list.append(payoff)
    return payoff_list
```

## When the asset is a zero-coupon risk-free note

