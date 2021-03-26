from vending_machine import VendingMachine


def input_action(machine: VendingMachine):
    

    while True:
        print("Possible actions:")
        print("1. Refill\n2. Insert Coin\n3. Make Selection\n4. Cancel\n5. Quit\n")
        print("Current State: {}".format(machine.state))
        try:
            action = int(input("What action would you like to take? (Enter the number)"))

            if action < 1 or action > 5:
                print("Please enter a valid choice(1-5)")
                continue

            if action == 1:
                machine.refill()
            elif action == 2:
                machine.insert_coin()
            elif action == 3:
                machine.make_selection()
            elif action == 4:
                machine.cancel()
            elif action == 5:
                break

        except ValueError:
            print("Please enter a valid choice (1-4)")


if __name__ == '__main__':
    vending_machine = VendingMachine()
    vending_machine.refill()

    input_action(vending_machine)
