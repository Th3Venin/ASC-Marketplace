"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time

ADD_COMMAND = "add"
REMOVE_COMMAND = "remove"
COMMAND_TYPE = "type"
ITEM_QUANTITY = "quantity"
PRODUCT = "product"
NAME = "name"

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)

        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.consumer_name = kwargs[NAME]

    """
    Parcurg fiecare produs din cos, apoi parcurg fiecare comanda si implementez
    logica diferita in functie de tipul comenzii. Daca este "add", incerc sa
    adaug produsul in cos, daca nu reusesc atunci astept. Daca comanda este
    "remove", incerc sa sterg produsul din cos, iar daca nu reusesc astept.
    La final, in cos raman doar produsele finale, apelez place_order si afisez
    produsele respective in fisierul de output.
    """
    def run(self):
        id_cart = self.marketplace.new_cart()

        for item in self.carts:
            for command in item:

                if command[COMMAND_TYPE] == ADD_COMMAND:

                    for _ in range(command[ITEM_QUANTITY]):
                        while self.marketplace.add_to_cart(id_cart, command[PRODUCT]) is False:
                            time.sleep(self.retry_wait_time)

                elif command[COMMAND_TYPE] == REMOVE_COMMAND:

                    for _ in range(command[ITEM_QUANTITY]):
                        self.marketplace.remove_from_cart(id_cart, command[PRODUCT])

        order_result = self.marketplace.place_order(id_cart)

        for item in order_result:

            self.marketplace.lock.acquire()
            print(self.consumer_name + " bought " + str(item[1]))
            self.marketplace.lock.release()