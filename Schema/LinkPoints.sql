-- Insert Points
INSERT INTO "CW2.Point" (latitude, longitude, description)
VALUES
    (50.423698, -4.110593, 'Point 1'),
    (50.424958, -4.108179, 'Point 2'),
    (50.420222, -4.099503, 'Point 3'),
    (50.422134, -4.113191, 'Point 4'),
    (50.424262, -4.109453, 'Point 5');

BEGIN
    DECLARE @Point1 INT = (SELECT id FROM "CW2.Point" WHERE latitude = 50.423698 AND longitude = -4.110593);
    DECLARE @Point2 INT = (SELECT id FROM "CW2.Point" WHERE latitude = 50.424958 AND longitude = -4.108179);
    DECLARE @Point3 INT = (SELECT id FROM "CW2.Point" WHERE latitude = 50.420222 AND longitude = -4.099503);
    DECLARE @Point4 INT = (SELECT id FROM "CW2.Point" WHERE latitude = 50.422134 AND longitude = -4.113191);
    DECLARE @Point5 INT = (SELECT id FROM "CW2.Point" WHERE latitude = 50.424262 AND longitude = -4.109453);

    UPDATE "CW2.Point"
    SET next_point_id = @Point2, previous_point_id = @Point5
    WHERE id = @Point1;

    UPDATE "CW2.Point"
    SET next_point_id = @Point3, previous_point_id = @Point1
    WHERE id = @Point2;

    UPDATE "CW2.Point"
    SET next_point_id = @Point4, previous_point_id = @Point2
    WHERE id = @Point3;

    UPDATE "CW2.Point"
    SET next_point_id = @Point5, previous_point_id = @Point3
    WHERE id = @Point4;

    UPDATE "CW2.Point"
    SET next_point_id = @Point1, previous_point_id = @Point4
    WHERE id = @Point5;


    -- Insert the new trail into the "CW2.Trail" table
    INSERT INTO "CW2.Trail" (
        author_id, 
        starting_point_id, 
        name, 
        summary, 
        description, 
        difficulty, 
        location, 
        length, 
        elevation_gain, 
        route_type
    )
    VALUES (
        NULL,
        @Point1,  -- starting_point_id (using Point 1)
        'Plymouth Airport Runway',
        'A walk that follows Plymouth Airports runway',
        'This trail follows the Plymouth airport runway. Not technically legal to walk this one.',
        'Easy',
        'Plymouth, UK',
        5.0,
        1,
        'Loop'
    );
END;