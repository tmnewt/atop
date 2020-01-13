class PayoffDiagram:
    '''Build payoff diagram object.
    
    Given a set of assets (a strategy), calculates the payoff diagram.
    Great for visualizing option strategies.'''
    def __init__(self, asset_list):
        self.asset_list = asset_list

        self.asset_payoffs = self.calc_asset_payoffs()
        self.strategy_payoffs = self.calc_strategy_payoffs()

    def calc_asset_payoffs(self):
        '''Returns payoffs for each asset.'''
        return NotImplemented

    def calc_strategy_payoffs(self):
        '''Returns payoffs for the entire strategy'''
        return NotImplemented
        