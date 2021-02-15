from kubernetes import client, config, watch
from kubernetes.client.rest import ApiException
from datetime import datetime, timedelta
import pytz
import getopt
import sys


# API
def watch_cluster_eval_pods(namespace=None, timeout_seconds=None):
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        w = watch.Watch()
        events = ''
        if namespace is None and timeout_seconds is None:
            events = w.stream(v1.list_pod_for_all_namespaces)
        elif namespace is None and timeout_seconds is not None:
            events = w.stream(v1.list_pod_for_all_namespaces, timeout_seconds=timeout_seconds)
        elif namespace is not None and timeout_seconds is None:
            events = w.stream(v1.list_namespaced_pod, namespace=namespace)
        elif namespace is not None and timeout_seconds is not None:
            events = w.stream(v1.list_namespaced_pod, namespace=namespace, timeout_seconds=timeout_seconds)
        pods_list = []
        for event in events:
            pod = dict()
            pod['name'] = event['object'].metadata.name
            pod['labels'] = event['object'].metadata.labels
            pod['image'] = event['object'].spec.containers[0].image
            pod['start_time'] = event['object'].status.start_time
            pods_list.append(pod)
            pod_evaluation = evaluate_pod(pod) 
            print(pod_evaluation)   
    except ApiException as e:
        raise e


# DATA EVAL LOGIC
def evaluate_image_prefix(img_name: str):
    return img_name.startswith('bitnami/')


def evaluate_label_team(labels: dict):
    return 'team' in labels and labels['team'] != ''


def evaluate_start_time(start_time: datetime):
    return datetime.now().replace(tzinfo=pytz.UTC) - start_time < timedelta(days=7)


def evaluate_pod(pod: dict):
    pod_evaluation = {
        'pod': pod['name'],
        'rule_evaluation': []
    }
    pod_evaluation['rule_evaluation'].append({
        'name': 'image_prefix',
        'valid': evaluate_image_prefix(pod['image'])
    })
    pod_evaluation['rule_evaluation'].append({
        'name': 'team_label_present',
        'valid': evaluate_label_team(pod['labels'])
    })
    pod_evaluation['rule_evaluation'].append({
        'name': 'recent_start_time',
        'valid': evaluate_start_time(pod['start_time'])
    })
    return pod_evaluation


if __name__ == "__main__":
    
    name_space = None
    timeout_secs = None
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:t:", ["namespace=", " ="])
    except getopt.GetoptError as err:
        print(err)
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", '--namespace'):
            name_space = arg
        elif opt in ("-t", '--tmosec'):
            timeout_secs = arg
    
    kwargs = dict(namespace=name_space, timeout_seconds=timeout_secs)
    
    watch_cluster_eval_pods(**{k: v for k, v in kwargs.items() if v is not None})