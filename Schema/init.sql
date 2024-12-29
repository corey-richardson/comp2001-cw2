CREATE SCHEMA CW2;

CREATE TABLE "CW2.User" (
    "id" INT PRIMARY KEY IDENTITY (1, 1),
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "role" VARCHAR(6) NOT NULL CHECK ("role" IN ('ADMIN', 'USER'))
);

CREATE TABLE "CW2.Trail" (
    "id" INT PRIMARY KEY IDENTITY (1, 1),
    "author_id" INT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "summary" VARCHAR(255) NOT NULL,
    "description" TEXT NOT NULL,
    "location" VARCHAR(255) NOT NULL,
    "length" FLOAT(6) NOT NULL,
    "elevation_gain" INT NOT NULL,
    "route_type" VARCHAR(15) NOT NULL,

    FOREIGN KEY ("author_id") REFERENCES "CW2.User" ("id")
    -- If author account gets deleted, set author to null
    ON DELETE SET NULL ON UPDATE CASCADE,

    CHECK ("difficulty" IN ('Easy', 'Moderate', 'Hard')),
    CHECK ("route_type" IN ('Loop', 'Out & back', 'Point to point')),
    -- Trail Names CAN be common but still different, but a combination of 
    -- trail_name and location being the same suggests a duplicate
    UNIQUE("trail_name", "location") 
);

-- Points follow a doubly-linked list structure
CREATE TABLE "CW2.Point" (
    "id" INT PRIMARY KEY IDENTITY (1, 1),
    "next_point_id" INT,
    "previous_point_id" INT,
    "latitude" DECIMAL(9,6) NOT NULL,
    "longitude" DECIMAL(9,6) NOT NULL,
    "description" VARCHAR(127),

    FOREIGN KEY ("next_point_id") REFERENCES "CW2.Point" ("id")
    ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY ("previous_point_id") REFERENCES "CW2.Point" ("id")
    ON DELETE SET NULL ON UPDATE CASCADE,

    CONSTRAINT check_latitude CHECK ("latitude" BETWEEN -90 AND 90),
    CONSTRAINT check_longitude CHECK ("longitude" BETWEEN -180 AND 180)
);

CREATE TABLE "CW2.Feature" (
    "id" INT PRIMARY KEY IDENTITY(1, 1),
    "feature" VARCHAR(255) NOT NULL
);

CREATE TABLE "CW2.TrailFeature" (
    "trail_id" INT NOT NULL,
    "feature_id" INT NOT NULL,

    FOREIGN KEY ("trail_id") REFERENCES "CW2.Trail" ("id")
    ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY ("feature_id") REFERENCES "CW2.Feature" ("id")
    ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE("trail_id", "feature_id")
);
