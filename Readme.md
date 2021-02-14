k8s-pod-eval-service
====================
A showcase microservice to watch for pods in kubernetes cluster and evaluate them according to a set of rules.

# Features
- Use of [kubernetes official API library](https://github.com/kubernetes-client/python) to get cluster status data
- Reshape data to fit specific requirements
- Evaluate specific conditions on pods status
- Output evaluation of pods in stdout, one line per pod
- Watch for changes in status, printing new line of updated pod
- Optional arguments for namespace and timeout
- Run locally or deploy to cluster

# How to test locally
This service can be tested locally manually against a configured
kubernetes cluster (local using minikube or kind or remote one)
by simply cloning and running main.py python script directly:

1. Make sure you are using python3

2. Clone this repository
```bash
git clone git@github.com:fviaren/k8s-pod-eval-service.git

```
3. Install dependencies
```bash
pipenv install
```
4. Run locally
```bash
pipenv run python main.py --namespace 'optional-namespace' --tmosec optional-timeout-seconds
```
or
```bash
pipenv run python main.py -n 'optional-namespace' -t optional-timeout-seconds
```
5. To run unit test
```bash
pipenv run python evaluate_pods_test.py
```
or
```bash
pipenv run python -m unittest evaluate_pod_test.py
```


# How to deploy




# TODOs
- [ ] Deploy - dockerfile, test deployment and readme
- [ ] Rule modules as arguments
- [ ] Test to create and delete cluster and pods
