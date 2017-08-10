REM @echo off

REM #############################################################################
REM #                                                                           #
REM #                                                                           #
REM #                                                                           #
REM #############################################################################

set data_dir=Y:\Data\data
set data_fname_0=this_data.txt
set data_fname=%data_dir%\%data_fname_0%
set stat_fname=stat_%data_fname_0%

set tname=this_table
set schema=this_schema

type %data_fname% | python mksql-ctable.py tab 1 null %tname% %schema% %data_fname% > %stat_fname%


