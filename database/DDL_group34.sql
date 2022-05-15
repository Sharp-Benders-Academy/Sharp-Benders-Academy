-- CS 340 - Databases
-- Group 34 - Sharp Squad: Elizabeth Thorne and Faihaan Arif
-- Project: Sharp Benders Academy

-- Foreign Key check (per assignment)
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cs340_thorneel`
--

-- --------------------------------------------------------

--
-- Table structure for table `Advisors`
--

CREATE OR REPLACE TABLE `Advisors` (
  `advisor_id` int(9) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `school_email` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address_line1` varchar(50) DEFAULT NULL,
  `address_line2` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `postal_code` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Advisors`
--

INSERT INTO `Advisors` (`advisor_id`, `first_name`, `last_name`, `school_email`, `phone_number`, `address_line1`, `address_line2`, `city`, `state`, `postal_code`) VALUES
(1, 'Iroh', 'Brooks', 'ibrooks@sharpbenders.edu', '193-483-2029', '2837 Drury Ln', NULL, 'Astoria', 'Oregon', '97103'),
(2, 'Toph', 'River', 'triver@sharpbenders.edu', '201-472-3849', '587 Douglas Dr.', 'Apt 203', 'Lake Oswego', 'Oregon', '97034'),
(3, 'Hama', 'Thomas', 'hthomas@sharpbenders.edu', '103-403-2748', '9871 Marion Ct', NULL, 'Pendleton', 'Oregon', '97801');

-- --------------------------------------------------------

--
-- Table structure for table `Courses`
--

CREATE OR REPLACE TABLE `Courses` (
  `course_id` int(4) NOT NULL,
  `title` varchar(50) NOT NULL,
  `start_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `num_of_credits` tinyint(4) NOT NULL,
  `is_remote` tinyint(1) NOT NULL DEFAULT 0,
  `capacity` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Courses`
--

INSERT INTO `Courses` (`course_id`, `title`, `start_time`, `end_time`, `num_of_credits`, `is_remote`, `capacity`) VALUES
(3101, 'Introduction to Bending', '08:00:00', '10:00:00', 5, 0, 100),
(4205, 'Bending Fundamentals', '15:00:00', '16:00:00', 3, 1, 150),
(5401, 'Manipulating Water - Waterbending Techniques', '12:00:00', '14:00:00', 5, 0, 75);

-- --------------------------------------------------------

--
-- Table structure for table `Courses_Instructors`
--

CREATE OR REPLACE TABLE `Courses_Instructors` (
  `course_instructor_id` int(5) NOT NULL,
  `instructor_id` int(9),
  `course_id` int(4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Courses_Instructors`
--

INSERT INTO `Courses_Instructors` (`instructor_id`, `course_id`, `course_instructor_id`) VALUES
(1, 3101, 2),
(1, 5401, 1),
(2, 3101, 4),
(2, 4205, 3),
(3, 3101, 5);

-- --------------------------------------------------------

--
-- Table structure for table `Grades`
--

