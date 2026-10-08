# Data migration
Since Dardel will cease to be a NAISS resource at the end of this year, the time has now come to start the data migration of Dardel to Arrhenius. The move of the Dardel data starts in October, and lasts until the end of this year.

## Procedure
For the data migration from Dardel, a similar procedure will be followed as for the data migration from Tetralith.

The PI (or another person the PI delegates this task to) can request a data transfer from NAISS using the command `storagemigrate` on Dardel. You will then be asked to provide the "what" and "when" for the data transfer. The last possible start date to request for a data transfer is 2026-12-17. You can change or cancel your request by simply re-running `storagemigrate` later.

The options for what the project wants NAISS to transfer are:

- Request a full move - NAISS moves the entire project storage directory.
- Request a partial move - NAISS moves ONLY the data you have put into the "to-arrhenius" subdirectory (e.g `/cfs/klemming/projects/supr/DIRECTORYNAME/to-arrhenius`) This can be useful if your data does not fit into your storage allocation on Arrhenius and you want to move most of the data to Arrhenius now but leave some on Dardel to be handled later. You need to create the `to-arrhenius` directory.
- No move - the project will move its own data
- No move - the project has no data that needs to move

Each project can only request one data transfer.

Data will be moved to the `from-dardel` subdirectory of your Arrhenius project storage directory, e.g `/cfs/klemming/projects/supr/DIRECTORYNAME` on Dardel will be moved to `/nobackup/proj/disk/DIRECTORYNAME/from-dardel`. You can then move the data from `from-dardel` to another location in the project storage directory tree, or leave it there.

Since most projects will get a smaller storage allocation on Arrhenius, most projects will need to remove or move data before the data can be transferred.
It is the project's responsibility to make sure that the data you request a transfer for will fit into your storage allocation on Arrhenius.
If the data you requested a transfer for will not fit into your storage allocation on Arrhenius the transfer may fail or you may end up being over quota on Arrhenius.

When the data transfer begins, the data becomes inaccessible on Dardel. When the data transfer is complete, the data will become accessible on Arrhenius. I.e you will never see partial data anywhere and you will not be able to access the data while the transfer is in progress. Once the data transfer is complete, the project directory on Dardel will be unlocked again for use until the project ends. Do note that data generated after the requested data transfer has been started will not be migrated. The project is responsible for migrating this data to Arrhenius themselves if needed.

Since storage projects on Dardel are generally much larger, the transfer will take more time than for the other clusters.
