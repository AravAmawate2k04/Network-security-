#include <bits/stdc++.h>
using namespace std;

// Improved hash function using a simple rolling hash
int improvedHash(const string &str) {
    int hash = 2026;
    for (char c : str) {
        hash = ((hash << 5) + hash) + c; // hash * 33 + c
    }
    return abs(hash % 10007); // Ensure non-negative values
}

// Function to encrypt plaintext using Vigenère cipher
string encryptVigenere(const string &plaintext, const string &key) {
    string ciphertext;
    int key_len = key.length();
    for (size_t i = 0; i < plaintext.length(); ++i) {
        int p = plaintext[i] - 'a';
        int k = key[i % key_len] - 'a';
        ciphertext += 'a' + (p + k) % 26;
    }
    return ciphertext;
}

// Function to decrypt ciphertext using Vigenère cipher
string decryptVigenere(const string &ciphertext, const string &key) {
    string plaintext;
    int key_len = key.length();
    for (size_t i = 0; i < ciphertext.length(); ++i) {
        int c = ciphertext[i] - 'a';
        int k = key[i % key_len] - 'a';
        plaintext += 'a' + (c - k + 26) % 26;
    }
    return plaintext;
}

int main() {
    // Define known key (for encryption)
    string known_key = "king"; // Key length is 4

    // Define plaintexts
    vector<string> plaintexts = {"aravamawate", "angad", "appar", "drbnjain", "rastogi"};

    // Compute hashes for plaintexts
    vector<int> plaintext_hashes;
    for (const auto &p : plaintexts) {
        plaintext_hashes.push_back(improvedHash(p));
    }

    // Encrypt plaintexts
    vector<string> ciphertexts;
    for (const auto &p : plaintexts) {
        ciphertexts.push_back(encryptVigenere(p, known_key));
    }

    // Display plaintexts, hashes, and ciphertexts
    cout << "Plaintexts and their hashes:\n";
    for (size_t i = 0; i < plaintexts.size(); ++i) {
        cout << "P" << i + 1 << ": (" << plaintexts[i] << ", " << plaintext_hashes[i] << ")\n";
    }

    cout << "\nCiphertexts:\n";
    for (size_t i = 0; i < ciphertexts.size(); ++i) {
        cout << "C" << i + 1 << ": " << ciphertexts[i] << "\n";
    }

    // Brute-force attack
    cout << "\nStarting brute-force attack...\n";

    bool key_found = false;
    string discovered_key;

    // Try all possible 4-letter keys
    for (char k1 = 'a'; k1 <= 'z' && !key_found; ++k1) {
        for (char k2 = 'a'; k2 <= 'z' && !key_found; ++k2) {
            for (char k3 = 'a'; k3 <= 'z' && !key_found; ++k3) {
                for (char k4 = 'a'; k4 <= 'z' && !key_found; ++k4) {
                    string current_key = {k1, k2, k3, k4};

                    bool all_match = true;
                    for (size_t i = 0; i < ciphertexts.size(); ++i) {
                        string decrypted = decryptVigenere(ciphertexts[i], current_key);
                        
                        // Fix: Compare the decrypted text directly with the original plaintext
                        if (decrypted != plaintexts[i]) {
                            all_match = false;
                            break;
                        }
                    }

                    if (all_match) {
                        discovered_key = current_key;
                        key_found = true;
                        break;
                    }
                }
            }
        }
    }

    // Display results
    if (key_found) {
        cout << "\nKey discovered: " << discovered_key << "\n";
        cout << "\nVerifying decrypted plaintexts:\n";
        for (size_t i = 0; i < ciphertexts.size(); ++i) {
            string decrypted = decryptVigenere(ciphertexts[i], discovered_key);
            cout << "Decrypted P" << i + 1 << ": " << decrypted << "\n";
        }
    } else {
        cout << "Key not found in the key space.\n";
    }

    return 0;
}
