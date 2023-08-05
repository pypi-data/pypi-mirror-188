--- depends: 083__drop_score_tables

alter table Segments add column is_open_at_start boolean not null default(FALSE);
