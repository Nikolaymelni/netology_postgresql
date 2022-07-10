import psycopg2


def drop_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
                DROP TABLE phone,
                DROP TABLE client
            );
            """)
        conn.commit()


def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS client(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(80) NOT NULL,
                last_name VARCHAR(80) NOT NULL,
                email VARCHAR(80) NOT NULL UNIQUE
        );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phone(
                id SERIAL PRIMARY KEY,
                client_id INTEGER NOT NULL REFERENCES client(id),
                number VARCHAR(20) NOT NULL UNIQUE);
        """)
        conn.commit()


def add_new_client(conn, first_name, last_name, email):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO client(first_name,last_name,email)
            VALUES(%s,%s,%s) RETURNING id,first_name,last_name,email;
        """, (first_name, last_name, email))
        print(cur.fetchone())
        pass


def add_phone_number(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phone(client_id,number)
            VALUES(%s,%s);
            """, (client_id, phone))
        conn.commit()
        pass


def change_data(conn, client_id, first_name=None, last_name=None, email=None, number=None):
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE client
            SET first_name = %s WHERE id = %s;
            """, (first_name, client_id))

        cur.execute("""
            UPDATE client
            SET last_name = %s WHERE id = %s;
            """, (last_name, client_id))

        cur.execute("""
            UPDATE client
            SET email = %s WHERE id = %s;
            """, (email, client_id))

        cur.execute("""
             UPDATE phone
             SET number = %s WHERE client_id = %s;
             """, (number, client_id))

        conn.commit()

        pass


def delete_phone_number(conn, client_id, number):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phone WHERE client_id = %s AND number = %s;
            """, (client_id, number))
        conn.commit()
        pass


def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
           DELETE FROM phone WHERE client_id = %s;
           """, (client_id,))

        cur.execute("""
           DELETE FROM client WHERE id = %s;
           """, (client_id,))

        conn.commit()
        pass


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
            SELECT client.id, client.first_name, client.last_name, client.email, phone.number FROM client
            JOIN phone ON client.id = phone.client_id
            WHERE client.first_name = %s OR client.last_name = %s OR client.email = %s OR phone.number = %s;
            """, (first_name, last_name, email, phone))

        print(cur.fetchone())
        pass


with psycopg2.connect(database='netology_db', user='postgres', password='180594') as conn:
    pass
    create_db(conn)
#   add_new_client(conn, 'Nikolai', 'Melnichenko', 'nikolaymelni@gmail.com')
#   add_phone_number(conn, 1, 9999999999)
#   add_phone_number(conn, 1, 9999999998)
#   delete_phone_number(conn,1, '9999999999')
#   delete_client(conn, 2)
#   find_client(conn, 'Nikolai')
#   change_data(conn, 1,'Nikolay', 'Melnichenko', 'Nikolay@gmail.com','89999999999')
