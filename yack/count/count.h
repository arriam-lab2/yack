#include <cstdint>
#include <cstddef>
#include <utility>
#include <vector>
#include "sparsepp/spp.h"

using spp::sparse_hash_map;

typedef spp::sparse_hash_map<uint64_t, uint64_t> SparseHashMap;

class KmerCounter
{
public:
    void count(uint64_t kmer_ref)
    {
        map[kmer_ref] += 1;
    }

    std::pair<std::vector<uint64_t>, std::vector<uint64_t>> values() const
    {
        std::vector<uint64_t> keys;
        std::vector<uint64_t> values;

        keys.reserve(size());
        keys.reserve(size());

        for (auto it = map.begin(); it != map.end(); ++it)
        {
            keys.push_back(it->first);
            values.push_back(it->second);
        }

        return std::make_pair(keys, values);
    }

    size_t size() const
    {
        return map.size();
    }

private:
    SparseHashMap map;
};


