## Requirements

- Python 3.x
- Pip 3.x
- [GNU Make x.x]

```bash
pip3 install -r requirements.txt
```

## Run

```bash
python3 main.py path/to/impulse/responses/dir path/to/dry/signals/dir [path/to/output/dir]
```

or as a script

```bash
chmod 744 main.py
./main.py path/to/impulse/responses/dir path/to/dry/signals/dir [path/to/output/dir]
```

## Demo

```bash
make run
```

## Clean

```bash
make clean
```

or even

```bash
make cleanall
```

although this is not necessary, notably to keep *_\_pycache__* directories alive

## JSON Syntax

```json
{
	"drypath0": "wetdirpath0",
	"drypath1": "wetdirpath1",
	"drypath2": "wetdirpath2",
	...
}
```

each path to a dry signal is a key to the directory path that contains all of its wet samples
