"""
Some utilties for AOC 2019
"""
from typing import Tuple


def gcd(a: int, b: int) -> int:
  """
  Return the gcd of a and b. Both must be nonzero.
  """
  if a * b == 0:
    raise ValueError('Both a and b must be nonzero')
  a = abs(a)
  b = abs(b)
  if a > b:
    tmp = a
    a = b
    b = tmp
  while b % a != 0:
    tmp = b % a
    b = a
    a = tmp
  return a


def dist(left: Tuple[int, int], right: Tuple[int, int]) -> int:
  """ Return the square distance between left and right """
  return (left[0] - right[0]) ** 2 + (left[1] - right[1]) ** 2
