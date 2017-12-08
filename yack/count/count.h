#include <cstdint>
#include <cstddef>
#include <string>
#include <vector>
#include <utility>
#include <flat_hash_map.hpp>

typedef std::vector<std::pair<uint64_t, uint64_t>> hist;
typedef ska::flat_hash_map<uint64_t, uint64_t> SparseHashMap;


class KmerCounter
{
public:
    void count(uint64_t kmer_ref)
    {
        map[kmer_ref] += 1;
    }

    hist values() const
    {
        return hist(map.begin(), map.end());
    }

    size_t size() const
    {
        return map.size();
    }

private:
    SparseHashMap map;
};


uint64_t ipow(uint64_t base, uint64_t exp)
{
    uint64_t result = 1;
    while (exp)
    {
        if (exp & 1)
        {
            result *= base;
        }

        exp >>= 1;
        base *= base;
    }

    return result;
}

const ska::flat_hash_map<char, uint8_t> alphabet {
    std::make_pair('A', 0),
    std::make_pair('a', 0),
    std::make_pair('C', 1),
    std::make_pair('c', 1),
    std::make_pair('G', 2),
    std::make_pair('g', 2),
    std::make_pair('T', 3),
    std::make_pair('t', 3)
};

char reverse_alphabet[] { 'A', 'C', 'G', 'T' };

std::vector<std::vector<uint8_t>> transform(const std::string& sequence)
{
    std::vector<std::vector<uint8_t>> out(1);

    size_t i = 0;
    for (auto c : sequence)
    {
        if (auto it = alphabet.find(c); it != alphabet.end())
        {
            out[i].push_back(it->second);
        }
        else
        {
            i += 1;
            out.emplace_back();
        }
    }

    return out;
}

std::string to_kmer(uint64_t rank, size_t kmer_size)
{
    std::vector<char> result;
    while (rank > 0)
    {
        result.push_back(reverse_alphabet[(uint8_t) (rank % 4)]);
        rank /= 4;
    }

    for (size_t i = result.size(); i < kmer_size; ++i)
    {
        result.push_back(reverse_alphabet[0]);
    }

    return std::string(result.rbegin(), result.rend());
}

std::vector<uint64_t> kmer_ranks(const std::vector<uint8_t>& in, const size_t k)
{
    const uint64_t m = 4;
    const size_t n = in.size();

    if (n < k)
    {
        return std::vector<uint64_t>();
    }

    std::vector<uint64_t> out(n - k + 1);
    out[0] = 0;
    for (size_t i = 0; i < k; ++i)
    {
        out[0] += in[i] * ipow(m, k-i-1);
    }

    for (size_t i = 1; i < n - k + 1; ++i)
    {
        out[i] = m * (out[i-1] - in[i-1] * ipow(m, k - 1)) + in[i+k-1];
    }
    return out;
}

hist count(const std::vector<std::string>& seqs, const size_t kmer_size, const size_t num_bins)
{
    const size_t pow4 = ipow(4, kmer_size);
    const uint64_t bin_step = (uint64_t)(pow4 / num_bins) + 1;
    std::vector<std::vector<uint64_t>> bins(num_bins);

    // distribute k-mers between bins
    std::vector<std::vector<uint64_t>> ranks;
    for (auto seq : seqs)
    {
        for (auto subseq : transform(seq))
        {
            for (auto rank : kmer_ranks(subseq, kmer_size))
            {
                size_t i = (size_t)(rank / bin_step);
                bins[i].push_back(rank);
            }
        }
    }

    // count k-mers from every bin independently
    std::vector<hist> hists;
    for (auto bin : bins)
    {
        KmerCounter counter;
        for (auto rank : bin)
        {
            counter.count(rank);
        }

        hist values = counter.values();
        std::sort(values.begin(), values.end());
        hists.push_back(values);
    }

    // put it all together
    hist result;
    size_t memory = 0;
    for (auto h : hists)
    {
        memory += h.size();
    }
    result.reserve(memory);
    for (auto h : hists)
    {
        std::move(h.begin(), h.end(), std::back_inserter(result));
    }
    return result;
}