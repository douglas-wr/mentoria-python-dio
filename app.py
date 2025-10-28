from __future__ import annotations

from sqlalchemy.orm import Session

from config.base import Base, engine
from models.customer import Customer
from models.order import Order

def create_db() -> None:
    Base.metadata.create_all(engine)

def drop_db() -> None:
    Base.metadata.drop_all(engine)

def create_customer(session: Session, name: str, email: str) -> Customer:
    c = Customer(name=name, email=email)
    session.add(c)
    session.flush()
    return c

def create_order(session: Session, customer_id: int, item: str, price: float) -> Order:
    o = Order(customer_id=customer_id, item=item, price=price)
    session.add(o)
    session.flush()
    return o

def main():
    drop_db()
    create_db()

    with Session(engine) as session:
        customer = create_customer(session, "Douglas Rittono", "douglas.willian@luizalabs.com")
        print(f"Cliente criado: {customer}")

        order1 = create_order(session, customer.id, "Notebook", 2500.00)
        order2 = create_order(session, customer.id, "Mouse", 50.00)
        order3 = create_order(session, customer.id, "Teclado Gamer", 250.00)

        print(f"Pedido 1: {order1}")
        print(f"Pedido 2: {order2}")
        print(f"Pedido 3: {order3}")

        session.commit()

        customers = session.query(Customer).all()
        print(f"\nTodos os clientes: {customers}")

        customers_orders = session.query(Order).filter(Order.customer_id == customer.id).all()
        print(f"Pedidos do cliente {customer.name}: {customers_orders}")

if __name__ == "__main__":
    main()