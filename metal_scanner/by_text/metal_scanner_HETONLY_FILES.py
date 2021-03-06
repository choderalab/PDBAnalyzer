from __future__ import print_function
import multiprocessing as mp
import glob
import gzip

pdbpath = '/cbio/jclab/share/pdb/*/*.ent.gz'
ppn = 32
metal_name = 'ZN'

mdtraj_noload_pdbs = ['/cbio/jclab/share/pdb/ar/pdb2arf.ent.gz',
 '/cbio/jclab/share/pdb/ax/pdb2axd.ent.gz',
 '/cbio/jclab/share/pdb/bz/pdb1bzb.ent.gz',
 '/cbio/jclab/share/pdb/c2/pdb1c2n.ent.gz',
 '/cbio/jclab/share/pdb/ca/pdb2ca7.ent.gz',
 '/cbio/jclab/share/pdb/cb/pdb4cbo.ent.gz',
 '/cbio/jclab/share/pdb/cg/pdb4cg3.ent.gz',
 '/cbio/jclab/share/pdb/ci/pdb1cir.ent.gz',
 '/cbio/jclab/share/pdb/cm/pdb3cmy.ent.gz',
 '/cbio/jclab/share/pdb/co/pdb2con.ent.gz',
 '/cbio/jclab/share/pdb/ct/pdb2ctn.ent.gz',
 '/cbio/jclab/share/pdb/d6/pdb2d6b.ent.gz',
 '/cbio/jclab/share/pdb/da/pdb2da8.ent.gz',
 '/cbio/jclab/share/pdb/dt/pdb1dt7.ent.gz',
 '/cbio/jclab/share/pdb/dt/pdb1dtc.ent.gz',
 '/cbio/jclab/share/pdb/dw/pdb1dw4.ent.gz',
 '/cbio/jclab/share/pdb/dw/pdb1dwl.ent.gz',
 '/cbio/jclab/share/pdb/dy/pdb2dyd.ent.gz',
 '/cbio/jclab/share/pdb/dz/pdb1dz5.ent.gz',
 '/cbio/jclab/share/pdb/e0/pdb1e0h.ent.gz',
 '/cbio/jclab/share/pdb/f0/pdb2f03.ent.gz',
 '/cbio/jclab/share/pdb/f8/pdb1f8h.ent.gz',
 '/cbio/jclab/share/pdb/fc/pdb2fci.ent.gz',
 '/cbio/jclab/share/pdb/fn/pdb2fnb.ent.gz',
 '/cbio/jclab/share/pdb/g0/pdb2g0z.ent.gz',
 '/cbio/jclab/share/pdb/g3/pdb2g32.ent.gz',
 '/cbio/jclab/share/pdb/gn/pdb2gn0.ent.gz',
 '/cbio/jclab/share/pdb/h2/pdb2h2m.ent.gz',
 '/cbio/jclab/share/pdb/hc/pdb1hc0.ent.gz',
 '/cbio/jclab/share/pdb/hc/pdb1hcp.ent.gz',
 '/cbio/jclab/share/pdb/he/pdb2hem.ent.gz',
 '/cbio/jclab/share/pdb/hi/pdb4hir.ent.gz',
 '/cbio/jclab/share/pdb/hy/pdb2hyn.ent.gz',
 '/cbio/jclab/share/pdb/ib/pdb1iba.ent.gz',
 '/cbio/jclab/share/pdb/ic/pdb2icy.ent.gz',
 '/cbio/jclab/share/pdb/ie/pdb1iek.ent.gz',
 '/cbio/jclab/share/pdb/ie/pdb1iey.ent.gz',
 '/cbio/jclab/share/pdb/if/pdb1ify.ent.gz',
 '/cbio/jclab/share/pdb/ih/pdb2iha.ent.gz',
 '/cbio/jclab/share/pdb/ik/pdb1ikm.ent.gz',
 '/cbio/jclab/share/pdb/iu/pdb2iue.ent.gz',
 '/cbio/jclab/share/pdb/j1/pdb2j15.ent.gz',
 '/cbio/jclab/share/pdb/je/pdb2je4.ent.gz',
 '/cbio/jclab/share/pdb/jh/pdb1jhb.ent.gz',
 '/cbio/jclab/share/pdb/jm/pdb2jmo.ent.gz',
 '/cbio/jclab/share/pdb/jx/pdb2jxh.ent.gz',
 '/cbio/jclab/share/pdb/k4/pdb2k45.ent.gz',
 '/cbio/jclab/share/pdb/k5/pdb1k5k.ent.gz',
 '/cbio/jclab/share/pdb/k8/pdb1k81.ent.gz',
 '/cbio/jclab/share/pdb/kd/pdb1kde.ent.gz',
 '/cbio/jclab/share/pdb/kh/pdb2kh4.ent.gz',
 '/cbio/jclab/share/pdb/ko/pdb2kog.ent.gz',
 '/cbio/jclab/share/pdb/kr/pdb1krt.ent.gz',
 '/cbio/jclab/share/pdb/l4/pdb2l4g.ent.gz',
 '/cbio/jclab/share/pdb/ld/pdb1ldl.ent.gz',
 '/cbio/jclab/share/pdb/ld/pdb1ldr.ent.gz',
 '/cbio/jclab/share/pdb/lp/pdb1lpv.ent.gz',
 '/cbio/jclab/share/pdb/lw/pdb2lwh.ent.gz',
 '/cbio/jclab/share/pdb/lw/pdb2lwp.ent.gz',
 '/cbio/jclab/share/pdb/m3/pdb2m3p.ent.gz',
 '/cbio/jclab/share/pdb/m7/pdb4m7p.ent.gz',
 '/cbio/jclab/share/pdb/m7/pdb2m7v.ent.gz',
 '/cbio/jclab/share/pdb/mw/pdb2mw5.ent.gz',
 '/cbio/jclab/share/pdb/mz/pdb1mzi.ent.gz',
 '/cbio/jclab/share/pdb/n1/pdb2n1r.ent.gz',
 '/cbio/jclab/share/pdb/nl/pdb3nla.ent.gz',
 '/cbio/jclab/share/pdb/nw/pdb1nwb.ent.gz',
 '/cbio/jclab/share/pdb/ny/pdb1nyg.ent.gz',
 '/cbio/jclab/share/pdb/of/pdb2ofg.ent.gz',
 '/cbio/jclab/share/pdb/ov/pdb1ov2.ent.gz',
 '/cbio/jclab/share/pdb/p3/pdb4p3q.ent.gz',
 '/cbio/jclab/share/pdb/p3/pdb4p3r.ent.gz',
 '/cbio/jclab/share/pdb/p8/pdb1p8h.ent.gz',
 '/cbio/jclab/share/pdb/p8/pdb1p8u.ent.gz',
 '/cbio/jclab/share/pdb/p9/pdb1p9f.ent.gz',
 '/cbio/jclab/share/pdb/pd/pdb2pdd.ent.gz',
 '/cbio/jclab/share/pdb/pk/pdb1pkt.ent.gz',
 '/cbio/jclab/share/pdb/pt/pdb4pth.ent.gz',
 '/cbio/jclab/share/pdb/pt/pdb4ptj.ent.gz',
 '/cbio/jclab/share/pdb/qa/pdb4qa9.ent.gz',
 '/cbio/jclab/share/pdb/qc/pdb1qck.ent.gz',
 '/cbio/jclab/share/pdb/ql/pdb1qlk.ent.gz',
 '/cbio/jclab/share/pdb/r8/pdb1r8p.ent.gz',
 '/cbio/jclab/share/pdb/rf/pdb1rfa.ent.gz',
 '/cbio/jclab/share/pdb/rf/pdb1rfh.ent.gz',
 '/cbio/jclab/share/pdb/sr/pdb1srm.ent.gz',
 '/cbio/jclab/share/pdb/su/pdb1suh.ent.gz',
 '/cbio/jclab/share/pdb/su/pdb1sut.ent.gz',
 '/cbio/jclab/share/pdb/t5/pdb1t55.ent.gz',
 '/cbio/jclab/share/pdb/tb/pdb1tbo.ent.gz',
 '/cbio/jclab/share/pdb/tn/pdb1tnn.ent.gz',
 '/cbio/jclab/share/pdb/tz/pdb4tz1.ent.gz',
 '/cbio/jclab/share/pdb/tz/pdb4tz3.ent.gz',
 '/cbio/jclab/share/pdb/tz/pdb4tz5.ent.gz',
 '/cbio/jclab/share/pdb/zy/pdb1zy8.ent.gz',
 '/cbio/jclab/share/pdb/zn/pdb1znm.ent.gz',
 '/cbio/jclab/share/pdb/um/pdb1ums.ent.gz',
 '/cbio/jclab/share/pdb/z8/pdb1z8s.ent.gz',
 '/cbio/jclab/share/pdb/z6/pdb1z64.ent.gz',
 '/cbio/jclab/share/pdb/yy/pdb1yyj.ent.gz',
 '/cbio/jclab/share/pdb/yy/pdb1yyx.ent.gz',
 '/cbio/jclab/share/pdb/yr/pdb1yrq.ent.gz',
 '/cbio/jclab/share/pdb/vj/pdb1vjm.ent.gz',
 '/cbio/jclab/share/pdb/vr/pdb1vrc.ent.gz',
 '/cbio/jclab/share/pdb/y6/pdb1y6d.ent.gz',
 '/cbio/jclab/share/pdb/xf/pdb2xfm.ent.gz',
 '/cbio/jclab/share/pdb/06/pdb406d.ent.gz',
 '/cbio/jclab/share/pdb/a6/pdb1a6s.ent.gz',
 '/cbio/jclab/share/pdb/al/pdb2alb.ent.gz',
 '/cbio/jclab/share/pdb/aq/pdb1aqs.ent.gz',
 '/cbio/jclab/share/pdb/bf/pdb1bfi.ent.gz',
 '/cbio/jclab/share/pdb/bf/pdb1bfz.ent.gz',
 '/cbio/jclab/share/pdb/bh/pdb1bha.ent.gz',
 '/cbio/jclab/share/pdb/bq/pdb1bq0.ent.gz',
 '/cbio/jclab/share/pdb/c5/pdb3c5f.ent.gz',
 '/cbio/jclab/share/pdb/cc/pdb2ccx.ent.gz',
 '/cbio/jclab/share/pdb/en/pdb1enw.ent.gz',
 '/cbio/jclab/share/pdb/ex/pdb2exg.ent.gz',
 '/cbio/jclab/share/pdb/ez/pdb3ezb.ent.gz',
 '/cbio/jclab/share/pdb/f9/pdb2f93.ent.gz',
 '/cbio/jclab/share/pdb/f9/pdb2f95.ent.gz',
 '/cbio/jclab/share/pdb/fb/pdb1fb9.ent.gz',
 '/cbio/jclab/share/pdb/g1/pdb2g10.ent.gz',
 '/cbio/jclab/share/pdb/g5/pdb1g5k.ent.gz',
 '/cbio/jclab/share/pdb/gi/pdb1gib.ent.gz',
 '/cbio/jclab/share/pdb/gq/pdb2gq4.ent.gz',
 '/cbio/jclab/share/pdb/gq/pdb2gq5.ent.gz',
 '/cbio/jclab/share/pdb/gq/pdb2gq6.ent.gz',
 '/cbio/jclab/share/pdb/gq/pdb2gq7.ent.gz',
 '/cbio/jclab/share/pdb/gu/pdb1gu8.ent.gz',
 '/cbio/jclab/share/pdb/gx/pdb1gxh.ent.gz',
 '/cbio/jclab/share/pdb/hh/pdb1hhw.ent.gz',
 '/cbio/jclab/share/pdb/i1/pdb1i11.ent.gz',
 '/cbio/jclab/share/pdb/il/pdb2il8.ent.gz',
 '/cbio/jclab/share/pdb/it/pdb2ith.ent.gz',
 '/cbio/jclab/share/pdb/j6/pdb1j6t.ent.gz',
 '/cbio/jclab/share/pdb/jb/pdb1jba.ent.gz',
 '/cbio/jclab/share/pdb/jf/pdb1jfw.ent.gz',
 '/cbio/jclab/share/pdb/jn/pdb2jnc.ent.gz',
 '/cbio/jclab/share/pdb/jo/pdb2jo0.ent.gz',
 '/cbio/jclab/share/pdb/js/pdb2jsc.ent.gz',
 '/cbio/jclab/share/pdb/jt/pdb1jtw.ent.gz',
 '/cbio/jclab/share/pdb/jy/pdb1jy6.ent.gz',
 '/cbio/jclab/share/pdb/k2/pdb2k2q.ent.gz',
 '/cbio/jclab/share/pdb/k9/pdb2k9y.ent.gz',
 '/cbio/jclab/share/pdb/kc/pdb2kcc.ent.gz',
 '/cbio/jclab/share/pdb/kf/pdb1kft.ent.gz',
 '/cbio/jclab/share/pdb/kk/pdb2kkk.ent.gz',
 '/cbio/jclab/share/pdb/l2/pdb2l27.ent.gz',
 '/cbio/jclab/share/pdb/l2/pdb2l2t.ent.gz',
 '/cbio/jclab/share/pdb/lc/pdb1lcd.ent.gz',
 '/cbio/jclab/share/pdb/le/pdb2leh.ent.gz',
 '/cbio/jclab/share/pdb/lu/pdb1lu8.ent.gz',
 '/cbio/jclab/share/pdb/ly/pdb1ly7.ent.gz',
 '/cbio/jclab/share/pdb/m8/pdb4m83.ent.gz',
 '/cbio/jclab/share/pdb/ma/pdb1maj.ent.gz',
 '/cbio/jclab/share/pdb/ma/pdb2maz.ent.gz',
 '/cbio/jclab/share/pdb/mf/pdb1mfn.ent.gz',
 '/cbio/jclab/share/pdb/mf/pdb2mfn.ent.gz',
 '/cbio/jclab/share/pdb/ms/pdb1msh.ent.gz',
 '/cbio/jclab/share/pdb/n0/pdb1n0o.ent.gz',
 '/cbio/jclab/share/pdb/n5/pdb1n5g.ent.gz',
 '/cbio/jclab/share/pdb/nc/pdb1ncu.ent.gz',
 '/cbio/jclab/share/pdb/nx/pdb1nxn.ent.gz',
 '/cbio/jclab/share/pdb/o2/pdb1o2f.ent.gz',
 '/cbio/jclab/share/pdb/oh/pdb1ohh.ent.gz',
 '/cbio/jclab/share/pdb/op/pdb2opu.ent.gz',
 '/cbio/jclab/share/pdb/os/pdb1osl.ent.gz',
 '/cbio/jclab/share/pdb/pb/pdb1pbz.ent.gz',
 '/cbio/jclab/share/pdb/pj/pdb1pjf.ent.gz',
 '/cbio/jclab/share/pdb/pm/pdb1pms.ent.gz',
 '/cbio/jclab/share/pdb/po/pdb1pog.ent.gz',
 '/cbio/jclab/share/pdb/pr/pdb1prl.ent.gz',
 '/cbio/jclab/share/pdb/pr/pdb1prs.ent.gz',
 '/cbio/jclab/share/pdb/pv/pdb1pv3.ent.gz',
 '/cbio/jclab/share/pdb/q1/pdb2q1z.ent.gz',
 '/cbio/jclab/share/pdb/q2/pdb4q29.ent.gz',
 '/cbio/jclab/share/pdb/q4/pdb2q44.ent.gz',
 '/cbio/jclab/share/pdb/q4/pdb2q4o.ent.gz',
 '/cbio/jclab/share/pdb/rg/pdb2rgz.ent.gz',
 '/cbio/jclab/share/pdb/rr/pdb2rr9.ent.gz',
 '/cbio/jclab/share/pdb/s9/pdb1s9o.ent.gz',
 '/cbio/jclab/share/pdb/sy/pdb1sy8.ent.gz',
 '/cbio/jclab/share/pdb/tf/pdb1tfb.ent.gz',
 '/cbio/jclab/share/pdb/ts/pdb1ts6.ent.gz',
 '/cbio/jclab/share/pdb/ty/pdb4tyv.ent.gz',
 '/cbio/jclab/share/pdb/uw/pdb1uwo.ent.gz',
 '/cbio/jclab/share/pdb/v3/pdb2v3l.ent.gz',
 '/cbio/jclab/share/pdb/ze/pdb1zev.ent.gz',
 '/cbio/jclab/share/pdb/vs/pdb1vsq.ent.gz',
 '/cbio/jclab/share/pdb/y7/pdb1y7j.ent.gz',
 '/cbio/jclab/share/pdb/y7/pdb1y7k.ent.gz',
 '/cbio/jclab/share/pdb/xq/pdb4xq2.ent.gz',
 '/cbio/jclab/share/pdb/wr/pdb1wr1.ent.gz',
 '/cbio/jclab/share/pdb/xb/pdb1xbl.ent.gz']

