while True:
    try:
        age = int(input("Enter your age: "))
        if 0 <= age <= 120:
            break
        print("Please enter an age between 0 and 120.")
    except ValueError:
        print("Please enter a whole number, e.g. 25.")
    except EOFError:
        raise SystemExit("\nNo input received.")

if age >= 18:
    print("You are eligible to vote")
else:
    print("You are underage")
