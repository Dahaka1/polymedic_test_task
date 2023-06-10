-- QUERY #1
SELECT s.id, s.fullname FROM student AS s JOIN student_group AS s_g ON s.student_group_id=s_g.id JOIN
faculty AS f ON s_g.faculty_id=f.id JOIN studying_plan AS s_p ON f.id=s_p.faculty_id JOIN
course_program AS c_p ON s_p.course_program_id=c_p.id JOIN course AS c ON c_p.course_id=c.id WHERE
c.title='Математика';

-- QUERY #2
-- score might be chosen only by type 'assessment'
-- exam_id must be defined early by course title
UPDATE student_exam SET score='3' WHERE student_id=10 AND exam_id=20;


-- QUERY #3
SELECT t.id, t.fullname FROM teacher AS t JOIN schedule AS s ON t.id=s.teacher_id JOIN
auditorium AS a ON s.auditorium_id=a.id JOIN building AS b ON a.building_id=b.id WHERE
b.id=3;

-- QUERY #4
-- я не разобрался до конца, как оно работает :(
-- но запрос должен выглядеть похожим образом
WITH old_self_work AS
    (SELECT self_work.id FROM self_work WHERE DATEDIFF(self_work.created_at, CURRENT_DATE) > 365 LIMIT 1)
DELETE FROM self_work WHERE id = old_self_work;


-- QUERY #5
INSERT INTO semester (number, semester_year) VALUES (2, date_part('year', now()));