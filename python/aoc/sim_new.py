"""
This AOC requires a lot of simultating a simple opcode
language. This is where we keep track of that code.
"""
import copy
from collections import deque
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


def _get_args(ops: List[int], nargs: int, full_opcode: int, pid: int, relative_base: int):
  modes = full_opcode // 100
  mode1 = modes % 10
  mode2 = (modes // 10) % 10
  mode3 = (modes // 100) % 10
  
  adds = []
  for narg, mode in zip(range(1, nargs + 1), [mode1, mode2, mode3]):
    val = ops[pid + narg]
    add = _mode_switch(ops, val, mode, relative_base)
    adds.append(add)
  return adds if len(adds) > 1 else adds[0]


def _store(
    ops: List[int],
    val: int,
    narg: int,
    full_opcode: int,
    pid: int,
    relative_base: int
  ) -> None:
  """
  Store `val` in the appropriate location described at
  `ops[pid + narg]` in accordance with the mode at `ops[pid]`.
  """
  modes = full_opcode // 100
  for _ in range(1, narg):
    modes //= 10
  mode = modes % 10
  pos = ops[pid + narg] + (relative_base if mode == 2 else 0)
  ops[pos] = val
   

class MemoryWrapper:
  """
  Imitate infinite memory. Pass a list and extend the list to a valid
  length based on reads and writes.
  """

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


class InputWrapper:
  def __init__(self, inputs):
    self.inputs = deque(inputs)

  def get(self):
    return self.inputs.popleft()

  def put(self, x):
    return self.inputs.append(x)

  def clear(self):
    self.inputs = deque([])
  
  def __bool__(self):
    return bool(self.inputs)


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
    * mode is either 0, 1, or 2:
      - 0: Interpret the argument as a pointer to a place in ops
      - 1: Interpret the argument as a literal
      - 2: Interpret the argument as a relative pointer to a place in ops;
           The pointer is relative to a global offset, which can be modified
           using opcode 9
    * pid and the global offset start at 0 unless specified in the args of this function
    * opcodes are as folllows (here args[i] means 'interpret according to above mode')
      - 1: Store args[0] + arg[1] in args[2]
      - 2: Store args[0] * arg[1] in args[2]
      - 3: Request input from the user; store in args[1]
      - 4: Call output_func with the value of args[1]
      - 5: Jump to args[1] if args[0] is nonzero
      - 6: Jump to args[1] if args[0] is zero
      - 7: Store 1 in args[2] if args[0] < args[1] else store 0
      - 8: Store 1 in args[2] if args[0] == args[1] else store 0
      - 9: Add args[1] to the global offset
      - 99: Halt
    * pid is increased by len(args) + 1 after running the instruction,
      unless the instruction was a jump instruction, in which case, no
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
    starting_relative_base: What should the global offset for mode 2 instructions
      start at?
  
  Return:
    The current PID if output_func returns Truthy. Else, -1 if opcode 99 is reached.
  """
  if not inplace:
    ops = copy.copy(ops)
  
  ops = MemoryWrapper(ops)
  if isinstance(inputs, list):
    inputs = InputWrapper(inputs)

  pid = starting_pid
  relative_base = starting_relative_base
  while True:
    full_opcode = ops[pid]
    opcode = full_opcode % 100

    if opcode == 1:
      add1, add2 = _get_args(ops, 2, full_opcode, pid, relative_base)
      _store(ops, add1 + add2, 3, full_opcode, pid, relative_base)
      pid += 4

    elif opcode == 2:
      add1, add2 = _get_args(ops, 2, full_opcode, pid, relative_base)
      _store(ops, add1 * add2, 3, full_opcode, pid, relative_base)
      pid += 4

    elif opcode == 3:
      if inputs:
        val = inputs.get()
      else:
        val = int(input('I request input:'))
      _store(ops, val, 1, full_opcode, pid, relative_base)
      pid += 2

    elif opcode == 4:
      #from IPython.core.debugger import Tracer; Tracer()()
      add = _get_args(ops, 1, full_opcode, pid, relative_base)
      pid += 2
      if output_func(add):
        return pid
    
    elif opcode == 5:
      add1, add2 = _get_args(ops, 2, full_opcode, pid, relative_base)
      if add1:
        pid = add2
      else:
        pid += 3
  
    elif opcode == 6:
      add1, add2 = _get_args(ops, 2, full_opcode, pid, relative_base)
      if not add1:
        pid = add2
      else:
        pid += 3

    elif opcode == 7:
      add1, add2 = _get_args(ops, 2, full_opcode, pid, relative_base)
      _store(ops, 1 if add1 < add2 else 0, 3, full_opcode, pid, relative_base)
      pid += 4
    
    elif opcode == 8:
      add1, add2, add3 = _get_args(ops, 3, full_opcode, pid, relative_base)
      _store(ops, 1 if add1 == add2 else 0, 3, full_opcode, pid, relative_base)
      pid += 4

    elif opcode == 9:
      add = _get_args(ops, 1, full_opcode, pid, relative_base)
      relative_base += add
      pid += 2

    elif opcode == 99:
      return -1

    else:
      raise ValueError("Invalid code: {}".format(ops[pid]))
