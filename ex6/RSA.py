import Base
import zlib
import math
from operator import is_
from gmpy2 import invert#求模逆
from gmpy2 import iroot,mpz,digits,is_square,isqrt
def gcd(a,b):
    if a%b == 0:
        return b
    else :
        return gcd(b,a%b)
    
def egcd(a,b):
    if a==0:
        return (b,0,1)
    else:
        g,y,x=egcd(b%a,a)
        return (g,x-(b//a)*y,y)   
def samemod(n,c1,c2,e1,e2):   
    n=int(n)
    c1=int(c1)
    c2=int(c2)
    e1=int(e1)
    e2=int(e2)
    s=egcd(e1,e2)
    s1=s[1]
    s2=s[2]
    if s1<0:
        s1=-s1
        c1=invert(c1,n)
    elif s2<0:
        s2=-s2
        c2=invert(c2,n)
    m=pow(c1,s1,n)*pow(c2,s2,n)%n
    print hex(m)
    return hex(m)
def chinese_remainder_theorem(items):
    N = 1
    for a, n in items:
        N *= n
        result = 0
    for a, n in items:
        m = N/n
        d, r, s = egcd(n, m)
        if d != 1:
            N=N/n
            continue
        result += a*s*m
    return result % N, N
def lowen(n,c):
    k=0
    while 1:
        res = iroot(c+k*n,3)
        if(res[1]==True):
            print res
            break
        print k
        k=k+1
def pp1(n):
    B=2**20
    a=2
    for i in range(2,B+1):
        a=pow(a,i,n)
        d=gcd(a-1,n)
        if (d>=2)and(d<=(n-1)):
            q=n/d
            n=q*d
    return d
def pq(n):
    B=math.factorial(2**14)
    u=0;v=0;i=0
    u0=iroot(n,2)[0]+1
    while(i<=(B-1)):
        u=(u0+i)*(u0+i)-n
        if is_square(u):
            v=isqrt(u)
            break
        i=i+1  
    p=u0+i+v
    return p
    
def decryped(num,string,string2): 
    c,a,count=[],'',0  
    for i in range(len(string)):
        a+=string[i]
        count+=1
        if(count%2==0):
            count=0
            c.append(a)
            a=''
    for i in c:
        a+=chr(int(i.upper(), 16))    
    print num,'----',a
 
def fun(x,n,N): 
    '''快速模取幂算法'''
    res=1  
    while n>0:  
        if(n & 1): 
            res=(res*x)%N 
        x=(x*x)%N 
        n >>= 1 
    return res 
    
m,N,E,C,n,e,c=[],[],[],[],[],[],[]
filename=['Frame'+str(i) for i in range(21)]
for i in range(21):
    fd = open(filename[i],'r')
    m.append(fd.read())
    fd.close()
for frame in m:
    N.append(frame[0:256])
    E.append(frame[256:512])
    C.append(frame[512:768])
#//#
for i in range(21):
    n.append(int('0x'+N[i],16))
    e.append(int('0x'+E[i],16))
    c.append(int('0x'+C[i],16))
    
#共模攻击0，4
samemod(n[0],c[0],c[4],e[0],e[4])

#低加密指数广播攻击，e=5，3，8，12，16，20
sessions=[{"c": int(c[3]),"n": int(n[3])},
{"c":int(c[8]) ,"n":int(n[8]) },
{"c":int(c[12]),"n":int(n[12])},
{"c":int(c[16]),"n":int(n[16])},
{"c":int(c[20]),"n":int(n[20])}]
data = []
for session in sessions:
    data = data+[(session['c'], session['n'])]
x, y = chinese_remainder_theorem(data)
m3 =iroot(mpz(x),5)
print hex(m3[0])

#低加密指数攻击
#lowen(mpz(n[7]),mpz(c[7]))
#模数分解1，18
gcdN=gcd(n[1],n[18])
q1=n[1]/gcdN
q18=n[18]/gcdN
phi1=(gcdN-1)*(q1-1)
phi18=(gcdN-1)*(q18-1)
d1=invert(e[1],phi1)
d18=invert(e[18],phi18)
m1=pow(c[1],d1,n[1])
m18=pow(c[18],d18,n[18])
print hex(m1)
print hex(m18)
'''           
#pollard’s p-1#2,6,19

for i in (2,6,19):
    p=pp1(n[i])
    #p2=1719620105458406433483340568317543019584575635895742560438771105058321655\
       #2385626130839796514765557880099945578220245652269329062952082627568222756\
       #63694111
    #p6=920724637201
    #p19=108563496559
    print p
    q=n[i]/p
    phi=(p-1)*(q-1)
    d=invert(e[i],phi)
    m=pow(c[i],d,n[i])
    print hex(m)

#p-q#10,14
for i in (10,14):
    p=pq(n[i])
    print p
    #p10=968692491755480541893763887279601716052566457985764059016032030080511\
        #544357818498593433858330318017858200959163432175520400839465585825498\
        #0766008932978699
    #p14=1095485629923346512635991417150030582284616543108518367399910975944970\
    #64176365197118817077316225064077221431638476720644593334315729920212578815\
    #51867597529
    q=n[i]/p
    phi=(p-1)*(q-1)
    d=invert(e[i],phi)
    m=pow(c[i],d,n[i])
    print hex(m)
'''


decryped(0,'4D79207365637265','From Frame 0 and 4')

decryped(3,'7420697320612066','From Frame 3,8,12,16 and 20')

decryped(1,'2E20496D6167696E','From Frame 1')
decryped(18,'6D204120746F2042','From Frame 18')

decryped(2,'2054686174206973','From Frame 2')
decryped(6,'20224C6F67696320','From Frame 6')
decryped(19,'696E737465696E2E','From Frame 19')

decryped(10,'77696C6C20676574','From Frame 10')
decryped(14,'20796F752066726F','From Frame 14')

 


 
