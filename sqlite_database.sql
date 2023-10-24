--
-- Файл сгенерирован с помощью SQLiteStudio v3.4.4 в Ср окт 25 01:18:57 2023
--
-- Использованная кодировка текста: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Таблица: ads
DROP TABLE IF EXISTS ads;
CREATE TABLE ads (page_id INTEGER PRIMARY KEY UNIQUE NOT NULL, split INTEGER NOT NULL DEFAULT (0), link1 TEXT, image1_path TEXT, link2 TEXT, image2_path TEXT, enabled INTEGER NOT NULL DEFAULT (1));

-- Таблица: brands
DROP TABLE IF EXISTS brands;
CREATE TABLE brands (id TEXT PRIMARY KEY UNIQUE NOT NULL, name TEXT NOT NULL, links TEXT, access_code TEXT UNIQUE);

-- Таблица: categories
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (id INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL, name TEXT NOT NULL);

-- Таблица: news
DROP TABLE IF EXISTS news;
CREATE TABLE news (id TEXT NOT NULL PRIMARY KEY UNIQUE, tg_message_id INTEGER NOT NULL UNIQUE, body TEXT NOT NULL, posted_on INTEGER NOT NULL);

-- Таблица: products
DROP TABLE IF EXISTS products;
CREATE TABLE products (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, category_id INTEGER NOT NULL REFERENCES categories (id), brand_id TEXT REFERENCES brands (id) NOT NULL, name TEXT NOT NULL, description TEXT NOT NULL, image_url TEXT, clicks INTEGER NOT NULL DEFAULT (0));

-- Таблица: replies
DROP TABLE IF EXISTS replies;
CREATE TABLE replies (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, review_id INTEGER REFERENCES reviews (id) NOT NULL, reply TEXT NOT NULL, posted_on INTEGER NOT NULL);

-- Таблица: reviews
DROP TABLE IF EXISTS reviews;
CREATE TABLE reviews (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, product_id INTEGER REFERENCES products (id) NOT NULL, review TEXT NOT NULL, rating INTEGER NOT NULL, posted_on INTEGER NOT NULL);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
