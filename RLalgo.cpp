#include <iostream>
#include <fstream>
#include <vector>

std::vector<unsigned char> compress(const std::vector<unsigned char>& data) {
    std::vector<unsigned char> compressed;
    unsigned char current = data[0];
    int count = 1;

    for (size_t i = 1; i < data.size(); ++i) {
        if (data[i] == current && count < 255) {
            ++count;
        } else {
            compressed.push_back(count);
            compressed.push_back(current);
            current = data[i];
            count = 1;
        }
    }

    compressed.push_back(count);
    compressed.push_back(current);

    return compressed;
}

std::vector<unsigned char> decompress(const std::vector<unsigned char>& compressed) {
    std::vector<unsigned char> decompressed;

    for (size_t i = 0; i < compressed.size(); i += 2) {
        unsigned char count = compressed[i];
        unsigned char value = compressed[i + 1];

        for (int j = 0; j < count; ++j) {
            decompressed.push_back(value);
        }
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

    std::vector<unsigned char> input_data(std::istreambuf_iterator<char>(input_file), {});

    std::vector<unsigned char> result_data;
    if (std::string(argv[3]) == "compress") {
        result_data = compress(input_data);
    } else if (std::string(argv[3]) == "decompress") {
        result_data = decompress(input_data);
    } else {
        std::cerr << "Error: Invalid action.\n";
        return 1;
    }

    output_file.write(reinterpret_cast<const char*>(result_data.data()), result_data.size());

    input_file.close();
    output_file.close();

    return 0;
}
