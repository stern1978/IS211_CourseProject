import sqlite3

with sqlite3.connect("books.db") as connection:
    c = connection.cursor()
    try:
        c.execute("""DROP TABLE books""")
        c.execute("""DROP TABLE users""")
    except:
        pass


    c.execute("""CREATE TABLE books(
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    pages TEXT NOT NULL,
    rating TEXT NOT NULL,
    thumbnail TEXT NOT NULL,
    link TEXT NOT NULL,
    description TEXT NOT NULL)""")


    c.execute("""CREATE TABLE users(
    USERNAME TEXT NOT NULL,
    PASSWORD TEXT NOT NULL)""")


    #c.execute('INSERT INTO books (title, author, pages, rating) values ("Accessory to War: The Unspoken Alliance Between Astrophysics and the Military", "Neil deGrasse Tyson", "448", "5.0")')
    c.execute('INSERT INTO users (USERNAME, PASSWORD) values ("admin", "password")')
