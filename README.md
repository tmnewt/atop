# atop: All Things Options

repo will host and document anything option related. 


## Whatcha got?:
Currently supports single period binomial pricing method for both calls and puts. Pass in the current underlying price, the strike price, the up value, the down value, and a risk-free rate and get back the option's price, as well as additional option data such as risk-neutral probabilites,hedge-ratio, etc. Can also override the state payoff values (very useful in multi-period binomial pricing)

## How to get running?
atop is not set up for pip or any other package manager, currently. Best to fork instead and run the file `test_of_binomialoption.py`. And then run the Multperiod notebook. But if just want to see some results you can see the static version of the [multperiod notebook](https://github.com/tmnewt/atop/blob/master/Notebooks/MultPeriod%20Notebook.ipynb).

## What are you up to now?

Right now I'm building out a platform that can 'populate' an arbitrary set of nodes. The first stage is to generate a standard tree of nodes given today's underlying value, volatility, and a set of periods describing a length of maturity, T. That's nothing special. The next stage stage is to experiment with the node structure. In this way I'll be able to mimic the payoff structures of option-like assets. Stage 3 is, I guess, back-testing.

## Long-term goal:
Build out a nice framework to price option-like assets. Also provide a variety of tools for solving any type of option problem. Create guides for using the code.

Long story short, there are a ton of things that need to get done. I'm just chipping away at what I can.