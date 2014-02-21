import subprocess
from itertools import izip
import os
import time

sh_files = filter(lambda f: f[-3:] == '.sh', os.listdir('.'))
names = [os.path.splitext(i)[0] for i in sh_files]
out_files = [i + '.out' for i in names]

for sh_file, out_file in izip(sh_files, out_files):
    if not os.path.exists(out_file):
        break
    print sh_file + '.'*(50-len(sh_file)),
    t = time.time()
    sh_output = subprocess.check_output(['sh', sh_file])
    with open(out_file) as f:
        file_output = f.read()
    if file_output == sh_output:
        print "OK   ",
    else:
        print "FAILD",
    print '%.2fs' % (time.time() - t)
        

    
    
    
    
    


    
    

