# tokenizer-app
Sample application to test installation and usage of Python tokenizers library.

## Directory structure

```text
tokenizer-app/
├── README.md           # This file
├── python-shell-pod.yaml        # OpenShift pod, app files, and Nexus proxy auth job
├── 1_direct_rhlw_repo/
│   ├── tokenizer.py                # CLI that tokenizes text with Hugging Face tokenizers
│   └── requirements-lightwell.txt   # pip install directly from packages.redhat.com
├── 2_proxy_rhlw_repo/
│   ├── tokenizer.py                # CLI that tokenizes text with Hugging Face tokenizers
│   └── requirements-nexus.txt       # pip install through the in-cluster Nexus proxies
└── 3_rhlw_api_usage/
```

