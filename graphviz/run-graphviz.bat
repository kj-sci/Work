REM echo off

if "%1" EQU "" (
 goto ERR
)

if "%2" EQU "" (
 goto ERR
)

if "%3" EQU "" (
 goto ERR
)

set base_dir=\\RKDA0201\Resource\Koji_Yokoyama\programs\python2\graphviz
set sql_list=%1
set node_fname=%base_dir%\nodes.txt
set edge_fname=%base_dir%\edge.txt
set dot_fname=%base_dir%\graph.dot
set png_fname=%base_dir%\%2
set graph_name=%3

REM ###########################################################
REM #                                                         #
REM #              SQL => NODES/EDGES                         #
REM #                                                         #
REM ###########################################################
type %sql_list% | python sql2graphviz.py %node_fname% %edge_fname%


REM ###########################################################
REM #                                                         #
REM #              NODES/EDGES => DOT                         #
REM #                                                         #
REM ###########################################################

python tsv2graphviz.py %graph_name% %node_fname% %edge_fname% > %dot_fname% 

REM ###########################################################
REM #                                                         #
REM #             DOT => PNG                                  #
REM #                                                         #
REM ###########################################################

set graphviz_dir=C:\Users\kfehvb1\Documents\software\graphviz\
set bindir=%graphviz_dir%bin\

%bindir%dot.exe -Tpng -o %png_fname% %dot_fname%


goto EOF

:ERR
echo usage: run-graphviz.bat sql_list png_name graph_title

:EOF




