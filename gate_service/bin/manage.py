#
# This is Python script that will be launched after gmanager
# set ups everything correctly.
#
# The CLI paramteres are passes as-is
#
import sys
from subprocess import Popen
import glob
import os
import inspect
import shutil
import time

#
# Run all available unit tests
#
def run_tests():
  print('[i] Will now launch tests')
  processes = []
  processes.append(Popen('python -m xmlrunner discover -s tests -p "test_*.py"', shell=True))
  for process in processes:
    process.wait()
    
  # Copy the xmp files
  dest_dir = "../test-results"
  glob_path = os.path.join(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
    '..',
    '*.xml'
  )
  dest_path = os.path.join(
    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))),
    '..',
    'test-results'
  )
  
  shutil.rmtree(os.path.abspath(dest_path))
  time.sleep(0.1)
  
  destDirCreated = True
  try:
    os.mkdir(os.path.abspath(dest_path))
  except:
    # Nothing meaningful
    destDirCreated = False
  
  for file in glob.glob(glob_path):
      obj_src = os.path.abspath(file)
      obj_dest = os.path.abspath(os.path.join(
        dest_path,
        'gate_service.xml'
      ))
      shutil.copy(obj_src, obj_dest)
      os.unlink(obj_src)

if __name__ == "__main__":

  if len(sys.argv) < 3:
    raise "The number of command line paramteres must be at least 3. Please run this script using gmanager"
    
  if len(sys.argv) < 4:
    raise "Must specify manage.py command."
    
  command = sys.argv[3]
  if command == 'test':
    run_tests()
  else:
    raise "Invalid command was specified!"

