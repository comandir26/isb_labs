#include<iostream>
#include<random>


void generate(size_t size) {
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distrib(0, 1);
    for (size_t i = 0; i < size; ++i)
    {
        std::cout << distrib(gen);
    }
}

int main() {
    generate(128);
}