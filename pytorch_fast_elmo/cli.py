# pylint: skip-file
import cProfile, pstats, io

import fire
from pytorch_fast_elmo import utils, profile


class Main:

    def cache_char_cnn(  # type: ignore
            self,
            vocab_txt,
            options_file,
            weight_file,
            hdf5_out,
            max_characters_per_token=utils.ElmoCharacterIdsConst.MAX_WORD_LENGTH,
            cuda=False,
            batch_size=256,
    ):
        utils.cache_char_cnn_vocab(
                vocab_txt,
                options_file,
                weight_file,
                hdf5_out,
                max_characters_per_token,
                cuda,
                batch_size,
        )

    def profile_full(  # type: ignore
            self,
            mode,
            options_file,
            weight_file,
            cuda=False,
            cuda_synchronize=False,
            batch_size=32,
            warmup_size=20,
            iteration_size=1000,
            word_min=1,
            word_max=20,
            sent_min=1,
            sent_max=30,
            random_seed=10000,
            profiler=False,
            output_file=None,
    ):
        sstream = io.StringIO()

        if profiler:
            pr = cProfile.Profile()
            pr.enable()

        mean, median, stdev = profile.profile_full_elmo(
                mode,
                options_file,
                weight_file,
                cuda,
                cuda_synchronize,
                batch_size,
                warmup_size,
                iteration_size,
                word_min,
                word_max,
                sent_min,
                sent_max,
                random_seed,
        )

        sstream.write(f'Finish {iteration_size} iterations.\n')
        sstream.write(f'Mode: {mode}\n')
        sstream.write(f'Duration Mean: {mean}\n')
        sstream.write(f'Duration Median: {median}\n')
        sstream.write(f'Duration Stdev: {stdev}\n\n')

        if profiler:
            pr.disable()
            ps = pstats.Stats(pr, stream=sstream).sort_stats('cumulative')
            ps.print_stats()

        if output_file:
            with open(output_file, 'w') as fout:
                fout.write(sstream.getvalue())
        else:
            print(sstream.getvalue())


def main():  # type: ignore
    fire.Fire(Main)
