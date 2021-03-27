import time

class VendingMachine:

    # defining the states
    STATE_IDLE = "Idle"
    STATE_WAITING = "Waiting"
    STATE_REFUNDING = "Refunding"
    STATE_DISPENSING = "Dispensing"
    

    # defining the valid transitions
    VALID_TRANSITIONS = {
        STATE_IDLE: [STATE_WAITING, STATE_IDLE],
        STATE_WAITING: [STATE_REFUNDING, STATE_DISPENSING, STATE_WAITING],
        STATE_REFUNDING: [STATE_IDLE],
        STATE_DISPENSING: [STATE_REFUNDING, STATE_IDLE]
    }
    
    # money inputs
    VALID_COINS = {
        "P": 0.01,
        "N": 0.05,
        "D": 0.10,
        "Q": 0.25,
        "1D": 1,
        "5D": 5, 
        "10D": 10
    }
    
    
    def __init__(self): 

        self.state = self.STATE_IDLE
        self.items = {}
        self.balance = 0


        
    def transition(self, new_state): # will check if a transition is valid, then make the transition

        # state is the same: valid transition, no need for print statement
        if self.state == new_state: 
            return True
        
        # valid transition
        if new_state in self.VALID_TRANSITIONS[self.state]: 
            self.state = new_state


            print("--------------------")
            print("State switched to {}\n--------------------".format(new_state))
            return True

        # invalid transition
        else: 
            print("Invalid transition: {} -> {}.".format(self.state, new_state))
            return False
            

        
    def refill(self): # will restore original quantities of all items

        if not self.transition(self.STATE_IDLE):
            return

        self.items = {

            "Pepsi": {
                "price": 2.00,
                "quantity": 5
            },

            "Coke": {
                "price": 2.00,
                "quantity": 5
            },

            "Sprite": {
                "price": 1.50,
                "quantity": 5
            },

            "Fanta": {
                "price": 4.00,
                "quantity": 2
            },

            "Twix": {
                "price": 0.50,
                "quantity": 10
            },

            "Protein Bar": {
                "price": 1.00,
                "quantity": 6
            }

        }
        print("--------------------")
        print("Machine refilled.")
        print("--------------------")
        time.sleep(1)

        
        
        
    def insert_coin(self): # user inserts coin into machine
        if not self.transition(self.STATE_WAITING):
            return 

        # processing coin input    
        while True: 
            try: 
                coin = input("Please add a coin to the machine (P, N, D, Q, 1D, 5D, 10D).")
                
            except: 
                print("Please insert a valid coin.")
                continue
                  
            if coin not in self.VALID_COINS: 
                print("Please insert a valid coin.")
                continue
            
            else: 
                self.balance += self.VALID_COINS[coin]
                break
        print("----------------------------------------")        
        print("Coin inserted. Your balance is {}".format(self.balance))
        print("----------------------------------------")



    def make_selection(self): # user selects item from machine

        # checking if user has inserted money
        if self.state != self.STATE_WAITING: 
            print("--------------------")
            print("Invalid transition: You must insert money before making a selection.")
            self.transition(self.STATE_IDLE)
            return


        self.show_items()

        # processing item input
        selected_item = None
        while True:
            try: 
                selected_item = str(input("Please enter the name of your selected item."))
                

                if selected_item not in self.items:
                    print("Please select a valid item.")
                    continue
                
                price = self.items[selected_item]['price']
                quantity = self.items[selected_item]['quantity']

                if self.balance < price:
                    print("You have not inserted enough coins to purchase this item. \
                        This item costs ${}. You have inserted ${}.".format(price, self.balance))
                    return
                if quantity == 0:
                    print("Please select an item that is in stock.")
                    continue
                else:
                    break
            except ValueError:
                print("Please select a valid item.")
                continue

        # dispensing item and refunding change
        self.dispense(selected_item)
        time.sleep(1)
        self.process_refund(selected_item)

        
    def calc_refund(self, selected_item): # calculates refund amount based on price of item and current balance
        price = self.items[selected_item]['price']
        if self.balance < price:
            return self.balance
        return self.balance - price


    def process_refund(self, selected_item): # refunds user, resets balance
        refund_amt = self.calc_refund(selected_item)
        
        self.transition(self.STATE_REFUNDING)

        if refund_amt == 0: 
            print("Your transaction is complete.")
            self.transition(self.STATE_IDLE)
        else: 
            print ("Refunding you a total of ${} in change...".format(refund_amt))
            self.balance = 0
            time.sleep(1)
            print("Your transaction is complete.")
            self.transition(self.STATE_IDLE)


    def dispense(self, selected_item): # gives item to user, updates count of items in machine
        self.transition(self.STATE_DISPENSING)
        time.sleep(1)
        print("Purchasing {}...".format(selected_item))
        self.items[selected_item]['quantity'] -= 1      


    

    def show_items(self): #displaying the menu of items in the machine
        print("--------------------\nCurrent Selection:")
        
        for item, info in self.items.items():
            print("{} | Price: {}, Quantity: {}".format(item, info['price'], info['quantity']))
        
        print("--------------------")
        
    def cancel(self): # cancels transaction, refunds any money in machine
        if self.balance != 0: 
            self.transition(self.STATE_REFUNDING)
            time.sleep(1)
            print("Refunded {} dollars.".format(self.balance))
            self.balance = 0
        time.sleep(1)
        self.transition(self.STATE_IDLE)

