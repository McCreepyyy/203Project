#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

// Structure to store user information
struct User {
    std::string username;
    std::string password;
    int gems; // New member variable to store gem count
};

// Global variables
int experience = 0;
int daystreak = 0;

// Function declarations
void login();
void menu(User currentuser); // Pass currentuser to menu function
void characters();
void leaderboard();
void profile(User currentuser); // Pass currentuser to profile function
void shop(User currentuser); // Pass currentuser to shop function
void quests();
void settings();
void languages(User currentuser); // Pass currentuser to languages function
void japanese();
void spanish();
void learn();
void createuser();
void exitProgram();

// Functions

// Language Selection
void languages(User currentuser) {
    system("clear");
    int choice;
    std::cout << "Choose Language: " << std::endl;
    std::cout << "1. Japanese" << std::endl;
    std::cout << "2. Spanish" << std::endl;
    std::cout << "3. Return to Menu" << std::endl;
    std::cin >> choice;

    switch (choice) {
        case 1:
            japanese();
            break;
        case 2:
            spanish();
            break;
        case 3:
            return; // Return to menu
        default:
            std::cout << "Invalid Choice." << std::endl;
            break;
    }
}

// Profile function
void profile(User currentuser) {
    system("clear");
    // Display Username
    std::cout << currentuser.username << std::endl;
    // Profile Statistics
    std::cout << "Statistics:" << std::endl << std::endl;
    std::cout << "Day Streak: " << daystreak << std::endl;
    std::cout << "Total XP: " << experience << std::endl;
    std::cout << "Gems: " << currentuser.gems << std::endl; // Display gem count
}

// Shop function
void shop(User currentuser) {
}


// Main Menu Function
void menu(User currentuser) {
    system("clear");
    int choice;
    do {
        std::cout << "Menu:" << std::endl;
        std::cout << "1. Learn" << std::endl;
        std::cout << "2. Characters" << std::endl;
        std::cout << "3. Leaderboard" << std::endl;
        std::cout << "4. Shop" << std::endl;
        std::cout << "5. Quests" << std::endl;
        std::cout << "6. Languages" << std::endl;
        std::cout << "7. Profile" << std::endl;
        std::cout << "8. Settings" << std::endl;
        std::cout << "9. Logout" << std::endl;
        std::cin >> choice;

        switch (choice) {
            case 1:
                learn();
                break;
            case 2:
                characters();
                break;
            case 3:
                leaderboard();
                break;
            case 4:
                shop(currentuser); // Pass currentuser to shop function
                break;
            case 5:
                quests();
                break;
            case 6:
                languages(currentuser); // Pass currentuser to languages function
                break;
            case 7:
                profile(currentuser); // Pass currentuser to profile function
                break;
            case 8:
                settings();
                break;
            case 9:
                return; // Return from menu function if logout is chosen
            default:
                std::cout << "Invalid choice." << std::endl;
                break;
        }
    } while (choice != 9);
}

// Close program
void exitProgram() {
    std::cout << "Exiting program." << std::endl;
    exit(0);
}

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
    system("clear");
    string username, password;
    User currentuser;
    bool found = false; // Initialize found variable

    std::cout << "Enter Username: ";
    std::cin >> username;
    std::cout << "Enter password: ";
    std::cin >> password; // Read password

    if (username.empty() || password.empty()) {
        std::cout <<"Username and password can not be empty." << std::endl;
        return;
    }

    ifstream usersfile("Accounts.txt");
    while (usersfile >> currentuser.username >> currentuser.password) {
        if (currentuser.username == username && currentuser.password == password) {
            found = true;
            menu(currentuser);
            break;
        }
    }
    if (!found) {
        std::cout << "Username or password is incorrect." << std::endl;
    }
    usersfile.close();
}

// Main function
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
