: true_block 10 . ;
: false_block 11 . ;
1 1 - ?0 if true_block else false_block fi
2 1 - ?0 if true_block else false_block fi

1 1 - ?0 if 12 . else 13 . fi
2 1 - ?0 if 12 . else 13 . fi
