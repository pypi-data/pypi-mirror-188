-- depends: 040__drop_view_last_evaluation_date

-- ExcelExports and ExcelExport_EventFrames

insert into Series (series_id)
select series_id
from ExcelExports
where true
on conflict (series_id) do nothing;

create table ExcelExports_new(
    id integer primary key autoincrement,
    data_service_view_id integer not null,
    series_id integer not null,
    filename text,
    file blob,
    date datetime,
    type text,
    start_date datetime,
    end_date datetime,

    foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade,
    foreign key (series_id) references Series(id)
);

create table ExcelExport_EventFrames_new(
    id integer primary key autoincrement,
    excel_export_id int not null,
    frame_type text not null,

    foreign key (excel_export_id) references ExcelExports_new(id) on delete cascade
);

insert into ExcelExports_new
select
    e.id,
    data_service_view_id,
    (select id from Series s where s.series_id = e.series_id),
    filename,
    file,
    date,
    type,
    start_date,
    end_date
from ExcelExports e;

insert into ExcelExport_EventFrames_new
select id, excel_export_id, frame_type
from ExcelExport_EventFrames;

drop index excel_export_event_frames_fe_id;

drop table ExcelExport_EventFrames;
drop table ExcelExports;

alter table ExcelExports_new rename to ExcelExports;
alter table ExcelExport_EventFrames_new rename to ExcelExport_EventFrames;

create index ExcelExport_EventFrames_idx_export_id on ExcelExport_EventFrames(excel_export_id);
create index Exports_idx_view_id on ExcelExports(data_service_view_id);

-- AnalyzedFrameTypes

insert into Series (series_id)
select series_reference
from AnalyzedFrameTypes
where true
on conflict (series_id) do nothing;

create table AnalyzedFrameTypes_new(
    id text primary key,
    data_service_view_id integer not null,
    series_id integer,
    event_frame_type text not null,
    start_date datetime not null,
    end_date datetime,

    foreign key (data_service_view_id) references DataServiceViews(id) on delete cascade
    foreign key (series_id) references Series(id)
);

insert into AnalyzedFrameTypes_new
select
    id,
    data_service_view_id,
    (select id from Series where series_id = series_reference),
    event_frame_type,
    start_date,
    end_date
from AnalyzedFrameTypes;

drop table AnalyzedFrameTypes;

alter table AnalyzedFrameTypes_new rename to AnalyzedFrameTypes;

create index AnalyzedFrameTypes_idx_view_id on AnalyzedFrameTypes(data_service_view_id);

-- Scores

insert into Series (series_id)
select series_id
from Scores
where true
on conflict (series_id) do nothing;

create table Scores_new(
    id integer primary key autoincrement,
    bin_id integer not null,
    series_id integer,
    score_name text not null,
    score real not null,
    kpi_name text,

    foreign key (bin_id) references DataServiceBins(id) on delete cascade,
    foreign key (series_id) references Series(id)
);

insert into Scores_new
select
    id,
    bin_id,
    (select id from Series s where s.series_id = sc.series_id),
    score_name,
    score,
    kpi_name
from Scores sc;

drop index scores_bin_id;
drop table Scores;
alter table Scores_new rename to Scores;

create index Scores_idx_bin_id on Scores(bin_id);

-- Subscores

insert into Series (series_id)
select series_id
from Subscores
where true
on conflict (series_id) do nothing;

create table Subscores_new(
    id integer primary key autoincrement,
    bin_id integer not null,
    series_id integer,
    subscore_name text not null,
    subscore_result real not null,
    kpi_name text,

    foreign key (bin_id) references DataServiceBins(id) on delete cascade,
    foreign key (series_id) references Series(id)
);

insert into Subscores_new
select
    id,
    bin_id,
    (select id from Series s where s.series_id = sc.series_id),
    subscore_name,
    subscore_result,
    kpi_name
from Subscores sc;

drop index subscores_bin_id;
drop table Subscores;
alter table Subscores_new rename to Subscores;

create index SubScores_idx_bin_id on Subscores(bin_id);

-- DataServiceBadActorScores

insert into Series (series_id)
select series_id
from DataServiceBadActorScores
where true
on conflict (series_id) do nothing;

create table DataServiceBadActorScores_new(
    id integer primary key autoincrement,
    bin_id integer not null,
    series_id integer not null,
    start_date datetime not null,
    end_date datetime not null,
    state text not null,
    score real not null,

    foreign key (bin_id) references DataServiceBins(id) on delete cascade,
    foreign key (series_id) references Series(id)
);

insert into DataServiceBadActorScores_new
select
    id,
    bin_id,
    (select id from Series s where s.series_id = sc.series_id),
    start_date,
    end_date,
    state,
    score
from DataServiceBadActorScores sc;

drop index DataServiceBadActorScores_idx_bin_id_series_id;
drop table DataServiceBadActorScores;
alter table DataServiceBadActorScores_new rename to DataServiceBadActorScores;

create index DataServiceBadActorScores_idx_bin_id_series_id on DataServiceBadActorScores(bin_id, series_id);

-- DataServiceBadActorKPIScore

insert into Series (series_id)
select series_id
from DataServiceBadActorKPIScore
where true
on conflict (series_id) do nothing;

create table DataServiceBadActorKPIScores(
    id integer primary key autoincrement,
    bin_id integer not null,
    series_id integer not null,
    start_date datetime not null,
    end_date datetime not null,
    kpi_name text not null,
    state text not null,
    score real not null,

    foreign key (bin_id) references DataServiceBins(id) on delete cascade
);

insert into DataServiceBadActorKPIScores
select
    id,
    bin_id,
    (select id from Series s where s.series_id = sc.series_id),
    start_date,
    end_date,
    kpi_name,
    state,
    score
from DataServiceBadActorKPIScore sc;

drop index DataServiceBadActorKPIScore_idx_bin_id_series_id;
drop table DataServiceBadActorKPIScore;

create index DataServiceBadActorKPIScores_idx_bin_id_series_id on DataServiceBadActorKPIScores(bin_id, series_id);

-- EventFrameReferences

insert into Series (series_id)
select reference
from EventFrameReferences
where reference is not null
on conflict (series_id) do nothing;

create table EventFrameReferences_new(
    id integer primary key autoincrement,
    event_frame_id integer not null,
    data_service_id integer not null,
    reference integer,

    unique(event_frame_id, reference),
    foreign key (event_frame_id) references "EventFrames"(id) on delete cascade,
    foreign key (reference) references Series(id)
);

insert into EventFrameReferences_new
select
    id,
    event_frame_id,
    data_service_id,
    (select id from Series where series_id = reference)
from EventFrameReferences;

drop index EventFrameReferences_idx_data_service_reference;
drop index EventFrameReferences_idx_data_service_id;
drop table EventFrameReferences;

alter table EventFrameReferences_new rename to EventFrameReferences;

create index EventFrameReferences_idx_data_service_reference on EventFrameReferences(data_service_id, reference);
create index EventFrameReferences_idx_data_service_id on EventFrameReferences(data_service_id);
create index EventFrameReferences_idx_reference on EventFrameReferences(reference);
