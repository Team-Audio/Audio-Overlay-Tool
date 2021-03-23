<h1 align="center">Audio Overlay Tool</h1>


### Manual
```
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
```

### Examples
```
# generate 100 new samples with samples from "input" and put them in "output",
# use two samples per sample 
python aot.py input output 100 2

# same as above but take only files that start with "keyboard"
python aot.py input output 100 2 -f="keyboard.+"

# take 5 samples per sample
python aot.py input output 100 5

# generate 200 new samples
python aot.py input output 200 5

# take files that have the form "keyboard_acoustic_<3-digits>-<3-digits>-<3-digits>.wav"
# and take the last two 3 digit pairs from each file in the output filename
python aot.py input output 100 2 -f="(keyboard_acoustic_)\d\d\d-(.+)\.wav" -o="{a1}{a2}{b2}.wav"

```