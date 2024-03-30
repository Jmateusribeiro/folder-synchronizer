# Folder Synchronizer

[![Unit Tests](https://github.com/Jmateusribeiro/folder-synchronizer/actions/workflows/test.yml/badge.svg?label=Unit%20Tests)](https://github.com/Jmateusribeiro/folder-synchronizer/actions/workflows/test.yml)

## Goal
    
    Implement a pythom program to perform folder synchronization
    
To implement folder synchronization, I selected 5 distinguished actions:
- Folder removal (Empty Folders);
- File removal;
- Folder creation (Empty Folders);
- File creation/copy;
- File update.

So with this actions in mind, I created a class to perform it. 
First I grouped these actions in two categories:
- Remove actions (*remove_items* method): because to perform these actions must iterate over replica folder
- Creation actions (*create_or_update_items* method): because to perform these actions must iterate over source folder

By the way, I started with remove actions because if we create items first, the remove task will iterate over more items.

A custom log class was created to handle both file and console log needs


## Dependencies and Execution

### Dependencies

On this task I didn't use external packages, so there is no external dependency. But I followed python good practices anyway and created *Requirements.txt* file

### Execution

The decision of whether to create a virtual env for executing the script is up to the user. In my case, I've created a virtual env, but I haven't committed it.

To run the program, it requires the following arguments:

- sourceDir: Complete directory path of the source folder.
- replicaDir: Complete directory path of the replica folder.
- logFolder: Complete directory path of the log folder.

Example of execution:

    python -m folder_synchronizer --sourceDir <sourceDir> --replicaDir <replicaDir> --logFolder <logFolder>


## Project Structure

The project was organized following the typical structure of a python package project, that's the reason to include a *setup.py* file.

To compile the package, execute the following command:

    python setup.py sdist bdist_wheel

this command generates a wheel and a tarball (.tar.gz) file of the version configured on the *setup.py*


## Tests

As a tester myself, I couldn't develop a project/script without including any tests. Therefore, I've created some unit tests under the *test* folder.

I don't strongly believe in achieving 100% coverage in unit tests, as it can lead to unnecessary time consumption in test implementation. Instead, I believe in focusing on the most crucial tests that can ensure the script works as expected. With this approach in mind, I've developed the following tests:

- Scenario 1: Source folder does not exist, should thrown error
- Scenario 2: Replica folder does not exist, should be created
- Scenario 3: Exists a Folder in Replica that does not exists on Source folder, should be removed
- Scenario 4: Exists a File in Replica that does not exists on Source folder, should be removed
- Scenario 5: A folder in Source is created, should be created as well in replica
- Scenario 6: A file in Source is created, should be created as well in replica
- Scenario 7: A file in Source is updated, should be updated as well in replica

To execute the tests, it can be used the pytest package with the simple command:

    python -m pytest -vv


## Final Notes
    
To make this task periodically, one may implement the "scheduler" on a CI/CD tool. For example, could be implemented a jenkins job to run the python program and that job can be schedule to execute periodically, out of the box.
- This approach would be a more scalable and manageable solution.
