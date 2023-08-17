Dataset **MVTec LOCO AD** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/i/j/S0/k7sEYGBQuRJdIHLLO3P9TC1xFPsEyZhfRztlBnY10gHZrvujEWTwOHtVD2G9tH8BfouXCrxTJW1nkN45VWp5MbYykIhrsvjvf2dYDwUJPc9PuQq51J4my7j4uhdV.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MVTec LOCO AD', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.mvtec.com/company/research/datasets/mvtec-loco).