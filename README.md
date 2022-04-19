# ASC-Marketplace

Implementare:

marketplace.py:

__init__:
self.products este o lista ce contine tupluri (producer_id, product).
self.producers este o lista ce contine producatorii (obiecte), impreuna cu numarul de produse.
self.carts este o lista ce contine listele de produse ale clientilor (adica tot tupluri ca in
self.products).
self.producer_id este id-ul ultimului producator adaugat, de asemenea poate fi folosit
si ca nr total de producatori.
self.consumer_id este id-ul ultimului client adaugat, de asemenea poate fi folosit
si ca nr total de clienti.
self.lock este mutexul pe care il folosesc pt sincronizare (!!! self.lock l-am folosit
mereu cu un scop, am pus lock peste tot unde era nevoie, daca este scos lacatul atunci
pica testele pe checker).
self.logger se ocupa de afisarea intrarilor/iesirilor din functii, aceste mesaje fiind
scrise in fisierul marketplace.log.

register_producer:
Incrementez producer_id si il returnez.

publish:
Daca numarul de produse al producatorului primit ca argument este mai mic
decat limita queue_size_per_producer, atunci in lista de produse adaug un nou tuplu 
in self.products.

new_cart:
Incrementez consumer_id si adaug o noua lista goala in lista de cosuri.

add_to_cart:
Caut produsul sa vad daca exista, il adaug in cos si il sterg din lista de
produse self.products. De asemenea actualizez nr de produse al producatorului
respectiv.

remove_from_cart:
Caut produsul in cos, iar daca exista il sterg din cos si il adaug inapoi
in lista de produse self.products. De asemenea, actualizez si nr de produse
al producatorului respectiv.

place_order:
Returnez cosul cu id-ul primit ca parametru.


producer.py:

__init__:
Aici am mai adaugat un atribut, respectiv self.nr_products, pe care il actualizez in
marketplace.py si il folosesc cand verific ca nr de produse sa fie in limita
queue_size_per_producer. De asemenea, aici adaug fiecare producator nou in lista
producers din marketplace.

run:
Parcurg toate produsele si mai fac un for in functie de cantitate, iar in while
incerc sa adaug produsul in cazul in care mai are loc in coada, altfel astept.


consumer.py:

run:
Parcurg fiecare produs din cos, apoi parcurg fiecare comanda si implementez
logica diferita in functie de tipul comenzii. Daca este "add", incerc sa
adaug produsul in cos, daca nu reusesc atunci astept. Daca comanda este
"remove", incerc sa sterg produsul din cos, iar daca nu reusesc astept.
La final, in cos raman doar produsele finale, apelez place_order si afisez
produsele respective in fisierul de output.
