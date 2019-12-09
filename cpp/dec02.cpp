#include <assert.h>
#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <locale>
#include <sstream>
#include <string>
#include <vector>


void simulate(int *program, const size_t program_length) {
  size_t pid = 0;
  while (true) {
    if (pid >= program_length)
      throw std::runtime_error("Invalid program: overflow");

    int op = program[pid];
    switch (op) {
      case 1:
        program[program[pid + 3]] = program[program[pid + 1]] + program[program[pid + 2]];
        pid += 4;
        break;

      case 2:
        program[program[pid + 3]] = program[program[pid + 1]] * program[program[pid + 2]];
        pid += 4;
        break;

      case 99:
        return;

      default:
        throw std::runtime_error("Invalid program");
    }
  }
}

int main(int argc, char **argv) {
  if (!aoc::checkArgs(argc, 2)) return 1;
  auto vect = aoc::readAsLine(argv[1]);

  int part1total = 0, part2total = 0;
  int *part1_program = (int*) std::malloc(vect.size() * sizeof(int));
  memcpy(part1_program, &vect[0], vect.size() * sizeof(int));
  part1_program[1] = 12;
  part1_program[2] = 2;
  simulate(part1_program, vect.size());
  aoc::part1Answer(part1_program[0]);
  std::free(part1_program);

  int *part2_program = (int*) std::malloc(vect.size() * sizeof(int));
  for (int x = 0; x < vect.size(); ++x) {
    for (int y = 0; y < vect.size(); ++y) {
      memcpy(part2_program, &vect[0], vect.size() * sizeof(int));
      part2_program[1] = x;
      part2_program[2] = y;
      try {
        simulate(part1_program, vect.size());
      } catch (const std::exception &e) {}
      if (part2_program[0] == 19690720) {
          aoc::part2Answer(100 * x + y);
      }
    }
  }
  std::free(part2_program);

  return 0;
}
