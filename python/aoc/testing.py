"""
Some functions to make testing slightly easier.
"""
from typing import List


def assert_all_equal(left: List, right: List):
  """
  Assert that each element of left is == each element of right in order.
  """
  assert len(left) == len(right)
  assert all(x == y for x, y in zip(left, right))
