-- course entity table (studying discipline)
CREATE TABLE IF NOT EXISTS course (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 ) NOT NULL
);

-- department defining faculties, etc
CREATE TABLE IF NOT EXISTS department (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 ) NOT NULL
);

-- building defines auditorium location
CREATE TABLE IF NOT EXISTS building (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 )
);

-- semester that defining studying plans period
CREATE TABLE IF NOT EXISTS semester (
    id serial PRIMARY KEY,
    number SMALLINT NOT NULL,
    semester_year SMALLINT NOT NULL
);

-- students exam; exam's course will be defined at course program table
CREATE TABLE IF NOT EXISTS exam (
    id serial PRIMARY KEY,
    exam_date DATE NOT NULL,
    exam_time TIME NOT NULL,
    content TEXT
);

-- students self-work; self-work's course will be defined at course program table
CREATE TABLE IF NOT EXISTS self_work (
    id serial PRIMARY KEY,
    created_at DATE DEFAULT CURRENT_DATE,
    content TEXT
);

-- studying faculties defined by department
CREATE TABLE IF NOT EXISTS faculty (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 ),
    department_id INTEGER REFERENCES department ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- students studying group
CREATE TABLE IF NOT EXISTS student_group (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 ),
    faculty_id INTEGER REFERENCES faculty ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- student entity
CREATE TABLE IF NOT EXISTS student (
    id serial PRIMARY KEY,
    fullname VARCHAR ( 50 ),
    student_group_id INTEGER REFERENCES student_group ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- teacher entity
CREATE TABLE IF NOT EXISTS teacher (
    id serial PRIMARY KEY,
    fullname VARCHAR ( 50 ),
    department_id INTEGER REFERENCES department ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- student scoring by exams (courses)
CREATE TABLE IF NOT EXISTS student_grade (
    id serial PRIMARY KEY,
    student_id INTEGER REFERENCES student ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    course_id INTEGER REFERENCES course ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    exam_id INTEGER REFERENCES exam ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    grade INTEGER NOT NULL
);

-- auditorium defined by building, defines where will spending schedule classes
CREATE TABLE IF NOT EXISTS auditorium (
    id serial PRIMARY KEY,
    title VARCHAR ( 50 ),
    building_id INTEGER REFERENCES building ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- student classes schedule
CREATE TABLE IF NOT EXISTS schedule (
    id serial PRIMARY KEY,
    course_id INTEGER REFERENCES course ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    student_group_id INTEGER REFERENCES student_group ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    teacher_id INTEGER REFERENCES teacher ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    auditorium_id INTEGER REFERENCES auditorium ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    class_date DATE NOT NULL,
    class_time TIME NOT NULL
);

-- course program defined by studying plan
CREATE TABLE IF NOT EXISTS course_program (
    id serial PRIMARY KEY,
    course_id INTEGER REFERENCES course ( id ) ON UPDATE CASCADE ON DELETE CASCADE
);

-- course program includes exams
CREATE TABLE IF NOT EXISTS course_program_exam (
    course_program_id INTEGER REFERENCES course_program ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    exam_id INTEGER REFERENCES exam ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT course_program_exam_pkey PRIMARY KEY ( course_program_id, exam_id )
);

-- course program includes self-working tasks
CREATE TABLE IF NOT EXISTS course_program_self_work (
    course_program_id INTEGER REFERENCES course_program ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    self_work_id INTEGER REFERENCES self_work ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT course_program_self_work_pkey PRIMARY KEY ( course_program_id, self_work_id )
);

-- studying plan defines which course program will be used at faculty semester
CREATE TABLE IF NOT EXISTS studying_plan (
    faculty_id INTEGER REFERENCES faculty ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    semester_id INTEGER REFERENCES semester ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    course_program_id INTEGER REFERENCES course_program ( id ) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT faculty_semester_course_program_pkey PRIMARY KEY ( faculty_id, semester_id, course_program_id )
);

