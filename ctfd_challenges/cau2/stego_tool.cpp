// ============================================================================
//   Challenge 2 - Steganography Tool (C++)  --  FILL IN THE BLANKS
// ============================================================================
//  The file worldcup.png looks like an ordinary image, but the flag is hidden
//  as plain TEXT inside the file itself (in its metadata). You do NOT need to
//  touch the pixels -- just read ALL the bytes of the file and look for the
//  flag text  UIT{...} .
//
//  Build:  g++ -std=c++17 -O2 -o stego_tool stego_tool.cpp
//  Run:    ./stego_tool worldcup.png        (Windows: stego_tool.exe worldcup.png)
//
//  YOUR TASK: implement the 2 functions marked  >>> FILL <<< :
//    (1) read_file_bytes() - read ALL the bytes of the image file
//    (2) find_flag()       - locate the  UIT{...}  text inside those bytes
// ============================================================================
#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <iterator>

// ============================================================================
//  (1) >>> FILL <<<
//  Open the file in BINARY mode and return ALL of its bytes as a std::string.
// ============================================================================
std::string read_file_bytes(const std::string& path) {

    return "";   // <-- replace with the bytes read from the file
}

// ============================================================================
//  (2) >>> FILL <<<
//  'data' holds all the bytes of the file. Find the hidden UIT{...} string and
//  return it. 
// ============================================================================
std::string find_flag(const std::string& data) {

    return "";   // <-- replace with the flag you found
}

int main(int argc, char** argv) {
    std::string path = (argc > 1) ? argv[1] : "worldcup.png";
    std::cout << "========================================================\n";
    std::cout << "  STEGO DECODER (C++) -- file: " << path << "\n";
    std::cout << "========================================================\n";

    std::string data = read_file_bytes(path);
    std::string flag = find_flag(data);

    if (!flag.empty() && flag.rfind("UIT{", 0) == 0)
        std::cout << "  >>> FLAG FOUND: " << flag << "\n";
    else
        std::cout << "  Flag not found. Complete the two functions above.\n";

    std::cout << "========================================================\n";
    return 0;
}
