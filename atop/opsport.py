from atop.blackscholes.bsmnode import BsmNode

class OptionPortfolio:
    '''Main entry point for users?'''
    
    def __init__(self):
        self.portfolio = []

    def add_asset(self, asset):
        self.portfolio.append(asset)
        

    def remove_asset(self, asset):
        self.portfolio.remove(asset)

    

    