1) The repo contains three files : RLalgo.cpp, DCalgo.cpp and script.py

    RLalgo.cpp contains implementation of running length algorithm and DCalgo.cpp contains implementation of Dictionary Coder algorithm.

2) script.py generates random test files of type .txt,image and binary, it automatically tests them on both RLalgo,DCalgo.
3) The results of the testcases are stored in folder name {algo}_results, which will automatically be created once process is done.
4) Inside the folders you can find the compressed, decompressed files and {algo}_compression_results.json which stores the compression time,compression size,decompression time for each file type.
5) Also script gives you comparison graphs of both algorithms based on compression ratio, compression time and decompression time.

In order to run the code you should have installed g++ and python3.

Simply type "./script.py" to run python script as executable file or type "python3 script.py" to run the script, rest everything will taken care by the script itself. 