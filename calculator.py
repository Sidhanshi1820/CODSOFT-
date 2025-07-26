def calculator():
    """Simple calculator with basic arithmetic operations"""
    
    print("=" * 40)
    print("      SIMPLE CALCULATOR")
    print("=" * 40)
    
    try:
        # Get first number from user
        num1 = float(input("Enter the first number: "))
        
        # Get second number from user
        num2 = float(input("Enter the second number: "))
        
        # Display operation choices
        print("\nSelect operation:")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        
        # Get operation choice from user
        choice = input("\nEnter choice (1/2/3/4): ")
        
        # Perform calculation based on choice
        if choice == '1':
            result = num1 + num2
            operation = "+"
        elif choice == '2':
            result = num1 - num2
            operation = "-"
        elif choice == '3':
            result = num1 * num2
            operation = "*"
        elif choice == '4':
            if num2 != 0:
                result = num1 / num2
                operation = "/"
            else:
                print("\nError: Division by zero is not allowed!")
                return
        else:
            print("\nError: Invalid choice! Please select 1, 2, 3, or 4.")
            return
        
        # Display the result
        print("\n" + "=" * 40)
        print(f"Result: {num1} {operation} {num2} = {result}")
        print("=" * 40)
        
    except ValueError:
        print("\nError: Please enter valid numbers!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

def main():
    """Main function to run the calculator"""
    while True:
        calculator()
        
        # Ask if user wants to perform another calculation
        again = input("\nDo you want to perform another calculation? (y/n): ").lower()
        if again != 'y' and again != 'yes':
            print("\nThank you for using the calculator!")
            break
        print("\n")

# Run the calculator
if __name__ == "__main__":
    main()