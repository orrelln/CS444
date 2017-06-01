## The SLOB SLAB: Best-Fit Allocation Algorithm

#### Algorithm for Allocation (n)
Info sourced from [RIT](https://www.cs.rit.edu/~ark/lectures/gc/03_03_03.html)

```
size(block) = n + size(header)
# Scan free list for smallest block w/ nWords
smallest >= size(block) 

if block not found:
    Failure and collect garbage
elseif freeblock_nWords >= size(block) + threshold:
    # Split into a free block and an in-use block
    freeblock_nWords = freeblock_nWords - size(block)
    in_use_block_nWords = size(block)
    Return pointer to in-use block
else:
    Unlink block from free list
    Return pointer to block
```

Note: Threshold must be set to at least ``size(header) + 1`` to leave room for
the header and link.

The threshold can be set high to deal with fragmentation.

--

#### Comparing efficiency between First-Fit and Best-Fit Algorithms
