"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from logging.handlers import RotatingFileHandler
from threading import Lock
import logging

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    """
    self.products este o lista ce contine tupluri (producer_id, product)
    self.producers este o lista ce contine producatorii, impreuna cu numarul de produse
    self.carts este o lista ce contine listele de produse ale clientilor.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """

        self.queue_size_per_producer = queue_size_per_producer

        self.producer_id = 0
        self.consumer_id = 0

        self.products = []
        self.producers = []
        self.carts = []

        self.lock = Lock()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        file_handler = RotatingFileHandler("marketplace.log")
        self.logger.addHandler(file_handler)

    """
    self.producer_id este id-ul ultimului producator adaugat, dar reprezinta si
    pozitia - 1 a respectivului producator in lista self.producers.
    """
    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """

        self.logger.info("Entered method: register_producer")
        self.lock.acquire()

        self.producer_id += 1
        producer_id = self.producer_id

        self.lock.release()

        self.logger.info("Exited method: register_producer")
        return producer_id


    """
    Daca numarul de produse al producatorului primit ca argument este mai mic
    decat limita, atunci in lista de produse adaug un nou tuplu in self.products.
    """
    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """

        self.logger.info("Entered method: publish")
        self.logger.info("Params: producer_id: " + str(producer_id)
        + ", product: " + str(product.name))
        self.lock.acquire()

        if self.producers[producer_id - 1].nr_products < self.queue_size_per_producer:

            self.products.append((producer_id, product))
            self.producers[producer_id - 1].nr_products += 1
            self.lock.release()
            self.logger.info("Exited method: publish")
            return True

        self.lock.release()
        self.logger.info("Exited method: publish")
        return False

    """
    self.consumer_id este id-ul ultimului client adaugat.
    Cu venirea unui nou client, adaug in lista de cosuri o noua lista goala.
    """
    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """

        self.logger.info("Entered method: new_cart")
        self.lock.acquire()

        self.consumer_id += 1
        consumer_id = self.consumer_id

        self.carts.append([])

        self.lock.release()

        self.logger.info("Exited method: new_cart")
        return consumer_id

    """
    Caut produsul sa vad daca exista, il adaug in cos si il sterg din lista de
    produse self.products.
    """
    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """

        self.logger.info("Entered method: add_to_cart")
        self.logger.info("Params: cart_id: " + str(cart_id) + ", product: " + str(product.name))
        self.lock.acquire()
        for item in self.products:
            if product == item[1]:

                self.carts[cart_id - 1].append(item)
                self.products.remove(item)
                self.producers[item[0] - 1].nr_products -= 1
                self.lock.release()
                self.logger.info("Exited method: add_to_cart")
                return True

        self.lock.release()
        self.logger.info("Exited method: add_to_cart")
        return False


    """
    Caut produsul in cos, iar daca exista il sterg din cos si il adaug inapoi
    in lista de produse self.products. De asemenea, actualizez si nr de produse
    al producatorului respectiv.
    """
    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """

        self.logger.info("Entered method: remove_from_cart")
        self.logger.info("Params: cart_id: " + str(cart_id) + ", product: " + str(product.name))
        self.lock.acquire()
        for item in self.carts[cart_id - 1]:
            if product == item[1]:

                self.carts[cart_id - 1].remove(item)
                self.products.append(item)
                self.producers[item[0] - 1].nr_products += 1
                self.lock.release()
                self.logger.info("Exited method: remove_from_cart")
                return

        self.lock.release()

    """
    Returnez cosul cu id-ul primit ca parametru.
    """
    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.logger.info("Entered method: place_order")
        self.logger.info("Exited method: place_order")
        return self.carts[cart_id - 1]