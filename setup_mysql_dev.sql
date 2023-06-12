--- CREATING MYSQL USER AND GRANT THE PRIVILEGE TO HIM ---

CREATE DATABASE IF NOT EXISTS hbnb_dev_db;
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';
GRANT SELECT ON perforamance_schema.* TO 'hbnb_dev'@'localhost';
