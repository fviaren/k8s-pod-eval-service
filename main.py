from kubernetes import client, config
from kubernetes.client.rest import ApiException
from datetime import datetime, timedelta


# API
def get_cluster_data():
    try:
        config.load_kube_config()
        v1 = client.CoreV1Api()
        pods_complete_list = v1.list_pod_for_all_namespaces(watch=False)
        pods_list = []
        for i in pods_complete_list.items:
            pod = dict()
            pod['name'] = i.metadata.name
            pod['labels'] = i.metadata.labels
            pod['image'] = i.spec.containers.image
            pod['start_time'] = i.status.start_time
            pods_list.append(pod)
        return pods_list
    except ApiException as e:
        raise e


# DATA EVAL LOGIC
def evaluate_image_prefix(img_name: str):
    return img_name.startswith('bitnami/')


def evaluate_label_team(labels: dict):
    return 'team' in labels and labels['team'] != ''


def evaluate_start_time(start_time: datetime):
    return datetime.now() - start_time < timedelta(days=7)


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


def evaluate_pods(pods_list: list):
    cluster_evaluation = []
    for pod in pods_list:
        cluster_evaluation.append(evaluate_pod(pod))
    return cluster_evaluation


# INTERFACE/OUTPUT
def output_evaluation():
    pods_list = get_cluster_data()
    cluster_eval = evaluate_pods(pods_list)
    for pod_eval in cluster_eval:
        print(pod_eval)


if __name__ == "__main__":
    output_evaluation()
