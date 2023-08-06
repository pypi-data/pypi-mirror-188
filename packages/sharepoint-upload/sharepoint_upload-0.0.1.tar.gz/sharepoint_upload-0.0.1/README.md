# Upload to SharePoint
A library to upload files to sharepoint.

This library depends on office 365 library, and it will use active directory authentication to connect to SharePoint.

## Installation
In order to install this library you need to obtain an `SSH code`

Use pip to install this library from Github:

    pip install git+ssh://git@github.com/mo-sij-inso/sharepoint_upload.git

## Requirements
First you need to initialize the the sharepoint connection, which is an object.
You have two options, either use embedded credentials in environment variables:

`USERNAME` for office365 email

`PASSWORD` for office365 password


Then you can use this call:

    sp = sp_folder(site_url)

The second option is to provide the credentials in the class call:

    sp = sp_folder(site_url,username,password)

Once the object is created successfully, you can call use `send_file` method to upload the files to sharepoiont

## Example
    site_url = "https://insongosafety.sharepoint.com/teams/TechnologyInnovation"
    target = "/teams/TechnologyInnovation/Shared Documents/General/Information Management/99. Resources/01. Executive Dashboard data"
    file = '1.txt'
    sp = sp_folder(site_url)
    sp.send_file(file,target)
