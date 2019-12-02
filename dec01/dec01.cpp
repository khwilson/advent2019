#include<assert.h>

#include<fstream>
#include<iostream>
#include<string>
#include <algorithm> 
#include <cctype>
#include <locale>


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

  {
    // Part 1
    std::ifstream myfile(argv[1]);
    int total = 0;
    if (myfile.is_open()) {
      std::string line;
      while (getline(myfile, line)) {
        trim(line);
        int val = std::stoi(line);
        total += mass_to_fuel(val);
      }
    }
    myfile.close();
    std::cout << "The total fuel necessary in Part 1 is " << total << std::endl;
  }

  {
    // Part 2
    std::ifstream myfile(argv[1]);
    int total = 0;
    if (myfile.is_open()) {
      std::string line;
      while (getline(myfile, line)) {
        trim(line);
        int fuel = std::stoi(line);
        while (fuel > 0) {
          fuel = mass_to_fuel(fuel);
          total += fuel;
        }
      }
    }
    myfile.close();
    std::cout << "The total fuel necessary in Part 2 is " << total << std::endl;

  }

  return 0;
}