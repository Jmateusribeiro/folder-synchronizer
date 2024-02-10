import os
import filecmp
import shutil
from pathlib import Path


class FolderSynchronizer:
    def __init__(self, source_folder, replica_folder, log):
        # using 'Path' class to facilitate (method rglob) iteration over all subfiles and directories.
        self.source_folder = Path(source_folder)
        self.replica_folder = Path(replica_folder)
        self.log = log

    def synchronize(self):

        # If source folder don't exists should be thrown error
        # but if replica folder don't exists must be created
        if not os.path.exists(self.source_folder):
            raise FileNotFoundError(f"Source folder not found: {self.source_folder}")
    
        if not os.path.exists(self.replica_folder):
            os.makedirs(self.replica_folder)
            # logging that action has a warning because 
            # this folder is created when the program starts, by default
            self.log.warn(f"Replica folder was deleted: {self.replica_folder}")

        self.__remove_items()
        self.__create_or_update_items()

    # since this class it will not be inherited (at least in this challenge)
    # methods from here will be private (and not protected)
    def __remove_items(self):
        for replica_item_path in self.replica_folder.rglob('*'):
            # it could be used 'Path' methods to perform the actions over files and folder 
            # but I prefer using 'os' methods, since 'Path' methods use 'os' anyway
            source_item_path = os.path.join(self.source_folder, 
                                            os.path.relpath(replica_item_path, self.replica_folder))
            try:
                if not os.path.exists(source_item_path):
                    if os.path.isfile(replica_item_path):
                        os.remove(replica_item_path)
                        self.log.info(f"Removed File: {replica_item_path}")
                    elif os.path.isdir(replica_item_path):
                        shutil.rmtree(replica_item_path)
                        self.log.info(f"Removed Folder: {replica_item_path}")

            except Exception as e:
                raise Exception(f"Error removing '{replica_item_path}' - {str(e)}")
   
    def __create_or_update_items(self):
        for source_item_path in self.source_folder.rglob('*'):
            replica_item_path = os.path.join(self.replica_folder, 
                                            os.path.relpath(source_item_path, self.source_folder))

            if os.path.isdir(source_item_path):
                if not os.path.exists(replica_item_path):
                    os.makedirs(replica_item_path)
                    self.log.info(f"Created folder: {replica_item_path}")  
                
            elif os.path.isfile(source_item_path):
                try:
                    # If file already exists and has the same content, should go to next iteration
                    if os.path.exists(replica_item_path) and filecmp.cmp(source_item_path, replica_item_path):
                        continue
                    
                    if os.path.exists(source_item_path):
                        
                        #Logging different variables just because a matter of logic :)
                        #Update item inside replica folder but copied from source folder
                        if os.path.exists(replica_item_path):
                            message = f"Updated file: {replica_item_path}"
                        else:
                            message = f"Copied file: {source_item_path}"

                        shutil.copy2(source_item_path, replica_item_path)
                        
                        # logging after the action was really performed
                        # but need to "catch" the action before 
                        # to understand if was a create or update action
                        self.log.info(message)
                        
                    else:
                        self.log.error(f"Error: Source file not found: {source_item_path}")
                except Exception as e:
                    raise Exception(f"Error creatig item '{source_item_path}' - {str(e)}")
                