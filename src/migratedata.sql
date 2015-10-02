INSERT INTO clubmembers_member
(id, acad_concentration,acad_grad_qtr,acad_major,acad_minor,email,name_first,name_last,phone,photo,photoheight,photowidth,pin_hash,shirt_size,texting_ok,date_created,is_active,is_staff,is_superuser,last_login,password,username,coyote_id,email_pending)
SELECT
old.auth_user.id as id,
acad_concentration,acad_grad_qtr,acad_major,acad_minor,old.clubmembers_member.email,name_first,name_last,phone,photo,photoheight,photowidth,pin_hash,shirt_size,texting_ok,date_joined as "date_created",is_active,is_staff,is_superuser,last_login,password,username,
'' as coyote_id,'' as email_pending
FROM old.clubmembers_member JOIN old.auth_user ON user_id==id;

INSERT INTO events_event
(id, title, start, end, allDay)
SELECT
id, title, start, end, allDay
FROM old.events_event;

INSERT INTO clubdata_club
(id, name_short, name_long)
SELECT
id, name_short, name_long
FROM old.clubmembers_club;

INSERT INTO contentblocks_block
(id, uniquetitle, description, datatype, blob, published, created_date, edited_date, club_id, created_by_user_id, edited_by_user_id)
SELECT
id, uniquetitle, description, datatype, blob, published, created_date, edited_date, club_id, created_by_user_id, edited_by_user_id
FROM old.contentblocks_block;
