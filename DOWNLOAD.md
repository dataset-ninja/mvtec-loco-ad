Dataset **MVTEC LOCO AD** can be downloaded in Supervisely format:

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/N/f/rA/UEdBjOjxjiMIYbqk4pV8AJjQJdW1RU5EznujSek0i3NpZxsg3V80u9mNYiZci0YIJ9xPr2TcLjr6mdHTosOtg0hKCq9JZNLHuZbVV790ls1fxYr5C2IjVtz4MePi.tar)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='MVTEC LOCO AD', dst_path='~/dtools/datasets/MVTEC LOCO AD.tar')
```
The data in original format can be 🔗[downloaded here](https://www.mvtec.com/company/research/datasets/mvtec-loco)