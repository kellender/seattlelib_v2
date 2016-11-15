#this unit test checks the functionality of the sin function 


from repyportability import *
add_dy_support(locals())
dy_import_module_symbols("math.r2py")


import math


# Checks values from 0 to +- 2 pi in intervals of pi/4
count = 0
while(count != 9):
  if(math_sin((math_pi*count) / 4) != math.sin((math_pi*count) / 4)):
    print ("[FAIL]: graphing the positive domain of sin was a failure")
  if(math_sin((-math_pi*count) / 4) != math.sin((-math_pi*count) / 4)):
    print ("[FAIL]: graphing the negative domain of sin was a failure")
  count += 1