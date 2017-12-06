if __name__ == "__main__":
    raise RuntimeError()
else:
    import os
    from ctypes import cdll, POINTER, c_uint8, c_uint64, c_size_t, c_int
    

    def find_lib(directory, prefix):
        for name in os.listdir(directory):
            fullname = os.path.join(directory, name)
            if os.path.isfile(fullname) and name.startswith(prefix) \
                    and name.endswith("so"):
                return fullname

        raise ValueError("Library '%s' not found" % prefix)


    libdir = os.path.dirname(os.path.abspath(__file__))
    ranklib = cdll.LoadLibrary(find_lib(libdir, "rank"))
    ranklib.count_kmer_ranks.argtypes = [POINTER(c_uint8), POINTER(c_uint64), c_size_t, c_int]
