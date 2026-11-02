import sqlite3
from argon2 import PasswordHasher
from cryptography.fernet import Fernet

# python3 -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
SECRET_KEY = b"fojBlPEtESSbDj3nOdzojBh-0RuEFpJABz8wl1sA-bw="
cipher = Fernet(SECRET_KEY)

DB = "database.db"

class TableCreate:
    def __init__(self):
        self.users()
        self.books()

    def users(self):
        conn = sqlite3.connect("database.db")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                registered_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

    def books(self):
        conn = sqlite3.connect("database.db")

        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                creater_username TEXT NOT NULL,
                bookname TEXT NOT NULL,
                note TEXT,
                name_with_access TEXT,
                public INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        conn.close()

class users:
    def add(username,password,password2):
        def addUp():
            DB = "database.db"

            ph = PasswordHasher(
                time_cost=3,
                memory_cost=65536,
                parallelism=4
            )

            conn = sqlite3.connect(DB)
            cursor = conn.cursor()

            password_hash = ph.hash(password)

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password_hash)
            )

            conn.commit()
            conn.close()

        def username_check(name):
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT EXISTS(SELECT 1 FROM users WHERE username = ?)",
                (name,)
            )

            exists = cursor.fetchone()[0]

            conn.close()

            if exists:
                return True
            else:
                return False
        

        if " " in username:
            return "Kullanıcı Adı Uygunsuzdur"

        if " " in password:
            return "Şifrede Boşluk Olamaz"  

        if username_check(username) == True:
            return "Bu Kullanıcı Adı Alınmış"

        if password != password2:
            return "Şifre Eşit Değil"


        if len(username) > 10:
            return "Kullanıcı Adı Çok Uzun"

        if len(password) > 16:
            return "Şifre Çok Uzun"
        
        if len(password) < 5:
            return "Şifre Çok Kısa"

        if len(username) < 2:
            return "Kullanıcı Adı Çok Kısa"

        addUp()
        return "ok"

    def login(username,password):
        def real_password(password_hash):
            ph = PasswordHasher()

            try:
                return ph.verify(password_hash, password)
            except:
                return False

        def password_hash():
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute(
                "SELECT password FROM users WHERE username = ?",
                (username,)
            )

            result = cursor.fetchone()
            conn.close()

            if result:
                return result[0]

            return None

        if password_hash() == None:
            return "Kullanıcı Bulunamadı!"

        if real_password(password_hash()) != True:
            return "Şifre Yanlış!"

        return "ok"

class books:

    def new(username,bookname,public):
            try:
                conn = sqlite3.connect(DB)
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT bookname FROM books WHERE creater_username = ?",
                    (username,)
                )

                books = [row[0] for row in cursor.fetchall()]

                if bookname in books:
                    return "Bu İsimi Kullanıyorsunuz Lütfen Farklı Bir İsim Seçiniz"

                cursor.execute(
                    "INSERT INTO books (creater_username, bookname, public) VALUES (?, ?, ?)",
                    (username, bookname, public)
                )

                conn.commit()
                conn.close()                
            except:
                return "Beklenmeyen Bir Hata Oluştu "

            return "ok"


    def bookDatas(username, bookname):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM books
            WHERE creater_username = ? AND bookname = ?
        """, (username, bookname))

        result = cursor.fetchone()

        conn.close()

        if result is not None:
            result = list(result)

            if result[2] is not None:
                result[2] = cipher.decrypt(
                    result[2].encode("utf-8")
                ).decode("utf-8")

            return tuple(result)

        return None

    def bookSave(username, bookname, notes):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        encrypted_notes = cipher.encrypt(notes.encode("utf-8")).decode("utf-8")

        cursor.execute("""
            UPDATE books
            SET note = ?
            WHERE creater_username = ? AND bookname = ?
        """, (encrypted_notes, username, bookname))

        conn.commit()
        conn.close()

        return "ok"

    def bookpublicUpdate(username,bookname,value:int):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE books
            SET public = ?
            WHERE creater_username = ? AND bookname = ?
        """, (value, username, bookname))

        conn.commit()
        conn.close()

        return "ok"

    def yetkiliguncelle(username,bookname,yetkili_adi):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE books
            SET name_with_access = ?
            WHERE creater_username = ? AND bookname = ?
        """, (yetkili_adi, username, bookname))

        conn.commit()
        conn.close()

        return "ok"

    def books_get(username):
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT bookname FROM books WHERE creater_username = ?",
            (username,)
        )

        booknames = [row[0] for row in cursor.fetchall()]

        conn.close()

        return booknames

    def book_sil(username,bookname):
        try:
            conn = sqlite3.connect(DB)
            cursor = conn.cursor()

            cursor.execute(
                "DELETE FROM books WHERE bookname = ? AND creater_username = ?",
                (bookname, username)
            )

            conn.commit()
            conn.close()
        except:
            return "error"

        return "ok"