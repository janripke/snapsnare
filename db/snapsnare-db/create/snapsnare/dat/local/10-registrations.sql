insert into registrations(uuid, username, password, first_name, last_name, state, rle_id) values (uuid_generate_v4(), 'admin@computersnaar.nl', 'e2668187c2a33e838a7b53c5b8c8eb7d90685b26d184144a40ae07546ce1c045','Stichting', 'Computersnaar', 'approved', get_role_id('admin'));
insert into registrations(uuid, username, password, first_name, last_name, state, rle_id) values (uuid_generate_v4(), 'peter.kusters@yahoo.com', 'a8308439108bcc50a9ca29cecb05ab7b2d43d00412c66d328c1eeaa8a5435572','Peter', 'Kusters', 'approved', get_role_id('admin'));
insert into registrations(uuid, username, password, first_name, last_name, state, rle_id) values (uuid_generate_v4(), 'janripke@gmail.com', '2a5c5f2623024ce3de6fe7dc8f5e13ca55b7aadc13174254b40af574e37018c1','Jan', 'Ripke', 'approved', get_role_id('user'));