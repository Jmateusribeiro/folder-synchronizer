import os
import shutil
from unittest.mock import Mock
import pytest
from folder_synchronizer.classes.folder_operations import FolderSynchronizer

source_folder = 'test_source_folder'
replica_folder = 'test_replica_folder'
log = Mock()


@pytest.fixture(scope="module", autouse=True)
def create_folders(request):
    
    #set up
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(replica_folder, exist_ok=True)

    def teardown():
        # Teardown code
        shutil.rmtree(source_folder)
        shutil.rmtree(replica_folder)

        assert not os.path.exists(source_folder)
        assert not os.path.exists(replica_folder)
    
    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def folder_sync():
    return FolderSynchronizer(source_folder, replica_folder, log)


def test_synchronize_nonexistent_source_folder():

    folder_sync = FolderSynchronizer('nonexistent_source', replica_folder, log)

    with pytest.raises(FileNotFoundError):
        folder_sync.synchronize()


def test_synchronize_create_replica_folder():
     
    custom_replica_folder = 'custom_replica_folder'
    folder_sync = FolderSynchronizer(source_folder, custom_replica_folder, log)

    folder_sync.synchronize()

    assert os.path.exists(custom_replica_folder)
    
    shutil.rmtree(custom_replica_folder)
    assert not os.path.exists(custom_replica_folder)


def test_synchronize_remove_folder(folder_sync):

    # Create a folder in replica folder (to be removed by 'synchronize' method)
    empty_folder = os.path.join(replica_folder, 'folder_removal/folder')
    os.makedirs(empty_folder)

    folder_sync.synchronize()

    assert not os.path.exists(empty_folder)


def test_synchronize_remove_file(folder_sync):

    # Create a file replica folder (to be removed by 'synchronize' method)
    empty_folder = os.path.join(replica_folder, 'file_removal/folder/')
    os.makedirs(empty_folder)
    empty_file = os.path.join(empty_folder, 'file.txt')
    open(empty_file, 'w').close()

    folder_sync.synchronize()

    assert not os.path.exists(empty_file)


def test_synchronize_create_folder(folder_sync):

    folder_name = 'folder_creation/folder/folder'
    # Create a folder in the source folder (to be coppied by 'synchronize' method)
    os.makedirs(os.path.join(source_folder, folder_name))

    folder_sync.synchronize()

    # Even though the folder was created on source
    # needs to be checked on the replica
    assert os.path.exists(os.path.join(replica_folder, folder_name))


def test_synchronize_create_file(folder_sync):

    # Create a file in the source folder (to be coppied by 'synchronize' method)
    folder_name = 'file_creation/folder/folder/'
    os.makedirs(os.path.join(source_folder, folder_name))
    file_name = folder_name + 'file.txt'
    open(os.path.join(source_folder, file_name), 'w').close()

    folder_sync.synchronize()

    # Even though the file was created on source
    # needs to be checked on the replica
    assert os.path.exists(os.path.join(replica_folder, file_name))


def test_synchronize_update_file(folder_sync):

    file_name = 'file.txt'
    content = 'test update file'
    # creat empty file in replica folder
    open(os.path.join(replica_folder, file_name), 'w').close()

    # create the same file in source folder but with content
    with open(os.path.join(source_folder, file_name), 'w') as f:
        f.write(content)

    folder_sync.synchronize()

    # Check if the file is updated in replica folder
    with open(os.path.join(replica_folder, file_name), 'r') as f:
        assert f.read() == content