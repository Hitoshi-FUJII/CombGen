import math
import functools,operator

        
class ConCon:
    def __init__(self,ccs,feas,arity,cards):
        self.disp = ccs.get("display")
        self.rnd  = ccs.get("random")
        if self.rnd is None: self.rnd = False
        self.rep  = ccs.get("replace")
        if self.rep is None: self.rep = False
           
        self.feas = feas
        self.arty = arity
        self.card = cards
        
        self.equ = all([self.feas[0] == feas for feas in self.feas])   
        
        dup = ccs.get("duplicate")
        if dup is True or dup is None: self.dup = True
        else: self.dup = False
        
        exc = ccs.get("exchange")
        if exc is True or exc is None: self.exc = True
        else: self.exc = False
            
        conts = ccs.get("contain")
        if conts is not None:
            if type(conts) is not list: conts = [conts]
            self.conts = [str(c) for c in conts]
            self.con   = True
            self.k     = len(self.conts)
        else:
            self.conts = None
            self.con   = False
            self.k     = 0
                
        conexp = ccs.get("total")
        if conexp is not None:
            self.tot = True
            if type(conexp) is int or type(conexp) is float:
                self.conexp = "==" + str(conexp)
            else:
                self.conexp = conexp
        else:
            self.tot    = False
            self.conexp = None
            
            
        self.exc_logs = []
        self.ncmb,self.comm = self._ncmb()
        
        
    def check(self,tup):
        if not self.dup:
            if len(set(tup)) < len(tup):
                return True
            
        if not self.exc:
            lis = sorted(tup)
            if lis in self.exc_logs:
                return True
            else:
                self.exc_logs.append(lis)
                
        if self.con:              
            if not all(s in tup for s in self.conts):   
                return True
            
        if self.tot:
            rsum = round(sum([self.feas[i][s] for i,s in enumerate(tup)]),9)
            if not eval(str(rsum)+self.conexp):
                return True  
            
        return False        

    
    
    def _ncmb(self):    
        ncmb_max = functools.reduce(operator.mul,self.card)
        jscrd = "*".join([str(c) for c in self.card])
        
        if self.tot:
            return "no estimate", "at most " + str(ncmb_max)+ "=" + jscrd 
        
        if not self.equ:
            if all([self.dup, self.exc, not self.con]):
                return ncmb_max,"=" + jscrd
            else:
                return "no estimate","at most " + str(ncmb_max)+ "=" + jscrd 
        
        else:  # for equivalent feasibles
            if self.dup and self.exc:
                func = pow
                ope  = "**"
            elif self.dup and not self.exc:
                func = self.mHn
                ope  = "H" 
            elif not self.dup and self.exc:
                func = self.mPn
                ope  = "P"
            else:
                func = self.mCn
                ope  = "C"
            return self.ncmbf(func,self.k),f"<={func(self.card[0],self.arty)}={self.card[0]}{ope}{self.arty}"


    def ncmbf(self,f,k):
        ncmb = 0
        for i in range(k+1):
            ncmb += (-1)**i * self.mCn(k,i) * f(self.card[0]-i,self.arty)
        return ncmb
            
    def mPn(self,m,n):
        if m-n < 0: return 0
        return math.factorial(m) // math.factorial(m-n)
    
    def mCn(self,m,n):
        return self.mPn(m,n) // math.factorial(n)       
        
    def mHn(self,m,n):
        return self.mCn(m+n-1,n)
           
  


