# Docker Manager 
Used to create, run, and remove docker images from connected machines.

## Implementation
Custom or Official docker images are implemented by creating a subclass of BaseBlueprint. This requires support for **create(), start(), stop(), and get_structure()**.

## Class
**BaseBlueprint**: 
Uses DockerSDK to manage docker containers on a remote machine
- **start()** starts Docker container as described by subclass' create() method. Has implementation, can be overriden
- **stop()** stops and removes docker container(will be updated to only stop in the future).
- **create()** builds an image to a remote machine. Since configuration can vary, BaseBlueprint does not implement it by default. 
- **get_structure()** Used to set configuration rules for the frontend. It must return the following structure:
    ```
    {
    "name": <project_name>, 
    "struct": {
        "machine_roles": [ // Can support many roles
            {
            "name": <role_name>, 
            "many":<bool> // can more than 1 machine use this role?
            }
            ]
        }
    }
    ```
    