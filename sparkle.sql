-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Aug 28, 2022 at 04:32 PM
-- Server version: 10.4.20-MariaDB
-- PHP Version: 7.4.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sparkle`
--

-- --------------------------------------------------------

--
-- Table structure for table `adhd_result`
--

CREATE TABLE `adhd_result` (
  `p_email` varchar(255) NOT NULL,
  `s_name` varchar(255) NOT NULL,
  `rpi` varchar(255) NOT NULL,
  `prof` varchar(255) NOT NULL,
  `implications` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adhd_result`
--

INSERT INTO `adhd_result` (`p_email`, `s_name`, `rpi`, `prof`, `implications`) VALUES
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult'),
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult');

-- --------------------------------------------------------

--
-- Table structure for table `adhd_test`
--

CREATE TABLE `adhd_test` (
  `p_email` varchar(40) NOT NULL,
  `q1` varchar(20) NOT NULL,
  `q2` varchar(20) NOT NULL,
  `q3` varchar(20) NOT NULL,
  `q4` varchar(50) NOT NULL,
  `total` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adhd_test`
--

INSERT INTO `adhd_test` (`p_email`, `q1`, `q2`, `q3`, `q4`, `total`) VALUES
('varadjs22@gmail.com', 'bread', 'no', 'monkey', 'xyz', '3');

-- --------------------------------------------------------

--
-- Table structure for table `adhd_time`
--

CREATE TABLE `adhd_time` (
  `p_email` varchar(255) NOT NULL,
  `att_time` varchar(255) NOT NULL,
  `dist_time` varchar(255) NOT NULL,
  `total_time` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `adhd_time`
--

INSERT INTO `adhd_time` (`p_email`, `att_time`, `dist_time`, `total_time`) VALUES
('varadjs22@gmail.com', '22.7646304130553', '27.40000000000012', '50.16463041305542');

-- --------------------------------------------------------

--
-- Table structure for table `blending_words`
--

CREATE TABLE `blending_words` (
  `sr_no` varchar(5) NOT NULL,
  `word` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `blending_words`
--

INSERT INTO `blending_words` (`sr_no`, `word`) VALUES
('1', 'But'),
('2', 'Bad'),
('3', 'Cheese'),
('4', 'Nature'),
('5', 'Dog'),
('6', 'Ring'),
('7', 'Pass'),
('8', 'See'),
('9', 'Square'),
('10', 'Away'),
('11', 'Pain'),
('12', 'Poem'),
('13', 'Out'),
('14', 'Gum'),
('15', 'Mouth'),
('16', 'Loud'),
('17', 'Food'),
('18', 'Visit'),
('19', 'Have'),
('20', 'Far');

-- --------------------------------------------------------

--
-- Table structure for table `cal_result`
--

CREATE TABLE `cal_result` (
  `p_email` varchar(255) NOT NULL,
  `s_name` varchar(255) NOT NULL,
  `rpi` varchar(255) NOT NULL,
  `prof` varchar(255) NOT NULL,
  `implications` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cal_result`
--

INSERT INTO `cal_result` (`p_email`, `s_name`, `rpi`, `prof`, `implications`) VALUES
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult'),
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult'),
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult'),
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult'),
('varadjs22@gmail.com', 'Isha', '24/90 to 67/90', 'Limited', 'Very Difficult');

-- --------------------------------------------------------

--
-- Table structure for table `cal_test`
--

CREATE TABLE `cal_test` (
  `p_email` varchar(255) NOT NULL,
  `q1` varchar(20) NOT NULL,
  `q2` varchar(20) NOT NULL,
  `q3` varchar(20) NOT NULL,
  `q4` varchar(20) NOT NULL,
  `q5` varchar(20) NOT NULL,
  `q6` varchar(20) NOT NULL,
  `q7` varchar(20) NOT NULL,
  `q8` varchar(20) NOT NULL,
  `q9` varchar(20) NOT NULL,
  `q10` varchar(20) NOT NULL,
  `q11` varchar(20) NOT NULL,
  `q12` varchar(20) NOT NULL,
  `q13` varchar(20) NOT NULL,
  `q14` varchar(20) NOT NULL,
  `q15` varchar(255) NOT NULL,
  `q16` varchar(255) NOT NULL,
  `q17` varchar(255) NOT NULL,
  `q18` varchar(255) NOT NULL,
  `total` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cal_test`
--

INSERT INTO `cal_test` (`p_email`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `q11`, `q12`, `q13`, `q14`, `q15`, `q16`, `q17`, `q18`, `total`) VALUES
('varadjs22@gmail.com', '0', '0', '0', '0', '4', '5', '3', '7', '8', '9', '6', '5', '4', '3', '5', '1', '1', '1', 1);

-- --------------------------------------------------------

--
-- Table structure for table `cal_test2`
--

CREATE TABLE `cal_test2` (
  `p_email` varchar(255) NOT NULL,
  `q1` varchar(255) NOT NULL,
  `q2` varchar(255) NOT NULL,
  `q3` varchar(255) NOT NULL,
  `q4` varchar(255) NOT NULL,
  `q5` varchar(255) NOT NULL,
  `q6` varchar(255) NOT NULL,
  `q7` varchar(255) NOT NULL,
  `q8` varchar(255) NOT NULL,
  `q9` varchar(255) NOT NULL,
  `q10` varchar(255) NOT NULL,
  `q11` varchar(255) NOT NULL,
  `q12` varchar(255) NOT NULL,
  `q13` varchar(255) NOT NULL,
  `q14` varchar(255) NOT NULL,
  `q15` varchar(255) NOT NULL,
  `q16` varchar(255) NOT NULL,
  `q17` varchar(255) NOT NULL,
  `q18` varchar(255) NOT NULL,
  `q19` varchar(255) NOT NULL,
  `q20` varchar(255) NOT NULL,
  `total` varchar(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `cal_test2`
--

INSERT INTO `cal_test2` (`p_email`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `q11`, `q12`, `q13`, `q14`, `q15`, `q16`, `q17`, `q18`, `q19`, `q20`, `total`) VALUES
('varadjs22@gmail.com', '0', '1', '-', '1', '2', '1', '3', '0', '2', '4', '7', '8', '9', '9', '9', '5', '5', '5', '5', '5', '2');

-- --------------------------------------------------------

--
-- Table structure for table `dolce_phrases`
--

CREATE TABLE `dolce_phrases` (
  `sr_no` int(5) NOT NULL,
  `phrase` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dolce_phrases`
--

INSERT INTO `dolce_phrases` (`sr_no`, `phrase`) VALUES
(1, 'A big horse'),
(2, 'A new hat'),
(3, 'About it'),
(4, 'I may go'),
(5, 'I will come'),
(6, 'In the box'),
(7, 'My brother'),
(8, 'When you come'),
(9, 'You will like'),
(10, 'The small boat');

-- --------------------------------------------------------

--
-- Table structure for table `dys_identification`
--

CREATE TABLE `dys_identification` (
  `sr. no` int(255) NOT NULL,
  `para` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dys_identification`
--

INSERT INTO `dys_identification` (`sr. no`, `para`) VALUES
(1, 'My house is red - a little house;\r\nA happy child am I.\r\nI laugh and play the whole day long,\r\nI hardly ever cry.\r\n\r\nI have a tree, a green, green tree,\r\nTo shade me from the sun;\r\nAnd under it I often sit,\r\nWhen all my play is done.'),
(2, 'If I were an apple\r\nAnd grew on a tree,\r\nI think I’d drop down\r\nOn a nice boy like me.\r\nI wouldn’t stay there\r\nGiving nobody joy,\r\nI’d fall down at once\r\nAnd say, “Eat me, my boy!”');

-- --------------------------------------------------------

--
-- Table structure for table `dys_parent_test`
--

CREATE TABLE `dys_parent_test` (
  `p_email` varchar(255) NOT NULL,
  `q1` int(255) NOT NULL,
  `q2` int(255) NOT NULL,
  `q3` int(255) NOT NULL,
  `q4` int(255) NOT NULL,
  `q5` int(255) NOT NULL,
  `q6` int(255) NOT NULL,
  `q7` int(255) NOT NULL,
  `q8` int(255) NOT NULL,
  `q9` int(255) NOT NULL,
  `q10` int(255) NOT NULL,
  `q11` int(255) NOT NULL,
  `q12` int(255) NOT NULL,
  `q13` int(255) NOT NULL,
  `q14` int(255) NOT NULL,
  `q15` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `dys_parent_test`
--

INSERT INTO `dys_parent_test` (`p_email`, `q1`, `q2`, `q3`, `q4`, `q5`, `q6`, `q7`, `q8`, `q9`, `q10`, `q11`, `q12`, `q13`, `q14`, `q15`) VALUES
('varadjs22@gmail.com', 2, 1, 2, 0, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `d_creds`
--

CREATE TABLE `d_creds` (
  `d_name` varchar(255) NOT NULL,
  `designation` varchar(255) NOT NULL,
  `d_mail` varchar(255) NOT NULL,
  `d_phone` int(255) NOT NULL,
  `d_pass` varchar(255) NOT NULL,
  `d_school` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `d_creds`
--

INSERT INTO `d_creds` (`d_name`, `designation`, `d_mail`, `d_phone`, `d_pass`, `d_school`) VALUES
('jenil', 'Psychologist', 'jenil.kanani@somaiya.edu', 1827645637, 'jenil', 'ryan international');

-- --------------------------------------------------------

--
-- Table structure for table `feedback_adhd`
--

CREATE TABLE `feedback_adhd` (
  `p_email` varchar(20) NOT NULL,
  `q1` varchar(20) NOT NULL,
  `q2` varchar(20) NOT NULL,
  `q3` varchar(20) NOT NULL,
  `q4` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `feedback_dyscalculia`
--

CREATE TABLE `feedback_dyscalculia` (
  `p_email` varchar(40) NOT NULL,
  `q1` varchar(20) NOT NULL,
  `q2` varchar(20) NOT NULL,
  `q3` varchar(20) NOT NULL,
  `q4` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback_dyscalculia`
--

INSERT INTO `feedback_dyscalculia` (`p_email`, `q1`, `q2`, `q3`, `q4`) VALUES
('varadjs22@gmail.com', 'Sometimes', 'Never', 'Never', '');

-- --------------------------------------------------------

--
-- Table structure for table `feedback_dysgraphia`
--

CREATE TABLE `feedback_dysgraphia` (
  `p_email` text NOT NULL,
  `q1` text NOT NULL,
  `q2` text NOT NULL,
  `q3` text NOT NULL,
  `q4` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback_dysgraphia`
--

INSERT INTO `feedback_dysgraphia` (`p_email`, `q1`, `q2`, `q3`, `q4`) VALUES
('varadjs22@gmail.com', 'Most of the time', 'Most of the time', 'Never', '');

-- --------------------------------------------------------

--
-- Table structure for table `feedback_dyslexia`
--

CREATE TABLE `feedback_dyslexia` (
  `p_email` text NOT NULL,
  `q1` text NOT NULL,
  `q2` text NOT NULL,
  `q3` text NOT NULL,
  `q4` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `feedback_dyslexia`
--

INSERT INTO `feedback_dyslexia` (`p_email`, `q1`, `q2`, `q3`, `q4`) VALUES
('varadjs22@gmail.com', 'Most of the time', 'Never', 'Rarely', '');

-- --------------------------------------------------------

--
-- Table structure for table `lex_result`
--

CREATE TABLE `lex_result` (
  `p_email` varchar(255) NOT NULL,
  `s_name` varchar(255) NOT NULL,
  `rpi` varchar(255) NOT NULL,
  `prof` varchar(255) NOT NULL,
  `implications` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_result`
--

INSERT INTO `lex_result` (`p_email`, `s_name`, `rpi`, `prof`, `implications`) VALUES
('varadjs22@gmail.com', 'Isha', '98/90 to 100/90', 'Advanced', 'Very Easy');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test1`
--

CREATE TABLE `lex_test1` (
  `p_email` varchar(20) NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` varchar(255) NOT NULL,
  `accuracy` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test1`
--

INSERT INTO `lex_test1` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'my house is red a little house a happy child am i i laugh and play the whole day long i hardly ever cry i have a tree a green green tree to shade me from the sun and under it i often sit when all my play is done', 'my house is red a little house a Happy Child am I I love and', 'my house is red a little house a happy child am i i and', 'my is a a i i i laugh and play play the the whole day long hardly ever cry have tree tree green green to shade me from sun under it often sit when all done', 'love', '0.0603448275862069', '0.9333333333333333');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test2`
--

CREATE TABLE `lex_test2` (
  `p_email` varchar(20) NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` varchar(255) NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test2`
--

INSERT INTO `lex_test2` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'if i were an apple and grew on a tree i think i’d drop down on a nice boy like me i wouldn’t stay there giving nobody joy i’d fall down at once and say “eat me my boy”', 'if I were an apple and grew on a tree I think I\'d drop down on a nice boy like me', 'if i were an apple and grew on a tree i think drop down on a nice boy like me', 'i and i’d i’d down me wouldn’t stay there giving nobody joy fall at once say “eat my boy”', 'i\'d', '0.1111111111111111', '0.9523809523809523');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_blendwords`
--

CREATE TABLE `lex_test_blendwords` (
  `p_email` text NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test_blendwords`
--

INSERT INTO `lex_test_blendwords` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'but bad cheese nature dog ring pass see square away pain poem out gum mouth loud food visit have far', 'but bad chief nature dog', 'but bad nature dog', 'cheese ring pass see square away pain poem out gum mouth loud food visit have far', 'chief', '0.2', '0.8');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_nonsensewords`
--

CREATE TABLE `lex_test_nonsensewords` (
  `p_email` text NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test_nonsensewords`
--

INSERT INTO `lex_test_nonsensewords` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'bunk cack haver posh shuck ad dev ral sib huf doc ep kab feb kub los puf bel has tum', 'bunk cat Hawa posh shop', 'bunk posh', 'cack haver shuck ad dev ral sib huf doc ep kab feb kub los puf bel has tum', 'cat hawa shop', '0.1', '0.4');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_objects`
--

CREATE TABLE `lex_test_objects` (
  `p_email` text NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test_objects`
--

INSERT INTO `lex_test_objects` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'apple banana butterfly ant banana apple ant butterfly butterfly ant banana apple banana apple ant butterfly banana apple apple banana', 'apple banana butterfly and banana', 'apple banana butterfly banana', 'apple apple apple apple apple banana banana banana banana butterfly butterfly butterfly ant ant ant ant', 'and', '4', '0.8');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_phrase`
--

CREATE TABLE `lex_test_phrase` (
  `p_email` text NOT NULL,
  `given` text NOT NULL,
  `spoken` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_sent`
--

CREATE TABLE `lex_test_sent` (
  `p_email` varchar(255) NOT NULL,
  `given` varchar(255) NOT NULL,
  `spoken` varchar(255) NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test_sent`
--

INSERT INTO `lex_test_sent` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'my name is isha', 'my name is Isha', 'my name is isha', '', '', '2', '1'),
('varadjs22@gmail.com', 'i study in ryan international school', 'I study in Ryan International School', 'i study in ryan international school', '', '', '3', '1');

-- --------------------------------------------------------

--
-- Table structure for table `lex_test_word`
--

CREATE TABLE `lex_test_word` (
  `p_email` varchar(255) NOT NULL,
  `given` varchar(255) NOT NULL,
  `spoken` varchar(255) NOT NULL,
  `right_words` text NOT NULL,
  `missing_words` text NOT NULL,
  `extra_words` text NOT NULL,
  `score` text NOT NULL,
  `accuracy` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `lex_test_word`
--

INSERT INTO `lex_test_word` (`p_email`, `given`, `spoken`, `right_words`, `missing_words`, `extra_words`, `score`, `accuracy`) VALUES
('varadjs22@gmail.com', 'after any ask fly her how may before because around', 'after any ask fly her how', 'after any ask fly her how', 'may before because around', '', '0.6', '1');

-- --------------------------------------------------------

--
-- Table structure for table `nonsense_words`
--

CREATE TABLE `nonsense_words` (
  `sr_no` text NOT NULL,
  `word` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `nonsense_words`
--

INSERT INTO `nonsense_words` (`sr_no`, `word`) VALUES
('1', 'bunk'),
('2', 'cack'),
('3', 'haver'),
('4', 'posh'),
('5', 'shuck'),
('6', 'ad'),
('7', 'dev'),
('8', 'ral'),
('9', 'sib'),
('10', 'huf'),
('11', 'doc'),
('12', 'ep'),
('13', 'kab'),
('14', 'feb'),
('15', 'kub'),
('16', 'los'),
('17', 'puf'),
('18', 'bel'),
('19', 'has'),
('20', 'tum');

-- --------------------------------------------------------

--
-- Table structure for table `objects`
--

CREATE TABLE `objects` (
  `sr_no` text NOT NULL,
  `objects` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `objects`
--

INSERT INTO `objects` (`sr_no`, `objects`) VALUES
('1', 'apple banana butterfly ant banana apple ant butterfly butterfly ant banana apple\r\nbanana apple ant butterfly banana apple apple banana');

-- --------------------------------------------------------

--
-- Table structure for table `p_creds`
--

CREATE TABLE `p_creds` (
  `s_name` varchar(20) NOT NULL,
  `age` int(10) NOT NULL,
  `p_name` varchar(20) NOT NULL,
  `school` varchar(50) NOT NULL,
  `p_email` varchar(20) NOT NULL,
  `p_phone` int(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `p_creds`
--

INSERT INTO `p_creds` (`s_name`, `age`, `p_name`, `school`, `p_email`, `p_phone`, `password`) VALUES
('Isha', 5, 'Manish', 'ryan international ', 'varadjs22@gmail.com', 123456, '123456');

-- --------------------------------------------------------

--
-- Table structure for table `sentences`
--

CREATE TABLE `sentences` (
  `sr_no` int(255) NOT NULL,
  `sentence` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sentences`
--

INSERT INTO `sentences` (`sr_no`, `sentence`) VALUES
(1, 'My name is'),
(2, 'I study in ');

-- --------------------------------------------------------

--
-- Table structure for table `words`
--

CREATE TABLE `words` (
  `sr_no` int(255) NOT NULL,
  `word` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `words`
--

INSERT INTO `words` (`sr_no`, `word`) VALUES
(1, 'After'),
(2, 'Any'),
(3, 'Ask'),
(4, 'Fly'),
(5, 'Her'),
(6, 'How'),
(7, 'May'),
(8, 'Before'),
(9, 'Because'),
(10, 'Around');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
