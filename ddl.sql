create table directory
(
    id     int auto_increment
        primary key,
    name   varchar(255) charset utf8mb3 not null,
    parent int                          null,
    constraint directory_directory_id_fk
        foreign key (parent) references directory (id)
            on delete cascade
);

create table file
(
    id           int                          not null
        primary key,
    name         varchar(255) charset utf8mb3 not null,
    directory_id int                          not null,
    content      mediumtext                   null,
    searchable   bit                          not null,
    constraint file_directory_id_fk
        foreign key (directory_id) references directory (id)
            on delete cascade
);

create fulltext index file__content
    on file (content);

create index file__name
    on file (name);

create
    definer = root@`%` procedure Search(IN from_dir int, IN query varchar(256), IN except_ids text)
BEGIN

    WITH RECURSIVE DirectoryPath AS (
    SELECT id, name, parent, name AS path
    FROM dcr.directory
    WHERE id = from_dir
    UNION ALL
    SELECT d.id, d.name, d.parent, CONCAT(dp.path, '/', d.name)
    FROM dcr.directory d
    INNER JOIN DirectoryPath dp ON d.parent = dp.id
),
FilesInDirectory AS (
    SELECT f.name, f.content, f.directory_id, f.id,
    CAST((LENGTH(f.content) - LENGTH(REPLACE(f.content, query, ''))) / LENGTH(query) as UNSIGNED) AS occurrences
    FROM dcr.file f
    WHERE f.directory_id IN (SELECT id FROM DirectoryPath)
    AND BINARY f.content LIKE CONCAT('%', query, '%')
    AND searchable = 1
    AND find_in_set(f.id, except_ids) = 0
)
SELECT fid.id, fid.name, fid.content, fid.directory_id,fid.occurrences, CONCAT(dp.path, '/', fid.name) AS full_path
FROM FilesInDirectory fid
INNER JOIN DirectoryPath dp ON fid.directory_id = dp.id;



END;

