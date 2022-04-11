"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
import time


class Producer(Thread):
    """
    Class that represents a producer.
    """

    """
    self.nr_products reprezinta numarul de produse al fiecarui producator, pe care
    il folosesc cand verific ca nr de produse sa fie in limita queue_size_per_producer.
    """
    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        Thread.__init__(self, **kwargs)

        self.nr_products = 0
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time

        self.marketplace.producers.append(self)
        self.producer_id = self.marketplace.register_producer()

    """
    Parcurg toate produsele si mai fac un for in functie de cantitate, iar in while
    incerc sa adaug produsul in cazul in care mai are loc in coada, altfel astept.
    """
    def run(self):
        while True:
            for item in self.products:
                for _ in range(item[1]):

                    while self.marketplace.publish(self.producer_id, item[0]) is False:
                        time.sleep(self.republish_wait_time)

                    time.sleep(item[2])