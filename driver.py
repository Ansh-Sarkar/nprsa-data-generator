import time
import tracemalloc
from nprsa import *
from csv import writer

if __name__ == '__main__':

    CSV_HEADER = ['nbits', 'nprimes', 'msgsize', 'spawnTime', 'encrTime', 'decrTime', 'memory']
    CONFIG_TEMPLATE = {
        "nbits": None,
        "nprimes": None,
        "prime_generator": prime_list_generator,
        "multiplier": multiplier,
        "totient": totient
    }

    result = open('nprsa.csv', 'a+')
    writerObj = writer(result)
    writerObj.writerow(CSV_HEADER)
    result.close()

    nBits, NBITS_INCR, nPrimes, NPRIMES_INCR, msgSize, MSG_SIZE_INCR = 0, 8, 2, 1, 8, 8
    NBITS_UL, MSG_UL, MAX_INITIALIZATION_TRIES, PRIMES_EXHAUSTED = 512, 32, 10, False

    for nbits in range(nBits, NBITS_UL + 1, NBITS_INCR):
        NPRIMES_UL = 2 * nbits

        for nprimes in range(nPrimes, NPRIMES_UL + 1, NPRIMES_INCR):

            print("Spawning Model . . . ")

            clk_model_gen_start = time.time()

            CONFIG_TEMPLATE['nbits'] = nbits
            CONFIG_TEMPLATE['nprimes'] = nprimes

            model = NPRSA(CONFIG_TEMPLATE)

            for _ in range(MAX_INITIALIZATION_TRIES):
                if not model.initialized: model.initialize()
                else: break
                
            if not model.initialized:
                PRIMES_EXHAUSTED = True
                break

            clk_model_gen_end = time.time()

            print("Model Initialized :", model)
            
            for msgsize in range(msgSize, MSG_UL + 1, MSG_SIZE_INCR):

                result = open('nprsa.csv', 'a+')
                writerObj = writer(result)

                tracemalloc.start()

                msg = nBitRandom(msgsize)
                print("Plaintext :", msg)

                clk_encr_start = time.time()
                CT = model.encrypt(msg)
                print("Encrypted :", CT)
                clk_encr_end = time.time()

                clk_decr_start = time.time()
                PT = model.decrypt(CT)
                print("Decrypted :", PT)
                clk_decr_end = time.time()

                memory = tracemalloc.get_tracemalloc_memory() / (1024 * 1024)
                tracemalloc.clear_traces()
                tracemalloc.stop()

                encr_time = clk_encr_end - clk_encr_start
                decr_time = clk_decr_end - clk_decr_start
                model_gen_time = clk_model_gen_end - clk_model_gen_start

                # nbits, nprimes, msgsize, spawnTime, encrTime, decrTime, memory
                row = [nbits, nprimes, msgsize, model_gen_time, encr_time, decr_time, memory]
                writerObj.writerow(row)
                result.close()

                print("\n\n")
    
    result.close()