CREATE OR REPLACE TABLE `Grades` (
  `grade_id` int(5) NOT NULL,
  `passed_course` tinyint(1) NOT NULL DEFAULT 1,
  `student_id` int(9),
  `course_id` int(4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Grades`
--

INSERT INTO `Grades` (`grade_id`, `passed_course`, `student_id`, `course_id`) VALUES
(1, 1, 1, 5401),
(2, 1, 3, 3101),
(3, 0, 2, 3101);

-- --------------------------------------------------------

--
-- Table structure for table `Instructors`
--

CREATE OR REPLACE TABLE `Instructors` (
  `instructor_id` int(9) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `school_email` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address_line1` varchar(50) DEFAULT NULL,
  `address_line2` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `postal_code` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Instructors`
--

INSERT INTO `Instructors` (`instructor_id`, `first_name`, `last_name`, `school_email`, `phone_number`, `address_line1`, `address_line2`, `city`, `state`, `postal_code`) VALUES
(1, 'Katara', 'Williams', 'kwilliams@sharpbenders.edu', '941-764-8916', '641 Otterville Ln', NULL, 'Bend', 'Oregon', '97701'),
(2, 'Sokka', 'Brown', 'sbrown@sharpbenders.edu', '461-764-4512', '2831 Fur Ct', 'Apt 312', 'Astoria', 'Oregon', '97103'),
(3, 'Azula', 'Stone', 'astone@sharpbenders.edu', '741-745-6421', '463 Rainy Blvd', NULL, 'Eugene', 'Oregon', '97401');

-- --------------------------------------------------------

--
-- Table structure for table `Majors`
--

CREATE OR REPLACE TABLE `Majors` (
  `major_id` varchar(4) NOT NULL,
  `title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Majors`
--

INSERT INTO `Majors` (`major_id`, `title`) VALUES
('ABND', 'Airbending'),
('EBND', 'Earthbending'),
('FBND', 'Firebending'),
('WBND', 'Waterbending');

-- --------------------------------------------------------

--
-- Table structure for table `Registrations`
--

CREATE OR REPLACE TABLE `Registrations` (
  `reg_id` int(5) NOT NULL,
  `student_id` int(9),
  `course_id` int(4),
  `year` year(4) NOT NULL,
  `semester_id` varchar(4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Registrations`
--

INSERT INTO `Registrations` (`student_id`, `course_id`, `reg_id`, `year`, `semester_id`) VALUES
(1, 5401, 1, 2021, 'FALL'),
(3, 3101, 2, 2021, 'FALL'),
(2, 3101, 3, 2021, 'SUMR'),
(1, 4205, 4, 2022, 'SUMR');

-- --------------------------------------------------------

--
-- Table structure for table `Semesters`
--

CREATE OR REPLACE TABLE `Semesters` (
  `semester_id` varchar(4) NOT NULL,
  `title` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Semesters`
--

INSERT INTO `Semesters` (`semester_id`, `title`) VALUES
('FALL', 'Fall'),
('SPNG', 'Spring'),
('SUMR', 'Summer');

-- --------------------------------------------------------

--
-- Table structure for table `Students`
--

CREATE OR REPLACE TABLE `Students` (
  `student_id` int(9) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `school_email` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address_line1` varchar(50) DEFAULT NULL,
  `address_line2` varchar(50) DEFAULT NULL,
  `city` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `postal_code` varchar(50) DEFAULT NULL,
  `advisor_id` int(9),
  `major_id` varchar(4)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

--
-- Dumping data for table `Students`
--

INSERT INTO `Students` (`student_id`, `first_name`, `last_name`, `school_email`, `phone_number`, `address_line1`, `address_line2`, `city`, `state`, `postal_code`, `advisor_id`, `major_id`) VALUES
(1, 'Korra', 'Smith', 'ksmith@sharpbenders.edu', '397-241-7985', '231 Tranquil Ave', NULL, 'Eugene', 'Oregon', '97401', 2, 'WBND'),
(2, 'Aang', 'Cook', 'acook@sharpbenders.edu', '341-874-8946', '432 Waterfall Dr.', 'Apt 212', 'Portland', 'Oregon', '97035', 3, 'ABND'),
(3, 'Roku', 'Hunter', 'rhunter@sharpbenders.edu', '746-842-7946', '129 Peaceful Ln', NULL, 'Bend', 'Oregon', '97701', 1, 'FBND');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Advisors`
--
ALTER TABLE `Advisors`
  ADD PRIMARY KEY (`advisor_id`);

--
-- Indexes for table `Courses`
--
ALTER TABLE `Courses`
  ADD PRIMARY KEY (`course_id`),
  ADD UNIQUE KEY `course_id_UNIQUE` (`course_id`);

--
-- Indexes for table `Courses_Instructors`
--
ALTER TABLE `Courses_Instructors`
  ADD PRIMARY KEY (`course_instructor_id`),
  ADD KEY `fk_Instructors_has_Courses_Courses1_idx` (`course_id`),
  ADD KEY `fk_Instructors_has_Courses_Instructors1_idx` (`instructor_id`);

--
-- Indexes for table `Grades`
--
ALTER TABLE `Grades`
  ADD PRIMARY KEY (`grade_id`),
  ADD KEY `fk_Grades_Students1_idx` (`student_id`),
  ADD KEY `fk_Grades_Courses1_idx` (`course_id`);

--
-- Indexes for table `Instructors`
--
ALTER TABLE `Instructors`
  ADD PRIMARY KEY (`instructor_id`);

--
-- Indexes for table `Majors`
--
ALTER TABLE `Majors`
  ADD PRIMARY KEY (`major_id`),
  ADD UNIQUE KEY `major_id_UNIQUE` (`major_id`);

--
-- Indexes for table `Registrations`
--
ALTER TABLE `Registrations`
  ADD PRIMARY KEY (`reg_id`),
  ADD KEY `fk_Students_has_Courses_Courses1_idx` (`course_id`),
  ADD KEY `fk_Students_has_Courses_Students1_idx` (`student_id`),
  ADD KEY `fk_Registrations_Semesters1_idx` (`semester_id`);

--
-- Indexes for table `Semesters`
--
ALTER TABLE `Semesters`
  ADD PRIMARY KEY (`semester_id`),
  ADD UNIQUE KEY `semester_id_UNIQUE` (`semester_id`);

--
-- Indexes for table `Students`
--
ALTER TABLE `Students`
  ADD PRIMARY KEY (`student_id`),
  ADD KEY `fk_Students_Advisors_idx` (`advisor_id`),
  ADD KEY `fk_Students_Majors1_idx` (`major_id`);

--
-- AUTO_INCREMENT for dumped tables
--
-- AUTO_INCREMENT for table `Advisors`
--
ALTER TABLE `Advisors`
  MODIFY `advisor_id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Courses_Instructors`
--
ALTER TABLE `Courses_Instructors`
  MODIFY `course_instructor_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Grades`
--
ALTER TABLE `Grades`
  MODIFY `grade_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `Instructors`
--
ALTER TABLE `Instructors`
  MODIFY `instructor_id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `Registrations`
--
ALTER TABLE `Registrations`
  MODIFY `reg_id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `Students`
--
ALTER TABLE `Students`
  MODIFY `student_id` int(9) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Courses_Instructors`
--
ALTER TABLE `Courses_Instructors`
  ADD CONSTRAINT `fk_Instructors_has_Courses_Courses1` 
  FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) 
  ON DELETE CASCADE,
  ADD CONSTRAINT `fk_Instructors_has_Courses_Instructors1` 
  FOREIGN KEY (`instructor_id`) REFERENCES `Instructors` (`instructor_id`) 
  ON DELETE CASCADE;

--
-- Constraints for table `Grades`
--
ALTER TABLE `Grades`
  ADD CONSTRAINT `fk_Grades_Courses1` 
  FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) 
  ON DELETE CASCADE,
  ADD CONSTRAINT `fk_Grades_Students1` 
  FOREIGN KEY (`student_id`) REFERENCES `Students` (`student_id`) 
  ON DELETE CASCADE;

--
-- Constraints for table `Registrations`
--
ALTER TABLE `Registrations`
  ADD CONSTRAINT `fk_Registrations_Semesters1` 
  FOREIGN KEY (`semester_id`) REFERENCES `Semesters` (`semester_id`) 
  ON DELETE SET NULL,
  ADD CONSTRAINT `fk_Students_has_Courses_Courses1` 
  FOREIGN KEY (`course_id`) REFERENCES `Courses` (`course_id`) 
  ON DELETE CASCADE,
  ADD CONSTRAINT `fk_Students_has_Courses_Students1` 
  FOREIGN KEY (`student_id`) REFERENCES `Students` (`student_id`) 
  ON DELETE CASCADE;

--
-- Constraints for table `Students`
--
ALTER TABLE `Students`
  ADD CONSTRAINT `fk_Students_Advisors` 
  FOREIGN KEY (`advisor_id`) REFERENCES `Advisors` (`advisor_id`) 
  ON DELETE SET NULL,
  ADD CONSTRAINT `fk_Students_Majors1` 
  FOREIGN KEY (`major_id`) REFERENCES `Majors` (`major_id`) 
  ON DELETE SET NULL;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- As Per assignment
SET FOREIGN_KEY_CHECKS=1;
COMMIT;