CREATE TABLE `Entry` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`	TEXT NOT NULL,
	`entry`	TEXT NOT NULL,
    `date` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL,
    FOREIGN KEY(`mood_id`) REFERENCES `Mood`(`id`)
);

CREATE TABLE `Mood` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `label`    TEXT NOT NULL
);

CREATE TABLE `Tag` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`tag`  TEXT NOT NULL
);

CREATE TABLE `Entry_tag` (
    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `tag_id` INTEGER NOT NULL,
    `entry_id` INTEGER NOT NULL,
    FOREIGN KEY(`tag_id`) REFERENCES `Tag`(`id`),
    FOREIGN KEY(`entry_id`) REFERENCES `Entry`(`id`)
);

INSERT INTO `Entry` VALUES (null, 'Python', 'We started python and SQL today', '1/9/22', 1);

INSERT INTO `Mood` VALUES (null, 'excited');

INSERT INTO `Tag` VALUES (null, "python");

INSERT INTO `Entry_tag` VALUES (null, 1, 1);

INSERT INTO entries VALUES (null, 'sql', 'We started sql', '1/18/22', 2);

INSERT INTO `moods` VALUES (null, 'exhausted');





