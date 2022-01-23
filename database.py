import psycopg2


class Database:
    def __init__(self, url):
        self.connection = psycopg2.connect(url)
        self.cursor = self.connection.cursor()
    
    def add_user(self, id, first_name, second_name, phone):
        with self.connection:
            self.cursor.execute("INSERT INTO users(id, first_name, second_name, phone)"
                                "VALUES (%(id)s, %(first_name)s, %(second_name)s, %(phone)s) ON CONFLICT(id) DO UPDATE SET " 
                                "id = %(id)s, first_name = %(first_name)s, second_name = %(second_name)s, phone = %(phone)s;", 
                                {'id': id, 
                                 'first_name': first_name, 
                                 'second_name': second_name,
                                 'phone': phone})
            
    def get_user(self, id):
        with self.connection:
            self.cursor.execute("SELECT * FROM users WHERE id = %s;", (id,))
            
            return self.cursor.fetchone()
        
    
    def get_apartament_by_categories(self, price, region, room_count):
        with self.connection:
            self.cursor.execute("SELECT id FROM apartament WHERE price <= %s AND region = %s AND room_count = %s ORDER BY price", (price, region, room_count, ))
            return self.cursor.fetchall()
        
    
    
    def get_apartament_info(self, id):
        with self.connection:
            self.cursor.execute("SELECT * FROM apartament WHERE id = %s", (id, ))
            apartament_info = self.cursor.fetchone()
            self.cursor.execute("SELECT url FROM apartament_photo WHERE apartament_id = %s", (id, ))
            apartament_photo = self.cursor.fetchall()
            
        return apartament_info, apartament_photo