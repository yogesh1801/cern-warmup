#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>

std::vector<unsigned char> compress(const std::vector<unsigned char>& data) {
    std::unordered_map<std::string, unsigned char> dictionary;
    std::vector<unsigned char> compressed;
    std::string current;

    for (unsigned char c : data) {
        std::string current_plus_c = current + std::string(1, c); 
        if (dictionary.find(current_plus_c) != dictionary.end()) {
            current = current_plus_c;
        } else {
            compressed.push_back(dictionary[current]);
            dictionary[current_plus_c] = dictionary.size(); // Assigning new code
            current = c;
        }
    }

    if (!current.empty()) {
        compressed.push_back(dictionary[current]);
    }

    return compressed;
}

std::vector<unsigned char> decompress(const std::vector<unsigned char>& compressed) {
    std::vector<unsigned char> decompressed;
    std::unordered_map<unsigned char, std::string> dictionary;
    unsigned int code = 256;

    for (unsigned int i = 0; i < 256; ++i) {
        dictionary[i] = std::string(1, static_cast<unsigned char>(i));
    }

    unsigned char prev = compressed[0];
    decompressed.push_back(prev);

    for (size_t i = 1; i < compressed.size(); ++i) {
        unsigned char curr = compressed[i];

        std::string entry;
        if (dictionary.find(curr) != dictionary.end()) {
            entry = dictionary[curr];
        } else if (curr == code) {
            entry = dictionary[prev] + dictionary[prev][0];
        } else {
            throw std::runtime_error("Decompression error: Invalid code");
        }

        decompressed.insert(decompressed.end(), entry.begin(), entry.end());

        dictionary[code++] = dictionary[prev] + entry[0];

        prev = curr;
    }

    return decompressed;
}

int main(int argc, char* argv[]) {
    if (argc != 4) {
        std::cerr << "Usage: " << argv[0] << " <input_file> <output_file> <action>\n";
        return 1;
    }

    std::ifstream input_file(argv[1], std::ios::binary);
    std::ofstream output_file(argv[2], std::ios::binary);

    if (!input_file.is_open() || !output_file.is_open()) {
        std::cerr << "Error: Could not open files.\n";
        return 1;
    }

    std::vector<unsigned char> input_data((std::istreambuf_iterator<char>(input_file)), (std::istreambuf_iterator<char>()));

    std::vector<unsigned char> result_data;
    try {
        if (std::string(argv[3]) == "compress") {
            result_data = compress(input_data);
        } else if (std::string(argv[3]) == "decompress") {
            result_data = decompress(input_data);
        } else {
            std::cerr << "Error: Invalid action.\n";
            return 1;
        }
    } catch (const std::exception& e) {
        std::cerr << e.what() << std::endl;
        return 1;
    }

    output_file.write(reinterpret_cast<const char*>(result_data.data()), result_data.size());

    input_file.close();
    output_file.close();

    return 0;
}
