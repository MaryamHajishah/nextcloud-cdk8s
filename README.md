# nextcloud-cdk8s
Simple Nextcloud deployment with cdk8s.


## How to use
1. Download [cdk8s](https://cdk8s.io/docs/latest/getting-started/) cli and set-up the environment as the instruction in its document.  
3. Clone the project.
4. Edit the global variables in ```settings.py``` and ```mariadb_credentials.json```. Edit other values like storage resource and storage class in the code!
4. Generate the manifest file with ```cdk8s synth```.
5. Create the namespace and storageclass in your cluster. 

Resources are located in ```dist``` can now be deployed on Kubernetes. 
