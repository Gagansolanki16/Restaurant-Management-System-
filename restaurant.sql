CREATE TABLE `admin` (
  `username` varchar(10) NOT NULL,
  `password` varchar(8) NOT NULL
);



INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');


CREATE TABLE `bills` (
  `Bill_no` int(11) NOT NULL,
  `Cname` varchar(30) NOT NULL,
  `Cno` varchar(10) NOT NULL,
  `Date` date NOT NULL,
  `Total` float NOT NULL
) ;



CREATE TABLE `menu` (
  `ID` int(3) NOT NULL,
  `Item_name` varchar(20) NOT NULL,
  `Cost` int(11) NOT NULL
);



ALTER TABLE `admin`
  ADD PRIMARY KEY (`username`);


ALTER TABLE `bills`
  ADD PRIMARY KEY (`Bill_no`);


ALTER TABLE `menu`
  ADD PRIMARY KEY (`ID`);
COMMIT;


