# TMKTThreader

## How to install it

```sh
pip install tmktthreader
```

## How to import it

```py
from tmktthreader import Threader
```

## How to use it

```py
@Threader
def my_func(*args, **kwargs):
    # do some stuff
    pass

my_func(myargs, mykwargs="")
```

> your function going to be a thread

> the function call return a Thread from ```threading```. So you can .join() it

```py
t = my_func(*args, **kwargs)
t.join()
```