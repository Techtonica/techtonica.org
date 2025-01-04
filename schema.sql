-- Users table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    is_admin BOOLEAN DEFAULT 0,
    is_participant BOOLEAN DEFAULT 0,
    is_staff BOOLEAN DEFAULT 0
);

-- Applications table
CREATE TABLE application (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL,
    program VARCHAR(50) NOT NULL,
    statement TEXT NOT NULL,
    status VARCHAR(20) DEFAULT 'Submitted',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Courses table
CREATE TABLE course (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    staff_id INTEGER NOT NULL,
    FOREIGN KEY (staff_id) REFERENCES user (id)
);

-- Assignments table
CREATE TABLE assignment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    due_date DATETIME NOT NULL,
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES course (id)
);

-- Submissions table
CREATE TABLE submission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    submitted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    grade FLOAT,
    assignment_id INTEGER NOT NULL,
    participant_id INTEGER NOT NULL,
    FOREIGN KEY (assignment_id) REFERENCES assignment (id),
    FOREIGN KEY (participant_id) REFERENCES user (id)
);

-- Messages table
CREATE TABLE message (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    sender VARCHAR(50) NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id)
);

-- Enrollments table (for many-to-many relationship between users and courses)
CREATE TABLE enrollments (
    user_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    PRIMARY KEY (user_id, course_id),
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (course_id) REFERENCES course (id)
);