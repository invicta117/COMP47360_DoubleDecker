# Django Application

## Step 1
please first create a conda virtual enviroment using the following command:
    
    conda create --name django_project python=3.8

Please activate this conda enviroment:

    conda activate django_project

Install required packages:

    pip install -r requirements.txt

## Step 2
Please ensure that you have created a new MySQL user and created the associated tables for Django as outlined in the DATA folder in the COMP47360_DoubleDecker/DATA directory

## Step 3
Please ensure that you have place the most up to data GTFS data in the folder COMP47360_DoubleDecker/DATA/RAW_DATA/ as per the README in that folder

## Step 4

Please run the weather scraper by running the command

    nohup python ./doubledecker/main.py &
        
This will run the script in the background

## Step 5

Please run the following command to run a local version of the application
    
    python manage.py runserver
