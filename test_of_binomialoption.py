from atop.options.calloption import CallOption 
from atop.options.putoption import PutOption

bc = CallOption(100, 110, 120, 90.25, 0.0513)
bc.print_calc_values()

bp = PutOption(100, 110, 120, 90.25, 0.0513)
bp.print_calc_values()

override_call_test = CallOption(100, 110, 110, 95, 0.05, 6.984, 0)
override_call_test.print_calc_values(hide_hegde_ratio=True)