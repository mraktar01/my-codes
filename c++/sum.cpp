#include <iostream>

int main() {
    int firstNumber, secondNumber, sum;

    std::cout << "Enter first integer: ";
    std::cin >> firstNumber;

    std::cout << "Enter second integer: ";
    std::cin >> secondNumber;

    sum = firstNumber + secondNumber;

    std::cout << "Sum: " << sum << std::endl;

    return 0;
}