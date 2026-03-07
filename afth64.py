'''
Afth64 Interpreter v0.7-alpha0 Library

Copyright (c) 2025-2026 Sara Berman

Permission is hereby granted, free of charge, to any person obtaining a 
copy of this software and associated documentation files (the "Software"), 
to deal in the Software without restriction, including without limitation 
the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in 
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
SOFTWARE.
'''

class AFTH64:
    def __init__(self,dname,fname):
        from sys import stdin, stdout
        self.dname=dname
        self.fname=fname
        self.dlen=0
        self.flen=0
        self.stack=[]
        self.stack2=[]
        self.ibuf=b''
        self.obuf=b''
        self.lnum=0
        self.lchar=0
        self.stdin=stdin
        self.stdout=stdout
        self.flst=[]
        self.j=False
        self.t=0
        self.ti=0
        self.tj=0
        self.tk=0
        self.tl=0
        self.tt=0
        self.numin=0
        self.nmode=False
        self.wordlist=[]
    def buf_in(self):
        _in=self.stdin.read(1)
        if _in == None or _in == '':
            pass
        else:
            self.ibuf=self.ibuf+_in.encode()
    def buf_in_pop(self):
        _r=self.ibuf[0]
        if len(self.ibuf) > 1:
            self.ibuf=self.ibuf[1:]
        else:
            self.ibuf=b''
        #if _r == 13:
        #    _r = 10
        #else:
        #    pass
        return _r
    def buf_in_get(self):
        while self.ibuf == b'':
            self.buf_in()
    def buf_out(self):
        while len(self.obuf) > 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=self.obuf[1:]
        if len(self.obuf) == 1:
            self.stdout.write(chr(self.obuf[0]))
            self.obuf=b''
    def buf_out_put(self,chin):
        if chin.encode() == b'\n':
            self.obuf=self.obuf+b'\n'
        else:
            self.obuf=self.obuf+chin.encode()
    def open_file(self):
        adict = open(self.dname,'rt')
        adict_lst = adict.readlines()
        adict.close()
        del adict
        afile = open(self.fname,'rt')
        afile_lst = afile.readlines()
        afile.close()
        del afile
        flst = []
        self.dlen=len(adict_lst)
        self.flen=len(afile_lst)
        i=0
        for i in range(len(adict_lst)):
            flst.append(adict_lst[i].strip('\n').strip('\r'))
        del adict_lst
        for i in range(len(afile_lst)):
            flst.append(afile_lst[i].strip('\n').strip('\r'))
        del afile_lst
        self.flst=flst
        del flst
    def varnum_encode(self,s=''):
        n=0
        if len(s) < 1 or len(s) > 5:
            pass
        else:
            for i in range(len(s)):
                if ord(s[i]) < 32 or ord(s[i]) > 95:
                    pass
                else:
                    n=n+((ord(s[i])-32)%64)*(64**i)
        #print('DEBUG VN {'+s+'} ',n)
        return n
    def varnum_decode(self,n=1073741824):
        from math import log,floor
        l=0
        s=''
        if n >= 1073741824 or n < 0:
            s=''
        else:
            l=floor(log(n,64))
            for i in range(l+1):
                s=s+chr((n//(64**i))%64+32)
        return s
    def varnum_decode_notrunc(self,n=1073741824):
        s=''
        if n >= 1073741824 or n < 0:
            s='     '
        else:
            for i in range(5):
                s=s+chr((n//(64**i))%64+32)
        return s
    def wordlist_append(self,s,cs):
        self.wordlist.append([self.varnum_encode(s),cs])
    def make_wordlist(self):
        self.wordlist.append([1073741824,' '])
    def rstac_t_s(self):
        self.t=self.stack.pop()
    def rstac_s_t(self):
        self.stack.append(self.t)
    def rstac_t_s2(self):
        self.t=self.stack2.pop()
    def rstac_s2_t(self):
        self.stack2.append(self.t)
    def rstac_t_len_s(self):
        self.t=len(self.stack)
    def rstac_t_len_s2(self):
        self.t=len(self.stack2)
    def rswap_t_i(self):
        self.tt=self.t
        self.t=self.ti
        self.ti=self.tt
    def rswap_t_j(self):
        self.tt=self.t
        self.t=self.tj
        self.tj=self.tt
    def rswap_t_k(self):
        self.tt=self.t
        self.t=self.tk
        self.tk=self.tt
    def rswap_t_l(self):
        self.tt=self.t
        self.t=self.tl
        self.tl=self.tt
    def rcore_zte(self):
        if self.t == 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_ztg(self):
        if self.t > 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_not_tl(self):
        if self.tl == 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_or_tl(self):
        if self.tl == 0 and self.t == 0:
            self.tl=0
        else:
            self.tl=1
    def rcore_and_tl(self):
        if self.tl != 0 and self.t != 0:
            self.tl=1
        else:
            self.tl=0
    def rcore_xor_tl(self):
        if self.tl == 0 and self.t == 0:
            self.tl=0
        elif self.tl != 0 and self.t != 0:
            self.tl=0
        else:
            self.tl=1
    def rcore_jnz_r(self):
        if self.tl != 0:
            self.lnum=self.lnum+self.t
            self.j=True
        else:
            pass
    def rcore_quit(self):
        from sys import exit as sys_exit
        sys_exit(self.t)
    def rcore_quit_iflz(self):
        from sys import exit as sys_exit
        if self.tl==0:
            sys_exit(self.t)
    def rcore_t_zero(self):
        self.t=0
    def rcore_t_x16_inc(self,n=0):
        self.t=self.t*16+(n%16)
    def rcore_t_inc(self):
        self.t=self.t+1
    def rcore_t_dec(self):
        self.t=self.t-1
    def rcore_t_shl(self):
        self.t=self.t*2
    def rcore_t_shr(self):
        self.t=self.t//2
    def rcore_t_abs(self):
        self.t=abs(self.t)
    def rcore_t_flipsign(self):
        self.t=self.t*-1
    def rmath_t_tl_add(self):
        self.t=self.t+self.tl
    def rmath_t_tl_mul(self):
        self.t=self.t*self.tl
    def rmath_t_tl_idiv(self):
        self.t=self.t//self.tl
    def rmath_t_tl_mod(self):
        self.t=self.t%self.tl
    def rmath_t_tl_pow(self):
        from math import floor
        self.t=floor(pow(self.t,self.tl))
    def rmath_t_tl_log(self):
        from math import floor,log
        self.t=floor(log(self.t,self.tl))
    def rxtra_t_randint(self):
        from time import monotonic_ns
        from random import seed,randint
        seed(monotonic_ns()%(2**31))
        self.t=randint(0,self.t-1)
    def rxtio_t_in_char(self):
        self.buf_in_get()
        self.t=self.buf_in_pop()
    def rxtio_t_in_int(self):
        a=0
        b=0
        d=[]
        self.buf_in_get()
        a=self.buf_in_pop()
        while a < 48 or a > 57:
            self.buf_in_get()
            a=self.buf_in_pop()
        while a >= 48 and a <= 57:
            d.append(a)
            self.buf_in_get()
            a=self.buf_in_pop()
        for i in range(len(d)):
            b=b*10+(d[i]-48)%10
        self.t=b
    def rxtio_t_out_char(self):
        self.buf_out_put(chr(abs(self.t)%128))
    def rxtio_t_out_int(self):
        from math import floor,log
        a=self.t
        j=0
        l=0
        s=0
        o=''
        if a != 0:
            l=floor(log(abs(a),10))
            s=a//abs(a)
        else:
            l=0
            s=1
        if s == -1:
            o=o+'-'
        else:
            pass
        for j in range(l+1):
            o=o+chr(48+(abs(a)//pow(10,l-j))%10)
        o=o+' '
        self.buf_out_put(o)
    def rxtio_t_in_hex(self):
        a=0
        b=0
        d=[]
        self.buf_in_get()
        a=self.buf_in_pop()
        while not ((a >= 48 and a <= 57) or (a >= 65 and a <= 70) or (a >= 97 and a <= 102)):
            self.buf_in_get()
            a=self.buf_in_pop()
        while (a >= 48 and a <= 57) or (a >= 65 and a <= 70) or (a >= 97 and a <= 102):
            d.append(a)
            self.buf_in_get()
            a=self.buf_in_pop()
        for i in range(len(d)):
            if d[i] >= 48 and d[i] <= 57:
                b=b*16+(d[i]-48)
            elif d[i] >= 65 and d[i] <= 70:
                b=b*16+(d[i]-55)
            elif d[i] >= 97 and d[i] <= 102:
                b=b*16+(d[i]-87)
            else:
                pass
        self.t=b
    def rxtio_t_out_hex(self):
        from math import floor,ceil,log
        a=self.t
        j=0
        l=0
        s=0
        o=''
        if a != 0:
            l=floor(log(abs(a),256))
            s=a//abs(a)
        else:
            l=0
            s=1
        if s == -1:
            o=o+'-'
        else:
            pass
        for j in range(l+1):
            n=(abs(a)//ceil(pow(256,l-j)))%256
            m=(n//16)%16
            if m >= 10:
                o=o+chr(87+m)
            else:
                o=o+chr(48+m)
            m=n%16
            if m >= 10:
                o=o+chr(87+m)
            else:
                o=o+chr(48+m)
        o=o+' '
        self.buf_out_put(o)
    def run_char(self,gch=b' '):
        ret=0
        if gch==b' ':
            pass
        elif gch==b'!':
            self.rcore_not_tl()
        elif gch==b'"':
            pass
        elif gch==b'#':
            pass
        elif gch==b'$':
            pass
        elif gch==b'%':
            self.rmath_t_tl_mod()
        elif gch==b'&':
            self.rcore_and_tl()
        elif gch==b"'":
            pass
        elif gch==b'(':
            self.rxtio_t_in_hex()
        elif gch==b')':
            self.rxtio_t_out_hex()
        elif gch==b'*':
            self.rmath_t_tl_mul()
        elif gch==b'+':
            self.rmath_t_tl_add()
        elif gch==b',':
            self.rxtio_t_in_char()
        elif gch==b'-':
            self.rcore_t_flipsign()
        elif gch==b'.':
            self.rxtio_t_out_char()
        elif gch==b'/':
            self.rmath_t_tl_idiv()
        elif gch==b'0':
            self.rcore_t_x16_inc(0)
        elif gch==b'1':
            self.rcore_t_x16_inc(1)
        elif gch==b'2':
            self.rcore_t_x16_inc(2)
        elif gch==b'3':
            self.rcore_t_x16_inc(3)
        elif gch==b'4':
            self.rcore_t_x16_inc(4)
        elif gch==b'5':
            self.rcore_t_x16_inc(5)
        elif gch==b'6':
            self.rcore_t_x16_inc(6)
        elif gch==b'7':
            self.rcore_t_x16_inc(7)
        elif gch==b'8':
            self.rcore_t_x16_inc(8)
        elif gch==b'9':
            self.rcore_t_x16_inc(9)
        elif gch==b':':
            self.rcore_t_abs()
        elif gch==b';':
            self.rcore_or_tl()
        elif gch==b'<':
            self.rcore_t_shl()
        elif gch==b'=':
            pass
        elif gch==b'>':
            self.rcore_t_shr()
        elif gch==b'?':
            pass
        elif gch==b'@':
            pass
        elif gch==b'A':
            self.rcore_t_x16_inc(10)
        elif gch==b'B':
            self.rcore_t_x16_inc(11)
        elif gch==b'C':
            self.rcore_t_x16_inc(12)
        elif gch==b'D':
            self.rcore_t_x16_inc(13)
        elif gch==b'E':
            self.rcore_t_x16_inc(14)
        elif gch==b'F':
            self.rcore_t_x16_inc(15)
        elif gch==b'G':
            self.rstac_s_t()
        elif gch==b'H':
            self.rstac_t_s()
        elif gch==b'I':
            self.rswap_t_i()
        elif gch==b'J':
            self.rswap_t_j()
        elif gch==b'K':
            self.rswap_t_k()
        elif gch==b'L':
            self.rswap_t_l()
        elif gch==b'M':
            self.rstac_s2_t()
        elif gch==b'N':
            self.rstac_t_s2()
        elif gch==b'O':
            self.rstac_t_len_s()
        elif gch==b'P':
            self.rstac_t_len_s2()
        elif gch==b'Q':
            self.rcore_quit()
        elif gch==b'R':
            self.rcore_quit_iflz()
        elif gch==b'S':
            self.rcore_jnz_r()
        elif gch==b'T':
            self.rcore_zte()
        elif gch==b'U':
            self.rcore_ztg()
        elif gch==b'V':
            self.rcore_t_dec()
        elif gch==b'W':
            self.rmath_t_tl_pow()
        elif gch==b'X':
            self.rcore_xor_tl()
        elif gch==b'Y':
            self.rmath_t_tl_log()
        elif gch==b'Z':
            self.rxtra_t_randint()
        elif gch==b'[':
            self.rxtio_t_in_int()
        elif gch==b'\\':
            pass
        elif gch==b']':
            self.rxtio_t_out_int()
        elif gch==b'^':
            self.rcore_t_inc()
        elif gch==b'_':
            self.rcore_t_zero()
        else:
            pass
        return ret
    def run_tri(self,cmp):
        runw=0
        if len(cmp) == 0:
            pass
        elif cmp[0]=='`' and len(cmp)==1:
            self.stack.append(ord(' ')%128)
        elif cmp[0]=='`' and len(cmp)>=2:
            self.stack.append(ord(cmp[1])%128)
        elif cmp[0]=='{' and len(cmp) >= 3:
            for lc in range(len(cmp)-2):
                if self.j == False:
                    cmdch = cmp[lc+1]
                    runl=self.run_char(cmdch.encode())
                    self.buf_out()
        elif ord(cmp[0]) >= 33 and ord(cmp[0]) <= 95:
            wn=self.varnum_encode(cmp)
            wnum=0
            for i in range(len(self.wordlist)):
                if self.wordlist[i][0]==wn:
                    wnum=i
            #print('DEBUG CW {{'+self.wordlist[wnum][1]+'}}')
            for lc in range(len(self.wordlist[wnum][1])):
                if self.j == False:
                    cmdch = self.wordlist[wnum][1][lc]
                    #print('DEBUG C {{{'+cmdch+'}}}')
                    runw=runw+self.run_char(cmdch.encode())
                    self.buf_out()
        else:
            pass
        return runw%256
    def run_line(self,line):
        runl=0
        #ln=self.lnum
        self.j=False
        self.t=0
        self.ti=0
        self.tj=0
        self.tk=0
        self.tl=0
        self.tt=0
        if len(line) == 0:
            pass
        elif line[0]=='~' and (ord(line[1]) >= 33 and ord(line[1]) <= 95):
            lines=line.split(' ')
            self.wordlist_append(lines[0][1:],lines[1])
        elif line[0]=='|' and len(line) >= 2:
            line2=line[1:]
            for i in range(len(line2)):
                self.stack.append(ord(line2[len(line2)-i-1]))
        elif len(line) >= 2:
            runp=0
            lines=line.split(' ')
            for i in range(len(lines)):
                cmdtri=lines[i]
                #print('DEBUG T {'+cmdtri+'}')
                runp=runp+self.run_tri(cmdtri)
            runl=runp%256
        else:
            pass
        if self.j==False:
            self.lnum=self.lnum+1
        return runl
    def run_file(self):
        runf=0
        self.make_wordlist()
        l=0
        while l < len(self.flst) and l > -1:
            line = self.flst[l]
            #print('DEBUG L:',line)
            runf=self.run_line(line)
            l=self.lnum
        return runf

def main(afth64_dict,file):
    import gc
    from sys import exit as sys_exit
    afth64=AFTH64(afth64_dict,file)
    afth64.open_file()
    gc.collect()
    r=afth64.run_file()
    del afth64
    gc.collect()
    sys_exit(abs(r)%256)
