import os
import sys
import shutil
from unittest.mock import Mock
import pytest
from typing import Generator
from _pytest.fixtures import FixtureRequest

# Adding the folder containing the folder_operations module to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from folder_synchronizer.classes.folder_operations import FolderSynchronizer

# Global variables for the source and replica folders used in tests
source_folder = 'test_source_folder'
replica_folder = 'test_replica_folder'
log = Mock()

@pytest.fixture(scope="module", autouse=True)
def create_folders(request: FixtureRequest) -> None:
    """
    Fixture to create and teardown test folders for the module.

    Args:
        request (FixtureRequest): The fixture request object.
    """
    # Setup
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(replica_folder, exist_ok=True)

    def teardown() -> None:
        # Teardown
        shutil.rmtree(source_folder)
        shutil.rmtree(replica_folder)

        assert not os.path.exists(source_folder)
        assert not os.path.exists(replica_folder)

    # Register the teardown function to be called after tests
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def folder_sync() -> FolderSynchronizer:
    """
    Fixture to provide a FolderSynchronizer instance for each test function.

    Returns:
        FolderSynchronizer: An instance of FolderSynchronizer.
    """
    return FolderSynchronizer(source_folder, replica_folder, log)

def test_synchronize_nonexistent_source_folder() -> None:
    """
    Test synchronizing a non-existent source folder raises FileNotFoundError.
    """
    folder_sync = FolderSynchronizer('nonexistent_source', replica_folder, log)

    with pytest.raises(FileNotFoundError):
        folder_sync.synchronize()

def test_synchronize_create_replica_folder() -> None:
    """
    Test that the replica folder is created if it does not exist.
    """
    custom_replica_folder = 'custom_replica_folder'
    folder_sync = FolderSynchronizer(source_folder, custom_replica_folder, log)

    folder_sync.synchronize()

    assert os.path.exists(custom_replica_folder)
    
    shutil.rmtree(custom_replica_folder)
    assert not os.path.exists(custom_replica_folder)

def test_synchronize_remove_folder(folder_sync: FolderSynchronizer) -> None:
    """
    Test that a folder in the replica that does not exist in the source is removed.
    """
    empty_folder = os.path.join(replica_folder, 'folder_removal/folder')
    os.makedirs(empty_folder)

    folder_sync.synchronize()

    assert not os.path.exists(empty_folder)

def test_synchronize_remove_file(folder_sync: FolderSynchronizer) -> None:
    """
    Test that a file in the replica that does not exist in the source is removed.
    """
    empty_folder = os.path.join(replica_folder, 'file_removal/folder/')
    os.makedirs(empty_folder)
    empty_file = os.path.join(empty_folder, 'file.txt')
    open(empty_file, 'w').close()

    folder_sync.synchronize()

    assert not os.path.exists(empty_file)

def test_synchronize_create_folder(folder_sync: FolderSynchronizer) -> None:
    """
    Test that a folder in the source is copied to the replica.
    """
    folder_name = 'folder_creation/folder/folder'
    os.makedirs(os.path.join(source_folder, folder_name))

    folder_sync.synchronize()

    assert os.path.exists(os.path.join(replica_folder, folder_name))

def test_synchronize_create_file(folder_sync: FolderSynchronizer) -> None:
    """
    Test that a file in the source is copied to the replica.
    """
    folder_name = 'file_creation/folder/folder/'
    os.makedirs(os.path.join(source_folder, folder_name))
    file_name = folder_name + 'file.txt'
    open(os.path.join(source_folder, file_name), 'w').close()

    folder_sync.synchronize()

    assert os.path.exists(os.path.join(replica_folder, file_name))

def test_synchronize_update_file(folder_sync: FolderSynchronizer) -> None:
    """
    Test that a file in the replica is updated to match the source.
    """
    file_name = 'file.txt'
    content = 'test update file'
    open(os.path.join(replica_folder, file_name), 'w').close()

    with open(os.path.join(source_folder, file_name), 'w') as f:
        f.write(content)

    folder_sync.synchronize()

    with open(os.path.join(replica_folder, file_name), 'r') as f:
        assert f.read() == content
