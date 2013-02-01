# pygrate

Like migrate, but with py.  Yum.

## Design

Essentially, pygrate is a generalized differ with some nice specific diffing
algorithms for SQL databases.  I support the following operations:

    diff(state1, state2) # returns delta12
    python(delta12)      # returns function for applying delta12
    sql(delta12)         # returns SQL for applying delta12 (if possible)
    human(delta12)       # returns a string description of what delta12 does 