# How to access Nvidia login node

Dardel has a number of nodes with Nvidia GraceHopper GPUs.
It is not possible to compile your code directly from
the default dardel login nodes, so you need to login to
a specific Nvidia node which currently comes equipped with GPUs.
Submitting jobs from the normal login nodes should be feasible from
the default nods.

If your allocation contains Nvidia GPU resources you can login to
this node using...

```text
ssh logingh
```
