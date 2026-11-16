# Data migration to Arrhenius
NOTE: Data migration to Arrhenius does not happen automatically. If no request is submitted on behalf of the project, no data will be transferred.

Since Dardel and Klemming will cease to be NAISS resources at the end of this year, the move of the Dardel data to Arrhenius is ongoing. 
The process started in October, and lasts until the end of this year, after which the data will be deleted (2026-12-31).

### What
Only project data on Klemming can be requested to be migrated. 
This means data in the 'scratch', and 'home' directories will not be transferred. 
If you wish to transfer data in your home directory to Arrhenius, there is a script available for this on Dardel. [More details can be found below](#home-directories).

All data belonging to NAISS users on Klemming will be deleted after the end of this year (2026-12-31).

### When
The data migration from Dardel to Arrhenius is ongoing.
If you wish for your project data to be migrated to Arrhenius, make sure you submit a data migration request before the 1st of December 2026.
Data belonging to NAISS users that has not been transferred before the end of this year (2026-12-31) will be deleted.

### How
Data migration is **not automatic**. 
To have your project data transferred to Arrhenius, you **must submit a request** using the command `storagemigrate` on Dardel ([see below for more details](#project-data)). 
If no request is submitted, no transfer will be done. 

Data transfers are scheduled on a first-come, first-served basis. This means that the project that submitted a data migration request for a specific day first, will be migrated first.
Transfers are started automatically, usually within half an hour on the requested date. Please note that the start date is not guanranteed and dependent on how many other projects have requested a transfer for that date.

Please run the `storagemigrate` command even if you do not wish to transfer data and select one of the 'No move' options when asked what to transfer. This makes it easier for NAISS staff to anticipate the demand for data migration. 

## Detailed procedure
### Project data
For the data migration from Dardel, a similar procedure will be followed as for the data migration from Tetralith.

The PI (or another person the PI delegates this task to) can request a data transfer from NAISS using the command `storagemigrate` on Dardel. You will then be asked to provide the "what" and "when" for the data transfer. The last possible start date to request for a data transfer is 2026-12-17. You can change or cancel your request by simply re-running `storagemigrate` later.

The options for what the project wants NAISS to transfer are:

- Request a full move - NAISS moves the entire project storage directory.
- Request a partial move - NAISS moves ONLY the data you have put into the `to-arrhenius` subdirectory (e.g `/cfs/klemming/projects/supr/DIRECTORYNAME/to-arrhenius`). This can be useful, e.g. if your data does not fit into your storage allocation on Arrhenius and you want to move most of the data to Arrhenius now but leave some on Dardel to be handled later. You need to create the `to-arrhenius` directory.
- No move - the project will move its own data
- No move - the project has no data that needs to move

Each project can only request one data transfer.

Data will be moved to the `from-dardel` subdirectory of your Arrhenius project storage directory, e.g `/cfs/klemming/projects/supr/DIRECTORYNAME` on Dardel will be moved to `/nobackup/proj/disk/DIRECTORYNAME/from-dardel`. You can then move the data from `from-dardel` to another location in the project storage directory tree, or leave it there.

Please make sure you have an allocation on Arrhenius before submitting a data migration request. 

Since most projects will get a smaller storage allocation on Arrhenius, most projects will need to remove or move data before the data can be transferred.
It is the project's responsibility to make sure that the data you request a transfer for will fit into your storage allocation on Arrhenius.
If the data you requested a transfer for will not fit into your storage allocation on Arrhenius the transfer may fail or you may end up being over quota on Arrhenius.

When the data transfer begins, the data becomes inaccessible on Dardel. When the data transfer is complete, the data will become accessible on Arrhenius. This means that you will never see partial data anywhere and you will not be able to access the data while the transfer is in progress. Once the data transfer is complete, the project directory on Dardel will be unlocked again for use until the project ends. Do note that data generated after the requested data transfer has been started will not be migrated. The project is responsible for migrating this data to Arrhenius themselves if needed.
The user that submitted the transfer request will receive an email notification when the transfer starts and when it is completed.

The command `storagemigrate_overview` can be used to see for which days other projects have already requested transfers. If possible, try to request your transfer for a day that is less busy, it will speed up your data transfer. `storagemigrate_overview` will also show ongoing transfers so you can use it to see if your transfer has started.

Since storage projects on Dardel are generally much larger, the transfer will take more time than for the other clusters. Transfers can span up to several days, or in some cases weeks.

If you plan to transfer data yourself, please remember to use the file transfer node `dardel-ftn01.pdc.kth.se`.

### Home directories
The command `copy_home_directory_to_arrhenius` is available on Dardel that will copy the contents of your home directory to Arrhenius. 

The home directory is copied, not moved.
The data will be copied to a subdirectory `from-dardel` in the Arrhenius home directory in order not to overwrite any Arrhenius settings or data that might already be there.

The script will ask for confirmation before doing anything and show you the rsync command that will be used.
