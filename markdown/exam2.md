---
title: Exam 2
...

# The Exam

Exam 2 was given in class on Monday 1 April, 2019.
The PDF of the exam is available [here](files/s2019exam2.pdf).
You can find your individual responses on the submission page.

Stat        Exam 1       Exam 2
------      -------      -------
High        91.1%        93.1%
Median      80.6%        77.8%
Mean        78.6%        76.0%
Low         54.8%        52.2%
StdDev       9.6%        11.3%

A few notes that may not be evident from the uploads:

- The full-page **Q11** was worth 4 points,
    though you'll see a normalized (out of 1) score displayed if you missed points on it.
    Most points were for avoiding serious errors like failing to unlock what you lock or having some threads wait on more barriers than others.
    
    Comments of the kinds of errors I found (if any) in your Q11 solution are included in comments after your solution
- **Q17.5** I dropped as ambiguous
- **Q18** I did read all your work, but did not transcribe it.
    Half the points were for computing the block size,
    half for setting those bits to 1 in your answer.

# Wrapping-up the Exam Experience

On or before Friday 12 April, you may submit an exam wrapper^[See [the teaching commons](https://teachingcommons.stanford.edu/teaching-talk/exam-wrappers) for a decent introduction to the idea of an exam wrapper.] to make up some of your lost points. This should be a plain-text document named `exam2wrap.txt` containing the following sections:

1. Preparation

    Reflect on how you prepared for the exam and how effective that was.
    Don't limit yourself to the days immediately before the exam; how effective were you approaches to learning the material as the semester progressed as well?

2. Errors
    
    List each mistake you made on the exam, and explain the correct answer.
    If possible, also explain why you answered incorrectly: what confused you?
    
    If there are questions you got right, but based on the wrong reasoning, explain those too.

3. Plans
    
    Wrap-up this exam experience by planning what you'll do differently in the future.

An example template might be:


```
Preparation
===========

I prepared for this exam by ...

I thought this was good/bad because ...


Errors
======

I missed Q17.4. The correct answer is ... because ...


Plans
=====

To improve my learning going forward, I plan to ...
```

If you do not submit a wrapper, your initial exam score will stand as your exam performance. If you do, that score can only go up, not down.

# Key

+--------+---------------------------------------------------------------------+
|Question|Key                                                                  |
+========+=====================================================================+
|Q1      | (x>>(P+(P-3)*(L-1)))&((1<<(P-3))-1)                                 |
+--------+---------------------------------------------------------------------+
|Q2      | 4                                                                   |
+--------+---------------------------------------------------------------------+
|Q3      | 3                                                                   |
+--------+---------------------------------------------------------------------+
|Q4      | 1                                                                   |
+--------+---------------------------------------------------------------------+
|Q5      | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q6      | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q7      | 1                                                                   |
+--------+---------------------------------------------------------------------+
|Q8      | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q9      | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q10     | 1                                                                   |
+--------+---------------------------------------------------------------------+
|Q11     | lock `m1` between `if` and `while`;                                 |
|        | unlock `m1` after `primes[num_primes++] = i;` and before next `}`   |
+--------+---------------------------------------------------------------------+
|Q12     | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q13     | 1 or 3 (can argue either way)                                       |
+--------+---------------------------------------------------------------------+
|Q14     | `C(x, R(H(x)))`                                                     |
+--------+---------------------------------------------------------------------+
|Q15     | 1                                                                   |
+--------+---------------------------------------------------------------------+
|Q16     | 2                                                                   |
+--------+---------------------------------------------------------------------+
|Q17     | True<br/>True<br/>False<br/>True<br/>True<br/>False                 |
+--------+---------------------------------------------------------------------+
|Q18     | `0x1003F`                                                           |
+--------+---------------------------------------------------------------------+
|Q19     | False<br/>False<br/>True<br/>True                                   |
+--------+---------------------------------------------------------------------+
