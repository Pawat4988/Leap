from dwave.system import DWaveSampler, EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler())

sampleset = sampler.sample_ising({'a': 1}, {('a', 'b'): 1})

print(sampleset.info["timing"])  