CREATE TABLE Groups(
            group_name TEXT PRIMARY KEY,
            description TEXT
            );
CREATE TABLE Users(
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            username TEXT PRIMARY KEY,
            password TEXT,
            FK_group TEXT,
            FOREIGN KEY (FK_group) REFERENCES Groups(group_name)
            );
CREATE TABLE Lectures(
                lectureID INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                type TEXT,
                class TEXT
            );
CREATE TABLE Lectured_By(
                lecture_byID INTEGER PRIMARY KEY AUTOINCREMENT,
                FK_lectures INTEGER,
                FK_user TEXT,
                FOREIGN KEY(FK_user) REFERENCES Users(username),
                FOREIGN KEY(FK_lectures) REFERENCES Lectures(lectureID)
                );
CREATE TABLE Marks(
                markID INTEGER PRIMARY KEY AUTOINCREMENT,
                FK_user TEXT,
                FK_lectures INTEGER,
                mark INTEGER,
                FOREIGN KEY(FK_user) REFERENCES Users(username),
                FOREIGN KEY(FK_lectures) REFERENCES Lectures(lectureID)
            );
CREATE TABLE GroupLectures(
                    grouplectureID INTEGER PRIMARY KEY AUTOINCREMENT,
                    FK_lectures INTEGER,
                    FK_group TEXT,
                    FOREIGN KEY (FK_group) REFERENCES Groups(group_name),
                    FOREIGN KEY (FK_lectures) REFERENCES Lectures(lectureID)
                );
