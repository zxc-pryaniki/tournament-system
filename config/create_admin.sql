INSERT INTO users_customuser (
    password, is_superuser, username, first_name, last_name, 
    email, is_staff, is_active, date_joined, role
) VALUES (
    'pbkdf2_sha256$600000$31S3XU9ZqFjZ2b4y$O+k/t9O1+5k2D9u+W8E/g/V+8=', 
    true, 'admin', '', '', 
    'admin@tournament.com', true, true, NOW(), 'admin'
);
