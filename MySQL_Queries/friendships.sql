--Return all users who are friends with Kermit, make sure their names are displayed in results.
SELECT first_name, last_name FROM friendships LEFT JOIN users ON friendships.user_id = users.id where friend_id = 4
--Return the count of all friendships
SELECT COUNT(user_id) as number_of_friends FROM friendships GROUP BY friendships.user_id
--Find out who has the most friends and return the count of their friends.
SELECT user_id, COUNT(user_id) as number_of_friends FROM friendships GROUP BY friendships.user_id order by number_of_friends DESC LIMIT 1
--Create a new user and make them friends with Eli Byers, Kermit The Frog, and Marky Mark
INSERT INTO users (first_name, last_name, created_at, updated_at) VALUES ( 'Tom', 'Chan', NOW(), NOW());
INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES (6, 2, NOW(), NOW())
INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES (6, 4, NOW(), NOW())
INSERT INTO friendships (user_id, friend_id, created_at, updated_at) VALUES (6, 5, NOW(), NOW())
--Return the friends of Eli in alphabetical order
select first_name, last_name from friendships LEFT JOIN users ON friendships.user_id = users.id where friend_id = 2 ORDER BY last_name ASC
--Remove Marky Marky from Eli’s friends.
DELETE FROM friendships WHERE user_id = 2 AND friend_id = 5
--Return all friendships, displaying just the first and last name of both friends
SELECT users.first_name as user_fn, users.last_name as user_ln, user2.first_name as friend_fn, user2.last_name as friend_ln FROM users 
JOIN friendships ON users.id = friendships.friend_id 
JOIN users as user2 ON user2.id = friendships.user_id