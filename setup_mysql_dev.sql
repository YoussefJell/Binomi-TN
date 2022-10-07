-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS binomi_dev_db;
CREATE USER IF NOT EXISTS 'binomi_dev'@'localhost' IDENTIFIED BY 'binomi_dev_pwd';
GRANT ALL PRIVILEGES ON `binomi_dev_db`.* TO 'binomi_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'binomi_dev'@'localhost';
FLUSH PRIVILEGES;
