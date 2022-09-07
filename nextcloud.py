from argparse import Namespace
from ast import keyword
from curses import keyname
from constructs import Construct, Node

from imports import k8s


class NextCloud(Construct):

    def __init__(self, scope: Construct, id: str):

        super().__init__(scope, id)

        k8s.KubePersistentVolumeClaim(self, 'PersistentVolumeClaim',
                                        metadata=k8s.ObjectMeta(name='app-pvc', namespace='next-cloud'), 
                                        spec=k8s.PersistentVolumeClaimSpec(
                                            access_modes=['ReadWriteOnce'], 
                                            resources=k8s.ResourceRequirements(requests={"storage": k8s.Quantity.from_string("50Gi")}),  
                                            storage_class_name='btrfs-rawfile'
                                        )
                                    )

        k8s.KubeDeployment(self, 'Deployment',
                            metadata=k8s.ObjectMeta(name='app', labels={'component':'app'}, namespace='next-cloud'), 
                            spec=k8s.DeploymentSpec(
                                selector=k8s.LabelSelector(match_labels={'component':'app'}),
                                replicas=1,
                                strategy=k8s.DeploymentStrategy(type='Recreate'), 
                                template=k8s.PodTemplateSpec(
                                    metadata=k8s.ObjectMeta(
                                        labels={'component':'app'}),
                                    spec=k8s.PodSpec(
                                        containers=[k8s.Container(
                                            name='app',
                                            image='nextcloud:apache', 
                                            image_pull_policy='Always', 
                                            ports=[k8s.ContainerPort(container_port=80)], 
                                            args=['--transaction-isolation=READ-COMMITTED', '--binlog-format=ROW', '--max-connections=1000'], 
                                            env=[
                                                k8s.EnvVar(name='MYSQL_DATABASE', value_from=k8s.EnvVarSource(secret_key_ref=k8s.SecretKeySelector(key='MYSQL_DATABASE', name='db-secrets'))),
                                                k8s.EnvVar(name='MYSQL_PASSWORD', value_from=k8s.EnvVarSource(secret_key_ref=k8s.SecretKeySelector(key='MYSQL_PASSWORD', name='db-secrets'))),
                                                k8s.EnvVar(name='MYSQL_ROOT_PASSWORD', value_from=k8s.EnvVarSource(secret_key_ref=k8s.SecretKeySelector(key='MYSQL_ROOT_PASSWORD', name='db-secrets'))),
                                                k8s.EnvVar(name='MYSQL_USER', value_from=k8s.EnvVarSource(secret_key_ref=k8s.SecretKeySelector(key='MYSQL_USER', name='db-secrets')))
                                            ],
                                            volume_mounts=[k8s.VolumeMount(mount_path='/var/www/html', name='app-persistent-storage')],
                                        )],
                                        restart_policy='Always', 
                                        volumes=[k8s.Volume(
                                            name='app-persistent-storage',
                                            persistent_volume_claim=k8s.PersistentVolumeClaimVolumeSource(claim_name='app-pvc'))]
                                    )   
                                )       
                            )
        )

        k8s.KubeService(
            self, 'service',
            metadata=k8s.ObjectMeta(name='app', labels={'component':'app'}, namespace='next-cloud'),
            spec=k8s.ServiceSpec(
                ports=[k8s.ServicePort(port=80)],
                selector={'component':'app'},
                type='NodePort'
            )
        )



       ## app-db, mount_path, image_name, spec_resources:50Gi, args-->variable image_pull_policydelkhah,  