# yack

Yack is yet another k-mer counter, designed for fast and lightweight counting of short k-mers (up to 31bp).

# Install

```
pip install yack
```

or install this from the github:

```
wget https://github.com/arriam-lab2/yack/archive/v0.1.2.tar.gz
tar xzf v0.1.2.tar.gz
rm v0.1.2.tar.gz
cd yack-0.1.2
python setup.py install
```

# Usage


## CLI application

```
yack count -k 25 INPUT_FILE --hist
```

## API

See `examples` folder for an example of usage yack as a python module.
