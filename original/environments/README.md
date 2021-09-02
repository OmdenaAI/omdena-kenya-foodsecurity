# Anaconda environment files for getting started

In order to get started we have created environment files for Anaconda. We try to provide at least 3 versions of the latest file.
<br>
<br>
**Windows 10** users should use the file [omdena-GPSDD_win_v0.1.1.yml](omdena-GPSDD_win_v0.1.1.yml)
 because if will have already all the dependencies solved. This will safe a lot of time during setup.
<br>
<br>
**MacOS** and **Linux** users should first try the file [omdena-GPSDD_v0.1.1.yml](environments\omdena-GPSDD_v0.1.1.yml). If this does not work out you can use option 3 which will take a long time and might still fail.
<br>
<br>
**Option 3**: [omdena-GPSDD_explicit_v0.1.1.yml](environments\omdena-GPSDD_explicit_v0.1.1.yml)

## Setting up the environment from Anaconda prompt
In the Anaconda prompt type:<br>

```conda env create --file filename.yml```

## Updating an existing environment from Anadonda prompt

```
conda activate omdena-GPSSD  
conda env update --file local.yml  
```