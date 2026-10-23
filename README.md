# tokenizer-app
Sample application to test installation and usage of Python tokenizers library.

## Pre-requsites
1. Lighwell service account credentials
2. OpenShift cluster with Nexus running (RHDP Lightwell Software Supply Chain Security Workshop)


## Setup
1. Update credentials in 
```credentials_dummy.yaml```, rename locally to ```credentials.yaml```

2. Connect to cluster  
```
oc login ...
``` 

3. Apply secrets on cluster  
``` 
oc apply -f credentials.yaml
```

4. Deploy pod on cluster with Python environment
```
oc apply -f python-shell-pod.yaml
```

## Demo-1: Direct Lightwell repo access
1. Open the Terminal tab for the ```python-shell-pod``` running in cluster.

2. Change directory and run ```pip```

```
$ cd 1_credentials.yaml
$ pip install -r requirements-lightwell.txt
```

```pip``` will install ```tokenizers==0.23.1``` directly from lightwell validated and remidiated repositories and select the latest version based on the suffix  ```tokenizers==0.23.1+rhlw.1```

3. Run tokenizer app to check if the ```tokernizers==0.23.1``` is working as expected

```
$ python tokenizer.py "This is a test sentence."
package: tokenizers 0.23.1+rhlw.1
tokenizer: bert-base-uncased
vocab: 30522
characters: 24
tokens: 8

   0  101       '[CLS]'
   1  2023      'this'
   2  2003      'is'
   3  1037      'a'
   4  3231      'test'
   5  6251      'sentence'
   6  1012      '.'
   7  102       '[SEP]'
```

## Demo-2: Use Nexus to proxy the Lightwell repo
1. Create proxy repos for each of Lightwell validated and remediated repos, e.g. ```lw-py-validated```, ```lw-py-remediated``` 

2. Open the Terminal tab for the ```python-shell-pod``` running in cluster.

3. Change directory and update repo paths in ```requirements-nexus.txt```
```
cd 2_proxy_rhlw_repo
```

4. Run pip to use Nexus as an in-cluster cached proxy to Lightwell repositories

```
pip install -r requirements-nexus.txt
```

5.  Run tokenizer app to check if the ```tokernizers==0.23.1``` is working as expected
```
$ python tokenizer.py "This is another test sentence."
package: tokenizers 0.23.1+rhlw.1
tokenizer: bert-base-uncased
vocab: 30522
characters: 30
tokens: 8

   0  101       '[CLS]'
   1  2023      'this'
   2  2003      'is'
   3  2178      'another'
   4  3231      'test'
   5  6251      'sentence'
   6  1012      '.'
   7  102       '[SEP]'
```

### Demo-3: Use Lightwell API 

TBD



## Directory structure

```text
tokenizer-app/
├── README.md           # This file
├── python-shell-pod.yaml        # OpenShift pod, app files, and Nexus proxy auth job
├── credentials_dummy.yaml        # Template file for credentials
├── 1_direct_rhlw_repo/ 
│   ├── tokenizer.py                # CLI that tokenizes text with Hugging Face tokenizers
│   └── requirements-lightwell.txt   # pip install directly from packages.redhat.com
├── 2_proxy_rhlw_repo/
│   ├── tokenizer.py                # CLI that tokenizes text with Hugging Face tokenizers
│   └── requirements-nexus.txt       # pip install through the in-cluster Nexus proxy
└── 3_rhlw_api_usage/
```