def metal_scanner(file):
    
    metal_scanner_data = [0, file]
    pdbfile = gzip.open(file)
    
    for line in pdbfile:
        fields = line.split()
        
        if fields[0] == 'HET' and fields[1] == metal_name:
            metal_scanner_data[0] = 1
        #if 'HETATM' in line and fields[2] == metal_name:
        #    metal_scanner_data[1] = 1    
    
    print(metal_scanner_data)        
    return metal_scanner_data
    
def database_analyzer(pdbpath):
    
    database_analyzer_data = [0, []]
    #all_files = 0
    #files_w_HETATM = 0
    
    for metal_scanner_data in pool.map(metal_scanner, pdbs):
        #all_files += 1
        if metal_scanner_data[0] == 1:
            database_analyzer_data[0] += 1
            database_analyzer_data[1].append(metal_scanner_data[1])
        #if metal_scanner_data[1] == 1:
        #    files_w_HETATM += 1       
            
    return database_analyzer_data   
            
# Multiprocess set-up
if __name__ == '__main__':
    
    pdbs = glob.glob(pdbpath) 
    
    pdbs = [x for x in pdbs if x not in mdtraj_noload_pdbs]
    
    pool = mp.Pool(processes = ppn)
    database_analyzer_data = database_analyzer(pdbpath)       
    
                    
# write results
with open('12Nov15FILES_metal_scanner_HETONLY_results.txt', 'w') as f:
    f.write("metal_name\n")
    f.write(metal_name)
    f.write("\n")
    f.write('All files in the database:\n')
    f.write(str(len(glob.glob(pdbpath))))
    f.write('\n')
    f.write("Files with metal in HET:\n")
    f.write(str(database_analyzer_data[0]))
    f.write('\n')
    #f.write('All files read:\n')
    #f.write(str(allfiles))
    #f.write('\n')
    #f.write("Files with metal in HETATM:\n")
    #f.write(str(files_w_HETATM))
    #f.close()
                   
    f.write('File paths\n')
    for line in database_analyzer_data[1]:
        f.write(str(line))
        f.write('\n')               
