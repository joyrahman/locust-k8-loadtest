from kubernetes import client, config
from kubernetes.client.rest import ApiException
from pprint import pprint
import time

def clusterSetup(api_instance, configs):
    for deployment, replicaCnt in configs.workflowDeplList.iteritems():
        # setup correct pod replica count for workflow deployments 
        try: 
            workflow_depl = api_instance.read_namespaced_deployment(
                name=deployment,
                namespace=configs.testNS,
                pretty='true',
                exact=True,
                export=True)

            workflow_depl.spec.replicas = int(replicaCnt)
            print("\nUpdating deployment %s with replicaCnt %d\n" % (deployment, workflow_depl.spec.replicas))
            updated_depl = api_instance.patch_namespaced_deployment(
                name=deployment,
                namespace=configs.testNS,
                body=workflow_depl)
            
            #check to confirm that replica cnt is now at correct amount
            ready = False
            for i in range(10):
                time.sleep(3)
                check_depl = api_instance.read_namespaced_deployment(
                    name=deployment,
                    namespace=configs.testNS,
                    pretty='true',
                    exact=True,
                    export=True)
                if check_depl.spec.replicas == int(replicaCnt):
                    print("--Deployment %s updated to replica cnt='%d'" % (updated_depl.metadata.name, updated_depl.spec.replicas))
                    ready = True
                    break

            if ready == False:    
                print("-- Deployment %s not able to be updated within 30sec! ---\n" % deployment)
        
        except ApiException as e:
            print("Exception when calling AppsV1Api->read_namespaced_deployment: %s\n" % e)

    # TODO: place interference deployment in correct zone w/ correct count
    namespace=configs.testNS 
    include_uninitialized = True # bool | If true, partially initialized resources are included in the response. (optional)
    pretty = 'pretty_example' # str | If 'true', then the output is pretty printed. (optional)
    dry_run = 'dry_run_example' # str | When present, indicates that modifications should not be persisted. An invalid or unrecognized dryRun directive will result in an error response and no further processing of the request. Valid values are: - All: all dry run stages will be processed (optional)
    body = create_batch_job_spec(10,configs.interferenceLvl,configs.interferenceZone, configs.interferenceType)
    try: 
        api_response = api_instance.create_namespaced_job(namespace, body, include_uninitialized=include_uninitialized, pretty=pretty, dry_run=dry_run)
        pprint(api_response)
    except ApiException as e:
        print("Exception when calling BatchV1Api->create_namespaced_job: %s\n" % e)




    
def create_batch_job_spec(cntCompletions=10,cntParallelism=2,zone="red",jobType="memory"):
    body = client.V1Job() # V1Job | 
    print(body)
    body.kind = "Job"
    body.spec.parallelism = cntParallelism
    body.spec.completions = cntCompletions
    #TODO: Remove ""
    if joyType=="" or jobType=="memory":
        body.metadata.name  = "stream"
        body.spec.template.metdata.name = "stream-pod"
        body.spec.template.spec.containers.name = "stream-container"
        body.spec.template.spec.containers.image = "joyrahman/stream3:v8"
    
    zoneSelector = dict()
    #TODO: remove zone null check
    if zone is None:
        zone == "red"
    zoneSelector['color'] = zone
    body.spec.template.spec.node_selector = zoneSelector

    return body





    

