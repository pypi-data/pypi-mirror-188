# RMOST

## Install
    $ pip install rmost
### Rtes
    from rmost import rtes

    rtes.start("tests.txt")
    count_tests = 2
    
    
    def f():
        ...
    
    
    f()
    rtes.run(f, count_tests)
    rtes.finish()
