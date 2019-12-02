#include<assert.h>
#include<algorithm> 
#include<cctype>
#include<fstream>
#include<iostream>
#include<locale>
#include<string>

/// <summary>
///   Convert a mass to the amount of fuel it requires
/// </summary>
/// <param name="mass">The mass to convert</param>
/// <returns>The amount of fuel required</returns>
int mass_to_fuel(int mass) {
  return std::max(mass / 3 - 2, 0);
}

// trim from start (in place)
static inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(), [](int ch) {
        return !std::isspace(ch);
    }));
}

// trim from end (in place)
static inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(), [](int ch) {
        return !std::isspace(ch);
    }).base(), s.end());
}

// trim from both ends (in place)
static inline void trim(std::string &s) {
    ltrim(s);
    rtrim(s);
}

int main(int argc, char** argv) {
  if (argc != 2) {
    std::cerr << "Wrong number of arguments provided" << std::endl;
    return 1;
  }

  // Run some simple tests
  assert(mass_to_fuel(12) == 2);
  assert(mass_to_fuel(14) == 2);
  assert(mass_to_fuel(1969) == 654);
  assert(mass_to_fuel(100756) == 33583);

  std::ifstream myfile(argv[1]);
  int part1total = 0, part2total = 0;
  if (myfile.is_open()) {
    std::string line;
    while (getline(myfile, line)) {
      trim(line);
      int mass = std::stoi(line);
      int fuel = mass_to_fuel(mass);
      part1total += fuel;
      part2total += fuel;
      while (fuel > 0) {
        fuel = mass_to_fuel(fuel);
        part2total += fuel;
      }
    }
  } else {
    std::cerr << "Error opening file" << std::endl;
    return 1;
  }
  myfile.close();
  std::cout << "The total fuel necessary in Part 1 is " << part1total << std::endl;
  std::cout << "The total fuel necessary in Part 2 is " << part2total << std::endl;

  return 0;
}