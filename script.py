import subprocess
import os
import time
import json
import random
import string
from PIL import Image
import matplotlib.pyplot as plt

def generate_text_file(filename, size_mb):
    with open(filename, 'w') as f:
        for _ in range(size_mb * 1024):
            f.write(''.join(random.choices(string.ascii_letters + string.digits, k=10)))

def generate_binary_file(filename, size_mb):
    with open(filename, 'wb') as f:
        f.write(os.urandom(size_mb * 1024 * 1024))

def generate_image_file(filename, width, height):
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    for i in range(width):
        for j in range(height):
            pixels[i, j] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image.save(filename)

def compile_cpp_program(program_name):
    subprocess.run(f"g++ -o {program_name} {program_name}.cpp", shell=True)

def run_cpp_program(program_name, input_file, output_file, action):
    cpp_program = f"./{program_name}"
    subprocess.run([cpp_program, input_file, output_file, action])

def measure_file_size(file_path):
    return os.path.getsize(file_path) / (1024 * 1024)

def measure_time(func, *args):
    start_time = time.time()
    func(*args)
    end_time = time.time()
    return end_time - start_time

def load_results(algo):
    results_file = f"{algo}_results/{algo}_compression_results.json"
    with open(results_file, "r") as f:
        return json.load(f)

def plot_comparison_graphs(results_rl, results_dc, algo):
    file_types = results_rl.keys()
    for file_type in file_types:
        plt.figure(figsize=(10, 6))
        plt.bar([0, 1], [results_rl[file_type]["Compression Time (s)"], results_dc[file_type]["Compression Time (s)"]], color=['blue', 'green'])
        plt.xticks([0, 1], [f'{algo} Compression', 'DCalgo Compression'])
        plt.ylabel('Time (s)')
        plt.title(f'Compression Time Comparison for {file_type.capitalize()} Files')
        plt.savefig(f'{algo}_vs_DCalgo_{file_type}_compression_time.png')
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.bar([0, 1], [results_rl[file_type]["Decompression Time (s)"], results_dc[file_type]["Decompression Time (s)"]], color=['blue', 'green'])
        plt.xticks([0, 1], [f'{algo} Decompression', 'DCalgo Decompression'])
        plt.ylabel('Time (s)')
        plt.title(f'Decompression Time Comparison for {file_type.capitalize()} Files')
        plt.savefig(f'{algo}_vs_DCalgo_{file_type}_decompression_time.png')
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.bar([0, 1], [results_rl[file_type]["Original File Size (MB)"]/results_rl[file_type]["Compressed File Size (MB)"], results_dc[file_type]["Original File Size (MB)"]/results_dc[file_type]["Compressed File Size (MB)"]], color=['blue', 'green'])
        plt.xticks([0, 1], [f'{algo} Compression', 'DCalgo Compression'])
        plt.ylabel('Compression Ratio')
        plt.title(f'Compression Ratio Comparison for {file_type.capitalize()} Files')
        plt.savefig(f'{algo}_vs_DCalgo_{file_type}_compression_ratio.png')
        plt.close()

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    generate_text_file(os.path.join(current_dir, "input_text.txt"), 10)
    generate_binary_file(os.path.join(current_dir, "input_binary.bin"), 10)
    generate_image_file(os.path.join(current_dir, "input_image.png"), 128, 128)

    compile_cpp_program("RLalgo")
    compile_cpp_program("DCalgo")

    algorithms = ["RLalgo", "DCalgo"]

    for algo in algorithms:
        results = {}

        results_dir = os.path.join(current_dir, f"{algo}_results")
        if not os.path.exists(results_dir):
            os.makedirs(results_dir)

        files = {
            "text": {
                "input": os.path.join(current_dir, "input_text.txt"),
                "compressed": os.path.join(results_dir, "compressed_text.bin"),
                "decompressed": os.path.join(results_dir, "decompressed_text.txt")
            },
            "image": {
                "input": os.path.join(current_dir, "input_image.png"),
                "compressed": os.path.join(results_dir, "compressed_image.bin"),
                "decompressed": os.path.join(results_dir, "decompressed_image.png")
            },
            "binary": {
                "input": os.path.join(current_dir, "input_binary.bin"),
                "compressed": os.path.join(results_dir, "compressed_binary.bin"),
                "decompressed": os.path.join(results_dir, "decompressed_binary.bin")
            }
        }

        for file_type, paths in files.items():
            print(f"Processing {file_type} file with {algo}...")

            input_file = paths["input"]
            compressed_file = paths["compressed"]
            decompressed_file = paths["decompressed"]

            print("Compressing...")
            compression_time = measure_time(run_cpp_program, algo, input_file, compressed_file, "compress")
            compressed_size = measure_file_size(compressed_file)

            print("Decompressing...")
            decompression_time = measure_time(run_cpp_program, algo, compressed_file, decompressed_file, "decompress")

            results[file_type] = {
                "Original File Size (MB)": measure_file_size(input_file),
                "Compression Time (s)": compression_time,
                "Compressed File Size (MB)": compressed_size,
                "Decompression Time (s)": decompression_time
            } 

            print(f"{file_type.capitalize()} file processing complete.")

        with open(os.path.join(results_dir, f"{algo}_compression_results.json"), "w") as f:
            json.dump(results, f, indent=4)

        print(f"Results for {algo} saved to {results_dir}/{algo}_compression_results.json.")


    results_rl = load_results("RLalgo")
    results_dc = load_results("DCalgo")

    plot_comparison_graphs(results_rl, results_dc, "RLalgo")

if __name__ == "__main__":
    main()
