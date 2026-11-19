#include<iostream>
#include<fstream>
using namespace std;
int main()
{
    int ch;
    string na, city, clg;
    cout << "What do you want to do?\n1. Create/Modify file(Creats First time only)\n2. Read the file\n";
    cin >> ch;
    
    ifstream fr("t.txt", ios::in);
    if (!fr)
    {
        cout << "File created!" << endl;
        ofstream data("t.txt", ios::out);
        cout << "Enter the name of the student: ";
        cin >> na;
        cout << "Enter the city of the student: ";
        cin >> city;
        cout << "Enter the college of the student: ";
        cin >> clg;
        data << "\t" << na << "\t" << city << "\t" << clg << endl;
        data.close();
        return 0;
    }

    if (ch == 1)
    {
        ofstream data2("t.txt", ios::app);
        cout << "Enter the name of the student: ";
        cin >> na;
        cout << "Enter the city of the student: ";
        cin >> city;
        cout << "Enter the college of the student: ";
        cin >> clg;
        data2 << "\t" << na << "\t" << city << "\t" << clg << endl;
        data2.close();
        return 0;
    
    }

    else if (ch == 2)
    {
        while (fr >> na >> city >> clg)
        {
            cout << "\n"
                 << na << "\t" << city << "\t" << clg;
        }
        fr.close();
    }
    else
    {
        cout << "Invalid choice";
        return 0;
    }
    return 0;
}