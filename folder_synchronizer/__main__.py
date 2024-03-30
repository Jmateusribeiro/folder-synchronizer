"""
    main module
"""

import argparse
import os
from folder_synchronizer.classes.log import CustomLogger
from folder_synchronizer.classes.folder_operations import FolderSynchronizer


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sourceDir", 
                        type=str, 
                        help="Complete Directory of Source folder", 
                        required=True)
    parser.add_argument("--replicaDir", 
                        type=str, 
                        help="Complete Directory of Replica folder", 
                        required=True)
    parser.add_argument("--logFolder", 
                        type=str, 
                        help="Complete Directory of Log folder", 
                        required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    
    source_folder = args.sourceDir
    replica_folder = args.replicaDir
    logs_folder = args.logFolder

    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(replica_folder, exist_ok=True)
    os.makedirs(logs_folder, exist_ok=True)

    log = CustomLogger(logs_folder)
    log.info("### Folder Synchronization ###")
    log.info(f"Source Folder: {source_folder}")
    log.info(f"Replica Folder: {replica_folder}")
    folder_sync = FolderSynchronizer(source_folder, replica_folder, log)  
    
    try:
        log.info("...Strating Synchronization...")
        folder_sync.synchronize()
        log.info("...Folders Synchronized...")
    except Exception as e:
        log.error(f"Error during synchronization: {str(e)}")
    
    log.info("...Ending Synchronization...")

if __name__ == "__main__":
    main()
