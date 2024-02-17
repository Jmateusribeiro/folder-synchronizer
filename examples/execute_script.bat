
set "batch_directory=%~dp0"
set sourceDir=%batch_directory%source_dir
set replicaDir=%batch_directory%replica_dir
set logFolder=%batch_directory%logs

mkdir "%replicaDir%"
mkdir "%logFolder%"

python -m folder_synchronizer --sourceDir %sourceDir% --replicaDir %replicaDir% --logFolder %logFolder%

pause

rd /s /q "%replicaDir%"
rd /s /q "%logFolder%"