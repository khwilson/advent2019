"""
This AOC requires a lot of simultating a simple opcode
language. This is where we keep track of that code.
"""
import copy
from typing import List


def read_ops(ops_str: str) -> List[int]:
  return [int(op) for op in ops_str.strip().split(',')]


def _mode_switch(ops: List[int], val: int, mode: int, relative_base: int):
  if mode == 0:
    return ops[val]
  elif mode == 1:
    return val
  elif mode == 2:
    return ops[val + relative_base]
  else:
    raise ValueError('Invalid mode {}'.format(mode))
   

class MemoryWrapper:
  def __init__(self, ops):
    self.ops = ops

  def __getitem__(self, i):
    while len(self.ops) <= i:
      self.ops.append(0)
    return self.ops[i]

  def __setitem__(self, i, x):
    while len(self.ops) <= i:
      self.ops.append(0)
    self.ops[i] = x
  
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return repr(self.ops)


def simulate(
    ops: List[int],
    inplace: bool = False,
    inputs: List[int] = None,
    output_func = lambda val: print('Printing output:', val),
    starting_pid: int = 0,
    starting_relative_base: int = 0
  ) -> bool:
  """
  Run the IntCode simulator in AOC 2019.
  
  Basic instructions:
    * instructions are formatted as [ABCDE, *args]
    * DE is an opcode, C is the mode for args[0], B the mode for args[1], A the mode for args[2]
    * mode is either 0 or 1:
      - 0: Interpret the argument as a pointer to a place in ops
      - 1: Interpret the argument as a literal
    * pid starts at 9 and then 
    * opcodes are as folllows:
      - 1: Add args[0] + arg[1] and store in args[2]
      - 2: Add args[0] * arg[1] and store in args[2]
      - 3: Request input from the user; store in args[1]
      - 4: Call output_func with the value of args[1]
      - 5: jump to args[1] if args[0] is nonzero
      - 6: jump to args[1] if args[0] is zero
      - 7: jump to args[2] if args[0] < args[1]
      - 8: jump to args[2] if args[0] == args[1]
      - 99: Halt
    * pid is increased by len(args) + 1 after running the instruction,
      unless the instructino was a jump instruction, in which case, no
      auto incrementing occurs.
  
  Args:
    ops: The program to run
    inplace: Should the simulator run on the passed ops or on a copy?
    inputs: The input queue. If empty and input is requested, asks the user
    output_func: A function that takes a single value (an emission from the
      program (opcode 4)). If the function returns a Truthy value, then
      this function will immediately return the current pid.
    starting_pid: What position (we call pid) to start the program at. Useful
      for restarting program after emission.
  
  Return:
    The current PID if output_func returns Truthy. Else, -1 if opcode 99 is reached.
  """
  if not inplace:
    ops = copy.copy(ops)
    
  inputs = deque(inputs)
  
  ops = MemoryWrapper(ops)

  pid = starting_pid
  relative_base = starting_relative_base
  while True:
    full_opcode = ops[pid]
    opcode = full_opcode % 100
    modes = full_opcode // 100
    mode1 = modes % 10
    mode2 = (modes // 10) % 10
    mode3 = (modes // 100) % 10

    if opcode == 1:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
      val3 = ops[pid + 3]

      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)

      ops[val3 + (relative_base if mode3 == 2 else 0)] = add1 + add2
      pid += 4

    elif opcode == 2:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
      val3 = ops[pid + 3]

      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)

      ops[val3 + (relative_base if mode3 == 2 else 0)] = add1 * add2
      pid += 4

    elif opcode == 3:
      if inputs:
        val = inputs.popleft()
      else:
        val = int(input('I request input:'))
      ops[ops[pid + 1] + (relative_base if mode1 == 2 else 0)] = val
      pid += 2

    elif opcode == 4:
      val = ops[pid + 1]
      add = _mode_switch(ops, val, mode1, relative_base)
      
      pid += 2
      if output_func(add):
        return pid
    
    elif opcode == 5:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
        
      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)
 
      if add1:
        pid = add2
      else:
        pid += 3
  
    elif opcode == 6:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
        
      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)
 
      if not add1:
        pid = add2
      else:
        pid += 3

    elif opcode == 7:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
      
      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)
      base = relative_base if mode3 == 2 else 0

      ops[ops[pid + 3] + base] = 1 if add1 < add2 else 0
      pid += 4
    
    elif opcode == 8:
      val1 = ops[pid + 1]
      val2 = ops[pid + 2]
      
      add1 = _mode_switch(ops, val1, mode1, relative_base)
      add2 = _mode_switch(ops, val2, mode2, relative_base)
      base = relative_base if mode3 == 2 else 0

      ops[ops[pid + 3] + base] = 1 if add1 == add2 else 0
      pid += 4

    elif opcode == 9:
      val = ops[pid + 1]
      add = _mode_switch(ops, val, mode1, relative_base)
      relative_base += add
      pid += 2

    elif opcode == 99:
      return -1

    else:
      raise ValueError("Invalid code: {}".format(ops[pid]))
