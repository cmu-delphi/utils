"""
Extracts tar and zip files.

Extraction is done using python built-ins, and all the usual compression
schemes are supported. Some basic safety/sanity checks are performed before
extraction.

Typical usage:
````
from extractor import Extractor

filename, destdir = 'somefile.tgz', 'some/dest/str'
Extractor.extract(filename, destdir)
````
"""

# standard library
import argparse
import tarfile
import zipfile


class Extractor:
  """Convenience class with static method for extracting tar and zip files."""

  @staticmethod
  def _check_type(item):
    """Check that the tar entry is either a directory or a file."""
    if not item.isdir() and not item.isfile():
      raise Exception('item is neither dir nor file [%s]' % item.name)

  @staticmethod
  def _check_name(name):
    """Check that the name looks like a reasonable path."""
    if name[:1] == '/' or '..' in name:
      raise Exception('member name is invalid [%s]' % name)
    print('  %s' % name)

  @staticmethod
  def _open_tar(filename, destdir):
    """Open a tar file."""
    def check(member):
      Extractor._check_type(member)
      Extractor._check_name(member.name)
    tf = tarfile.open(filename)
    return tf, tf.getmembers(), check

  @staticmethod
  def _open_zip(filename, destdir):
    """Open a zip file."""
    zf = zipfile.ZipFile(filename)
    return zf, zf.namelist(), Extractor._check_name

  @staticmethod
  def extract(filename, destdir):
    """
    Extract the contents of the given file into the given directory.

    The destination directory will be created if it doesn't already exist.
    Existing files, if present, will be silently overwritten.
    """

    # determine file type
    if tarfile.is_tarfile(filename):
      open_func = Extractor._open_tar
    elif zipfile.is_zipfile(filename):
      open_func = Extractor._open_zip
    else:
      # this file can't be extracted
      raise Exception('neither a tar nor zip file [%s]' % str(filename))

    # open the file
    container, items, check = open_func(filename, destdir)

    # check its contents
    print('extracting %s:' % filename)
    for item in items:
      check(item)

    # finally, extract it
    container.extractall(destdir)
    print('done')


def main():
  """Command line usage."""

  # args and usage
  parser = argparse.ArgumentParser()
  parser.add_argument(
    'filename',
    type=str,
    help='a tar or zip file to extract'
  )
  parser.add_argument(
    'destdir',
    type=str,
    help='the output directory'
  )
  args = parser.parse_args()

  # extract the file
  Extractor.extract(args.filename, args.destdir)


if __name__ == '__main__':
  main()
