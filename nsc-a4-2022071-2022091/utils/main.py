from auth import signup, login
from pdf_generator import generate_degree_certificate, generate_grade_report

def main():
    current_user = None
    while True:
        print("\n1. Signup\n2. Login\n3. Download Certificate & Report\n4. Exit")
        choice = input("Select option: ").strip()
        if choice == "1":
            signup()
        elif choice == "2":
            user = login()
            if user:
                current_user = user
        elif choice == "3":
            if not current_user:
                print("Please login first.")
            else:
                cert_path = generate_degree_certificate(current_user)
                report_path = generate_grade_report(current_user)
                print(f"Degree saved to: {cert_path}")
                print(f"Grades saved to: {report_path}")
        elif choice == "4":
            print("Exiting.")
            break
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
