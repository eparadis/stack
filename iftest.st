: true_block 10 peek ;
: false_block 11 peek ;
1 1 - ?0 if true_block else false_block fi
2 1 - ?0 if true_block else false_block fi

1 1 - ?0 if 12 peek else 13 peek fi
2 1 - ?0 if 12 peek else 13 peek fi
