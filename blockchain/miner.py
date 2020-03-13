import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random


def proof_of_work(last_proof, time_limit):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...AE9123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    """
    This mining algorithm uses a couple tricks to speed up mining.
    1. It only computes the matching condition once.
    2. It prepends a (probably) unique string to randomize the search.
    3. It stops mining after a time limit, which is set dynamically based
        on past late submissions.
    """

    start = timer()
    print("last proof:", last_proof)
    print("Searching for next proof")
    guess = f'{last_proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    match = str(guess_hash)[-6:]
    proof = 0
    while not valid_proof(proof, match):
        if timer() - start > time_limit:
            return None, None
        proof += 1
    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return "GOOGLE_JURY_NULLIFICATION"+str(proof), timer() - start


def valid_proof(proof, match):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the hash of the last proof match the first six characters of the hash
    of the new proof?

    IE:  last_hash: ...AE9123456, new hash 123456E88...
    """
    guess = f'GOOGLE_JURY_NULLIFICATION{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == match

if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    time_limit = 20
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof, proof_time = proof_of_work(data.get('proof'), time_limit)
        if new_proof == None:
            continue

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            time_limit = min(time_limit, proof_time)
            print(data.get('message'))
            print("new time limit:", time_limit)
