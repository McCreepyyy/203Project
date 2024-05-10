#include <iostream>
#include <fstream>
using namespace std;

// Structure to store user information
struct User {
    std::string username;
    std::string password;
};

// Function declarations
void login();
void menu(std::string username);
void characters();
void leaderboard();
void profile();
void shop();
void quests();
void settings();
void languages();
void learn();
void createuser();
void exitProgram();

// Function for register
void createuser() {
    system("clear");

    User newuser;
    std::cout << "Enter Username: ";
    std::cin >> newuser.username;
    std::cout << "Enter Password: ";
    std::cin >> newuser.password;

    ofstream usersfile("Accounts.txt", ios::app);
    usersfile << newuser.username << " " << newuser.password << " " << std::endl;
    usersfile.close();

    std::cout << "Account Created Successfully!" << std::endl;

    main();
}

// Function for login
void login() {
    // Your login function implementation
}

// Main Menu
void menu(std::string username) {
    // Your menu function implementation
}

// Other functions go here

// Close program
void exitProgram() {
    std::cout << "Exiting program." << std::endl;
    exit(0);
}

int main() {
    system("clear");
    int choice;
    std::cout << "1. Login" << std::endl;
    std::cout << "2. Register" << std::endl;
    std::cout << "3. Exit" << std::endl;
    std::cin >> choice;

    if (choice == 1) {
        login();
    } else if (choice == 2) {
        createuser();
    } else if (choice == 3) {
        exitProgram();
    }

    return 0;
}
