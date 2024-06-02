"""
unit tests
"""
import os
import sys
import shutil
from unittest.mock import Mock
import pytest
from _pytest.fixtures import FixtureRequest
from folder_synchronizer.classes.folder_operations import FolderSynchronizer

# Adding the folder containing the folder_operations module to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Global variables for the source and replica folders used in tests
SOURCE_FOLDER = 'test_source_folder'
REPLICA_FOLDER = 'test_replica_folder'
log = Mock()

@pytest.fixture(scope="module", autouse=True)
def create_folders(request: FixtureRequest) -> None:
    """
    Fixture to create and teardown test folders for the module.

    Args:
        request (FixtureRequest): The fixture request object.
    """
    # Setup
    os.makedirs(SOURCE_FOLDER, exist_ok=True)
    os.makedirs(REPLICA_FOLDER, exist_ok=True)

    def teardown() -> None:
        # Teardown
        shutil.rmtree(SOURCE_FOLDER)
        shutil.rmtree(REPLICA_FOLDER)

        assert not os.path.exists(SOURCE_FOLDER)
        assert not os.path.exists(REPLICA_FOLDER)

    # Register the teardown function to be called after tests
    request.addfinalizer(teardown)

@pytest.fixture(scope="function")
def folder_sync() -> FolderSynchronizer:
    """
    Fixture to provide a FolderSynchronizer instance for each test function.

    Returns:
        FolderSynchronizer: An instance of FolderSynchronizer.
    """
    return FolderSynchronizer(SOURCE_FOLDER, REPLICA_FOLDER, log)

def test_synchronize_nonexistent_source_folder() -> None:
    """
    Test synchronizing a non-existent source folder raises FileNotFoundError.
    """
    folder_sync_test = FolderSynchronizer('nonexistent_source', REPLICA_FOLDER, log)

    with pytest.raises(FileNotFoundError):
        folder_sync_test.synchronize()

def test_synchronize_create_replica_folder() -> None:
    """
    Test that the replica folder is created if it does not exist.
    """
    custom_replica_folder = 'custom_replica_folder'
    folder_sync_test = FolderSynchronizer(SOURCE_FOLDER, custom_replica_folder, log)

    folder_sync_test.synchronize()

    assert os.path.exists(custom_replica_folder)

    shutil.rmtree(custom_replica_folder)
    assert not os.path.exists(custom_replica_folder)

def test_synchronize_remove_folder(folder_sync) -> None:
    """
    Test that a folder in the replica that does not exist in the source is removed.
    """
    empty_folder = os.path.join(REPLICA_FOLDER, 'folder_removal/folder')
    os.makedirs(empty_folder)

    folder_sync.synchronize()

    assert not os.path.exists(empty_folder)

def test_synchronize_remove_file(folder_sync) -> None:
    """
    Test that a file in the replica that does not exist in the source is removed.
    """
    empty_folder = os.path.join(REPLICA_FOLDER, 'file_removal/folder/')
    os.makedirs(empty_folder)
    empty_file = os.path.join(empty_folder, 'file.txt')
    with open(empty_file, 'w', encoding='utf-8'):
        pass

    folder_sync.synchronize()

    assert not os.path.exists(empty_file)

def test_synchronize_create_folder(folder_sync) -> None:
    """
    Test that a folder in the source is copied to the replica.
    """
    folder_name = 'folder_creation/folder/folder'
    os.makedirs(os.path.join(SOURCE_FOLDER, folder_name))

    folder_sync.synchronize()

    assert os.path.exists(os.path.join(REPLICA_FOLDER, folder_name))

def test_synchronize_create_file(folder_sync) -> None:
    """
    Test that a file in the source is copied to the replica.
    """
    folder_name = 'file_creation/folder/folder/'
    os.makedirs(os.path.join(SOURCE_FOLDER, folder_name))
    file_name = folder_name + 'file.txt'
    with open(os.path.join(SOURCE_FOLDER, file_name), 'w', encoding='utf-8'):
        pass

    folder_sync.synchronize()

    assert os.path.exists(os.path.join(REPLICA_FOLDER, file_name))

def test_synchronize_update_file(folder_sync) -> None:
    """
    Test that a file in the replica is updated to match the source.
    """
    file_name = 'file.txt'
    content = 'test update file'
    with open(os.path.join(REPLICA_FOLDER, file_name), 'w', encoding='utf-8'):
        pass

    with open(os.path.join(SOURCE_FOLDER, file_name), 'w', encoding='utf-8') as f:
        f.write(content)

    folder_sync.synchronize()

    with open(os.path.join(REPLICA_FOLDER, file_name), 'r', encoding='utf-8', ) as f:
        assert f.read() == content
