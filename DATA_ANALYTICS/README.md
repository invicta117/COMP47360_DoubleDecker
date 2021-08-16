# Data Analytics

As the size of the data is quite large and connection to the high powered server is tempromental and can cause disconnections frequently the following command can be run to allow the notebooks to be run without a browser and saving the output to the origional notebook so that it can be loaded later and examined. This ensures that a break in connection will not result in the execution being lost.

    nohup jupyter nbconvert --execute --to notebook --inplace DUBLIN_BUS_JAN.ipynb &> notebook.log &