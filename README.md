# wordability-www

This is a ready example of using word2vec model generated by [wordability](https://github.com/nksoff/wordability).

## Run using gunicorn
```
gunicorn --log-level debug --workers 10 --bind 0.0.0.0:80 wordability:app
```

## Run single thread
```
python3 wordability.py
```
