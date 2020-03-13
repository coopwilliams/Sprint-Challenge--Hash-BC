#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    for i, x in enumerate(weights):
        hash_table_insert(ht, x, i)

    # pick weight below limit
    for i_1, weight_1 in enumerate(weights):
        if weight_1 > limit:
            pass
        # get the index of its complement from the hashtable
        i_2 = hash_table_retrieve(ht, limit-weight_1)
        if i_2 is not None:
            return i_2, i_1
    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
