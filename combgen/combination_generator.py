import numpy as np
import itertools

from combgen.constraint_conditions import ConCon



class CombGen:
    def __init__(self,feasibles,**kwargs):
        self.feas = self.get_feas(feasibles)
        self.arty = len(self.feas)
        self.card = [len(dic) for dic in self.feas]
    
        self.cc = ConCon(kwargs,self.feas,self.arty,self.card)
        
        if self.cc.disp:
            print(f"-----------------------------------")   
            print(f"  random           : {self.cc.rnd}")
            print(f"    replace        : {self.cc.rep}")
            
            print(f"  duplicate        : {self.cc.dup}")
            print(f"  exchange         : {self.cc.exc}")
            print(f"  contain          : {self.cc.conts}")
            print(f"  total            : {self.cc.conexp}")

            print(f"  arity            : {self.arty}")
            print(f"  cardinalities    : {self.card}")
            print(f"  equivalent       : {self.cc.equ}")
            print(f"  estimated number : {self.cc.ncmb} ({self.cc.comm})")
            print(f"  feasibles        :")
            for fea in self.feas:
                print(f"    {self.disp_dic(fea)}")
            print(f"-----------------------------------")
        print()
        self.rep_logs = []
        if self.cc.rnd:
            self.gen = self._gen_random()
        else:
            self.gen = self._gen()
        
        
    def __iter__(self):
        return self.gen
    
    def __next__(self):
        return next(self.gen)

    
    def get_feas(self,iterables):
        # "generator" and "range" objects are expanded here.
        feas = []
        for itr in iterables:
            if type(itr) is dict:
                itr = {str(k):v for k,v in itr.items()}
            elif type(itr).__name__ == "ndarray":
                itr = {str(round(v,9)):v for v in itr} 
            else:
                itr = {str(v):v for v in itr} 
            feas.append(itr)
        return feas    
           
    
    def disp_dic(self,dic):
        lis = list(dic.keys())
        if len(lis) <= 4:
            s = lis[0]
            for i in range(1,len(lis)):
                s += ",  " + lis[i]
        else:
            s = f"{lis[0]},  {lis[1]},  ...,  {lis[-1]}"
        return s
        
    
    def _gen(self):
        for tup in itertools.product(*self.feas):
            if self.cc.check(tup):
                continue
            yield " ".join(tup)
        
        
    def _gen_random(self):
        itr = 10000
        rng = np.random.default_rng()
        liss = [list(feas) for feas in self.feas]
        cnt = 0
        while True:
            cnt += 1
            if cnt > itr:
                return StopIteration
            
            tup = tuple(rng.choice(lis) for lis in liss)
            
            if self.cc.check(tup):
                continue
            
            if not self.cc.rep:
                if tup in self.rep_logs:
                    continue
                     
            cnt = 0
            if not self.cc.rep:
                self.rep_logs.append(tup)
            yield " ".join(tup)      
            
               
    def show(self):
        for i,cmb in enumerate(self):
            print(f"{i}   {cmb}")
 
               
    def test(self,n_gen=30):
        for i in range(n_gen):
            try:
                print(f"{i}   {next(self)}")
            except StopIteration:
                pass
    
    
    
