import os
import random

from filter import Filter
from utils import is_file_in_dir, ensure_folder, merge_audio


class Remixer:

    def __init__(self, args):

        # get how many samples we need to generate
        self.to_generate = int(args['<num_generate>'])
        print("Generating:", self.to_generate)

        # get the input directory
        self.in_dir = args['<input_dir>']
        print("Input:", self.in_dir)

        # get the output directory
        self.out_dir = args['<output_dir>']
        print("Output:", self.out_dir)

        # samples per sample
        self.samples_per_sample = int(args['<samples_per_sample>'])
        print("Samples to take:", self.samples_per_sample)

        if self.samples_per_sample > 12:
            print("WARNING: possibly wrong input format! more than 12 samples/sample specified")
            print("Clamping to 12")
            self.samples_per_sample = 12

        self.filter_driver = Filter(args['--filter'] if '--filter' in args else None,
                                    args['--outfmt'] if '--outfmt' in args else None)

        print(self.filter_driver)

        # get all files in input dir
        self.file_collection = self.iterate_directory(self.in_dir)

    def select_some(self, N):
        # copy the input directory collection
        # select some
        return random.sample(self.file_collection[:], N)

    # gets all files in a directory and checks it against the filter
    def iterate_directory(self, path):
        return [(x, path) for x in os.listdir(path)
                if is_file_in_dir(x, path)
                and self.filter_driver.good(x)]

    def run(self):

        ensure_folder(self.out_dir)

        for i in range(self.to_generate):
            [x, *rest] = self.select_some(self.samples_per_sample)

            # based on the filter and the outfmt
            # we need to create the output filename
            # here
            out_name = self.filter_driver.pattern_replace([y[0] for y in [x] + rest])

            merge_audio(os.path.join(*x[::-1]), *[os.path.join(*p[::-1]) for p in rest],
                        out=os.path.join(self.out_dir, out_name))
