# atop: All Things Options

repo will host and document anything option related. 


## What da got?:
Currently supports single period binomial pricing method for both calls and puts. Pass in the current underlying price, the strike price, the up value, the down value, and a risk-free rate and get back the option's price, as well as additional option data such as risk-neutral probabilites,hedge-ratio, etc. Can also override the state payoff values (very useful in multi-period binomial pricing)

## What are you up to now?

Right now working on showcasing how to chain single-period binomial option pricing method together to solve multi-period option pricing. 

## Long-term goal:
Build out a nice framework to price option-like assets. Also provide a variety of tools for solving any type of option problem.
