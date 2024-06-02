"""
Folder Synchronizer class for synchronizing contents between source and replica folders.
"""
import os
import filecmp
import shutil
from pathlib import Path

class FolderSynchronizer:
    """
    A class to synchronize contents between a source folder and a replica folder.

    Attributes:
        source_folder (Path): Path to the source folder.
        replica_folder (Path): Path to the replica folder.
        log (CustomLogger): CustomLogger instance for logging synchronization activities.
    """

    def __init__(self, source_folder: str, replica_folder: str, log: 'CustomLogger') -> None:
        """
        Initializes the FolderSynchronizer with the given folders and logger.

        Args:
            source_folder (str): The path to the source folder.
            replica_folder (str): The path to the replica folder.
            log (CustomLogger): CustomLogger instance for logging synchronization activities.
        """
        self.source_folder = Path(source_folder)
        self.replica_folder = Path(replica_folder)
        self.log = log

    def synchronize(self) -> None:
        """
        Synchronizes the contents of the source folder to the replica folder.
        Raises:
            FileNotFoundError: If the source folder does not exist.
        """
        if not os.path.exists(self.source_folder):
            raise FileNotFoundError(f"Source folder not found: {self.source_folder}")

        if not os.path.exists(self.replica_folder):
            os.makedirs(self.replica_folder)
            self.log.warning(f"Replica folder was created: {self.replica_folder}")

        self.remove_items()
        self.create_or_update_items()

    def remove_items(self) -> None:
        """
        Removes items from the replica folder that do not exist in the source folder.
        """
        for replica_item_path in self.replica_folder.rglob('*'):
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
                raise Exception(f"Error removing '{replica_item_path}' - {str(e)}") from e

    def create_or_update_items(self) -> None:
        """
        Creates or updates items in the replica folder to match the source folder.
        """
        for source_item_path in self.source_folder.rglob('*'):
            replica_item_path = os.path.join(self.replica_folder,
                                            os.path.relpath(source_item_path, self.source_folder))

            if os.path.isdir(source_item_path):
                if not os.path.exists(replica_item_path):
                    os.makedirs(replica_item_path)
                    self.log.info(f"Created folder: {replica_item_path}")

            elif os.path.isfile(source_item_path):
                try:
                    if os.path.exists(replica_item_path) and filecmp.cmp(source_item_path,
                            replica_item_path, shallow=False):
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
                    error_msg = f"Error creating or updating item '{source_item_path}' - {str(e)}"
                    raise Exception(error_msg) from e
