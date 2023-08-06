import os
import ntpath
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext

class sp_folder:

    def __init__(self,site_url,username=os.environ.get('USERNAME'),password=os.environ.get('PASSWORD')):
        """
        Init constructor to build the class, requires only the @site_url
        it will take username and password as optional values, if two are not provided
        they will be retrieved from the local environment under $USERNAME and $PASSWORD name
        """

        self.site_url = site_url    # parameter for the sharepoint site
        self.username = username    # AD username
        self.password = password    # AD password
        self.ctx = self.ctx()       # Establish connection

        
    def ctx(self):
        try:
            ctx = ClientContext(self.site_url).with_credentials(UserCredential(f"{self.username}", f"{self.password}"))
            return ctx
        except:
            print("[Error] Could not connect to the SharePoint site, check your credentials and site url.")

        
    def read_file(self,file):
        """
        This function will read the content of the file before uploading it
        and returns a file_content object
        """
        try:
            with open(file, 'rb') as opened_file:
                file_content = opened_file.read()
                return file_content
        except:
            raise Exception("[Error] Could not read the file contents, make sure it's available with correct path.")

    def send_file(self,file,target_url) -> bool:
        """
        Function to send a @file within the local premise to a sharepoint @target_folder
        It shouldn't have the library url, so no http link and it has only / (backslashes) 
        This will return True if the file was uploaded successfully
        A good example is: "/teams/TechnologyInnovation/Shared Documents/General/Information Management/
        """

        # Read the file content
        file_content = self.read_file(file)

        # Extract the file's name
        file_name = ntpath.basename(file)

        try:
            # Get actual folder from server
            folder = self.ctx.web.get_folder_by_server_relative_url(target_url)
        except:
            raise Exception("[Error] Could not get to the folder, make sure the path is correct")
        
        try:
            # Upload file to that folder
            folder.upload_file(file_name, file_content).execute_query()

            return True
        except:
            raise Exception("[Error] Could not upload the file, make sure it's not read-only and you have proper")
