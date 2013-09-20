INSERT INTO user (id, username, netid, university_id, status, created_at, modified_at) VALUES (1, 'abc123', 'abc123', 'N123456', 'enabled', '2013-09-06 07:48:00', '2013-09-06 07:48:00');
INSERT INTO user (id, username, netid, university_id, status, created_at, modified_at) VALUES (2, 'def456', NULL, NULL, 'enabled', '2013-09-06 07:48:00', '2013-09-06 07:55:00');
INSERT INTO user (id, username, netid, university_id, status, created_at, modified_at) VALUES (3, 'gh7', 'gh7', 'N78901', 'enabled', '2013-09-06 07:49:00', '2013-09-06 07:49:00');
INSERT INTO user (id, username, netid, university_id, status, created_at, modified_at) VALUES (4, 'ijk89', 'ijk89', 'N23', 'enabled', '2013-09-06 07:51:00', '2013-09-06 07:51:00');

INSERT INTO link (id, url, user, title, annotation, created_at, modified_at) VALUES (1, 'http://eff.org', 2, 'Electronic Frontier Foundation', NULL, '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO link (id, url, user, title, annotation, created_at, modified_at) VALUES (2, 'http://dronestre.am', 2, 'Realtime Drone Strike Data', 'Thesis of Josh Begley', '2013-09-06 11:51:00', '2013-09-06 11:51:00');
INSERT INTO link (id, url, user, title, annotation, created_at, modified_at) VALUES (3, 'http://eff.org', 3, 'EFF', NULL, '2013-09-06 08:55:00', '2013-09-06 08:55:00');
INSERT INTO link (id, url, user, title, annotation, created_at, modified_at) VALUES (4, 'http://python.org', 1, 'Python', 'Python Programming Language', '2013-09-06 16:18:00', '2013-09-06 16:18:00');

INSERT INTO tag (id, tag, status, created_at, modified_at) VALUES (1, 'privacy', 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO tag (id, tag, status, created_at, modified_at) VALUES (2, 'programming', 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO tag (id, tag, status, created_at, modified_at) VALUES (3, 'drone', 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO tag (id, tag, status, created_at, modified_at) VALUES (4, 'law', 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');

INSERT INTO link_tag (link_id, tag_id) VALUES (1, 1);
INSERT INTO link_tag (link_id, tag_id) VALUES (1, 4);
INSERT INTO link_tag (link_id, tag_id) VALUES (2, 3);
INSERT INTO link_tag (link_id, tag_id) VALUES (3, 4);
INSERT INTO link_tag (link_id, tag_id) VALUES (4, 2);

INSERT INTO idcard (id, serial, user, status, created_at, modified_at) VALUES (1, '74856', 1, 'enabled', '2013-09-06 07:51:00', '2013-09-06 07:51:00');
INSERT INTO idcard (id, serial, user, status, created_at, modified_at) VALUES (2, '00680', 4, 'enabled', '2013-09-06 07:51:00', '2013-09-06 07:51:00');
INSERT INTO idcard (id, serial, user, status, created_at, modified_at) VALUES (3, '1378', 2, 'enabled', '2013-09-06 07:51:00', '2013-09-06 07:51:00');

INSERT INTO apikey (id, apikey, user, status, created_at, modified_at) VALUES (1, '7c53e1ed-922e-4595-94cb-9eb76b1e6e75', 1, 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO apikey (id, apikey, user, status, created_at, modified_at) VALUES (2, 'c0dc70db-7068-43c1-b144-464cd8902f36', 2, 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO apikey (id, apikey, user, status, created_at, modified_at) VALUES (3, 'b7976898-8f8b-47bd-8dec-762e30b780ce', 3, 'enabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');
INSERT INTO apikey (id, apikey, user, status, created_at, modified_at) VALUES (4, 'cae9a4a2-7dcc-42a9-9773-9b6968750495', 4, 'disabled', '2013-09-06 08:51:00', '2013-09-06 09:51:00');




