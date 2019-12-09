namespace aoc {
  std::vector<int> split_string(std::string &str, char sep = ',') {

    std::vector<int> vect;
    std::stringstream ss (str);
    for (int i; ss >> i; ) {
      vect.push_back(i);
      if (ss.peek() == sep) {
        ss.ignore();
      }
    }

    return vect;
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

  static inline bool checkArgs(int argc, int num_args) {
    if (argc != num_args) {
      std::cerr << "Wrong number of arguments provided" << std::endl;
      return false;
    }
    return true;
  }

  static inline std::vector<int> readAsLine(char *filename) {
    std::ifstream myfile (filename);
    if (!myfile.is_open())
      throw std::runtime_error("Problem opening file");

    std::string line;
    getline(myfile, line);
    trim(line);
    auto vect = split_string(line);
    myfile.close();

    return vect;
  }

  template<T>
  static inline void printAnswer(T answer, int part) {
    std::cout << "The answer to part " << part << " is " << answer << std::endl;
  }

  template<T>
  static inline void part1Answer(T answer) {
    printAnswer(answer, 1);
  }

  template<T>
  static inline void part2Answer(T answer) {
    printAnswer(answer, 2);
  }
}
