"""Audio Overlay Tool
Usage:
    aot.py <input_dir> <output_dir> <num_generate> <samples_per_sample> [options]

Options:
    -f RGX --filter=RGX      a filter for selecting the input files from the input directory.
    -o FMT --outfmt=FMT      Output format of the files (file a information in {a+cg} file b information in {b+cg}
                             For Example:
                             a=bass-something.wav b=bass-something_else.wav c=...
                             filter=(bass)-(.+)(\.wav)
                             outfmt=remixed-{a1}-{a2}+{b2}{a3}
                             then result => remixed-bass-something+something_else.wav
                             Note that a0 and b0 are the full match.

    -h --help                Show this screen.
    --version                Show version.

"""
import asyncio
from docopt import docopt
from driver import Remixer


async def main():
    arguments = docopt(__doc__, version="0.0.1-alpha0")
    driver = Remixer(args=arguments)
    await driver.run()


if __name__ == "__main__":
    asyncio.run(main())
