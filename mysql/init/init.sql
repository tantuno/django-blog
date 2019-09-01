CREATE DATABASE vakoms_test_blog;
CREATE USER 'blog_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON vakoms_test_blog.* TO 'blog_user'@'localhost';