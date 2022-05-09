#!/usr/bin/env python
# coding: utf-8

# In[119]:


import random
import math
#import matplotlib.pyplot as plt
#import seaborn as sns
import numpy as np
from numpy.linalg import inv


# In[120]:


from numpy import linalg as LA
mat=np.array([[1,0.2,0.04],
            [0.2,1,0.2],
            [0.04,0.2,1]])
w,v=LA.eig(mat)
half=np.dot(v,np.diag(np.sqrt(w)))


def AcceptReject_2(b=4,cov=half): #random sample functions
    while True:
        r=random.uniform(0,1)**(1/3)
        rn=np.random.normal(loc=0.0, scale=1.0, size=3)
        norm_2=np.linalg.norm(rn,ord=2)
        theta=rn/norm_2
        random_unitball=r*theta
        #x = random.uniform(-scale, scale)
        y = random.uniform(0, 1)
        if y*b <= b*(1-np.linalg.norm(random_unitball,ord=2)**2)**(b-1):
            return np.dot(cov,random_unitball)

def AceeptReject(scale=1, c1=15 / (8), power=2):  # random sample functions
    while True:
        x = random.uniform(-scale, scale)
        y = random.uniform(0, 1)
        if y * c1 <= 15 / (8 * scale ** 5) * math.pow((scale - x) * (x + scale), power):
            return 1/2*x

# In[121]:


class Solution:
    def __init__(self, th=1e-4):
        self.th = th  # 设置阈值threshold  th=1e-4

    #def phi_root(self,a,x,thetax,stepsize):
    #    while abs(self.phi(a,x,thetax)) >= self.th:  # 判断是否收敛
    #        x = x- stepsize*self.phi(a,x,thetax)/self.phi_p(a,x) # (x*x - a)/(2x)
    #    return x
    
    def phi_root(self,c,d,thetax):
        #if self.phi(a,c,thetax)*self(a,d,thetax)>=0:
        #    return None
        a_n = c
        b_n = d
        m_n=(a_n+b_n)/2
        iter=0
        while abs(self.phi(m_n,thetax)) >= self.th and iter<=1000:  # 判断是否收敛
             #   x = x- stepsize*self.phi(a,x,thetax)/self.phi_p(a,x)
            iter+=1
            m_n = (a_n + b_n)/2
            f_m_n = self.phi(m_n,thetax)
            if self.phi(a_n,thetax)*f_m_n < 0:
                a_n = a_n
                b_n = m_n
            elif self.phi(b_n,thetax)*f_m_n < 0:
                a_n = m_n
                b_n = b_n
            elif f_m_n == 0:
                print("Found exact solution.")
                return m_n
            else:
                print("Bisection method fails.")
                return float('NaN')
        return (a_n + b_n)/2

    def phi(self, x, thetax):

        # return x-(-x**13/13+6*x**11/11-15*x**9/9+20*x**7/7-3*x**5+2*x**3-x+0.34099234)/(1-x**2)**6+thetax
        return x-(-(2*x)**5/5+2*(2*x)**3/3-2*x+8/15)/(2*(1-(2*x)**2)**2)+thetax#(1.2 * x ** 5 - 8 / 3 * x ** 3 + 2 * x - 8 / 15) / (x ** 4 - 2 * x ** 2 + 1) + thetax

    def F(self, x,thetax):
        if x-thetax>0.5:
            return 0
        elif x-thetax<-0.5:
            return x
        else:

        # return x-(-x**13/13+6*x**11/11-15*x**9/9+20*x**7/7-3*x**5+2*x**3-x+0.34099234)/(1-x**2)**6+thetax
            return x*15/16*(-(2*(x-thetax))**5/5+2*(2*(x-thetax))**3/3-2*(x-thetax)+8/15)


# In[122]:


class Kernel:
    def __init__(self,v_i,y_t,n):
        self.v_i=v_i
        self.y_t=y_t
        #global v_i
        #global y_t
        self.n=n
        self.h=4*n**(-1/5)

    def sec_kernel_h(self,t):
        vec=self.kernel((self.v_i-t)/self.h)
        return 1/(self.n*self.h)*sum(vec*self.y_t)
    
    def sec_kernel_f(self,t):
        vec=self.kernel((self.v_i-t)/self.h)
        return 1/(self.n*self.h)*sum(vec)
    
    def sec_kernel_h1(self,t):
        vec=self.kernel2((self.v_i-t)/self.h)
        return -1/(self.n*self.h**2)*sum(vec*self.y_t)
    
    def sec_kernel_f1(self,t):
        vec=self.kernel2((self.v_i-t)/self.h)
        return -1/(self.n*self.h**2)*sum(vec)
    
    def sec_kernel_h2(self,t):
        vec=self.kernel3((self.v_i-t)/self.h)
        return 1/(self.n*self.h**3)*sum(vec*self.y_t)
    def sec_kernel_f2(self,t):
        vec=self.kernel3((self.v_i-t)/self.h)
        return 1/(self.n*self.h**3)*sum(vec)
    
    def kernel(self, x):
        return (1-x**2)**5*((abs(x)<=1)*1)

    def kernel2(self, x):
        return -5*(1-x**2)**4*2*x*((abs(x)<=1)*1)

    def kernel3(self, x):
        return -5*(1-x**2)**3*(2-18*x**2)*((abs(x)<=1)*1)

    #def kernel(self,x): #six order kernel
    #    return ((1-26/3*x**2+13*x**4)*(1-x**2)**3)*((abs(x)<=1)*1)
        #return (1-11/3*x**2)*(1-x**2)**3*((abs(x)<=1)*1)
    
    #def kernel2(self,x):
    #    return ((-70*x/3+364*x**3/3-130*x**5)*(1-x**2)**2)*((abs(x)<=1)*1)
     #   return (-22/3*x*(1-x**2)**3+(1-11/3*x**2)*3*(1-x**2)**2*(-2*x))*((abs(x)<=1)*1)
    
   # def kernel3(self,x):
    #    return (-2*x*(1-x**2)*(-70*x/3+364*x**3/3-130*x**5)+(1-x**2)**2*(-70/3+364*x**2-650*x**4))*((abs(x)<=1)*1)
     #   return (-4*x*(1-x**2)*(88/3*x**3-40/3*x)+(1-x**2)**2*(88*x**2-40/3))*((abs(x)<=1)*1)
    
    
        
    def sec_kernel_whole1(self,t):
        return self.sec_kernel_h(t)/self.sec_kernel_f(t)
    
    def sec_kernel_whole2(self,t):
        return (self.sec_kernel_h1(t)*self.sec_kernel_f(t)-self.sec_kernel_h(t)*self.sec_kernel_f1(t))/self.sec_kernel_f(t)**2
    def sec_kernel_whole3(self,t):
        kh1=self.sec_kernel_h1(t)
        kf0=self.sec_kernel_f(t)
        kh0=self.sec_kernel_h(t)
        kf1=self.sec_kernel_f1(t)
        kh2=self.sec_kernel_h2(t)
        kf2=self.sec_kernel_f2(t)
        
        return ((kh1*kf0)**2-(kh0*kf1)**2-kh0*kh2*kf0**2+kh0**2*kf0*kf2)/(kh1*kf0-kh0*kf1)**2
    
    def phi(self,t,thetax):
        return t+self.sec_kernel_whole1(t)/self.sec_kernel_whole2(t)+thetax
    
    
    def phi_p(self,t): 
        return 1+self.sec_kernel_whole3(t)
    
    def phi_root(self,y,thetax,stepsize):
        iter=0
        x=(-1.7)*np.exp(y)/(1+np.exp(y))+0.3
        while abs(self.phi(x,thetax)) >= 1e-4 and iter<=1000:  # 判断是否收敛
            y = y- stepsize*self.phi(x,thetax)/(self.phi_p(x)*(-1.7)*np.exp(y)/(1+np.exp(y))**2)
            #print(y)
            x=(-1.7)*np.exp(y)/(1+np.exp(y))+0.3
            iter=iter+1 # (x*x - a)/(2x)
            #x=-0.8*math.exp(y)/(1+math.exp(y))
        return x


# In[125]:

mat1=np.array([[0.4,0.16,0],
            [0.16,0.4,0.16],
            [0,0.16,0.4]])
mat2=np.array([[0.1,0.01,0],
            [0.01,0.1,0.01],
            [0,0.01,0.1]])
solu=Solution()
B=6
T_l=[1500,2000,3100,4000,5000,6300]
l_0=200
theta= np.sqrt(2/3)*np.ones(3, dtype = int)
reg_Tcum=np.zeros(30,dtype=int)
reg_Tcum_tt=np.zeros(30,dtype=int)
reg_Tcum_tf=np.zeros(30,dtype=int)
reg_Tcum_bt=np.zeros(30,dtype=int)
reg_Tcum.reshape(1,30)
reg_Tcum_tt.reshape(1,30)
reg_Tcum_tf.reshape(1,30)
reg_Tcum_bt.reshape(1,30)
for T in T_l:
    epi_num=math.ceil(math.log(T/l_0+1, 2))
    reg_T=[] #record 30 times
    reg_T_tt=[]
    reg_T_tf=[]
    reg_T_bt=[]
    for times in range(30):
        reg=[] #for every time, record all the regret
        reg_tt=[]
        reg_tf=[]
        reg_bt=[]
        x_m0 = np.zeros((500, 3))
        for i in range(2, len(x_m0)):
            x_m0[i] = (np.dot(mat1,x_m0[i - 1].T) +(np.dot(mat2,x_m0[i-2].T))+np.array(AcceptReject_2(4, half))).reshape(1, 3)
        x_m1=x_m0[498]
        x_m=x_m0[499]
        for k in range(epi_num):
            t=0
            l_k=l_0*2**k
            l_k1=math.floor((l_k*3)**(5/7))
            v_i=[]
            v_i_true=[]
            v_t=[]
            y_t=[]
            p_t_coll=[]
            X=np.zeros(3,dtype=int)
            X=X.reshape(1,3)
         #   X=np.zeros(5,dtype=int)
         #   X=X.reshape(1,5)
            while t<=l_k:
                if t<=l_k1:  
                    x=np.dot(mat1,x_m.T)+np.dot(mat2,x_m1.T)+np.array(AcceptReject_2(4,half))
                    X=np.concatenate((X,x.reshape(1,3)))
                    x_m1=x_m
                    x_m=x
                    #0.2*x_m+np.array([AceeptReject2(1,35/8,3) for _ in range(5)])
                    theta_x=3+np.dot(theta,x)
                    v=theta_x+AceeptReject(1,15/8,2)
                    p_t=random.uniform(0,B)
                    v_i_true.append(p_t-3-np.dot(theta,x))
                    p_t_coll.append(p_t)
                    op_price=solu.phi_root(-0.495,0.495,theta_x)+theta_x
                    rev_diff=solu.F(op_price,theta_x)-solu.F(p_t,theta_x)
                    #print(op_price)
                    print(rev_diff)
                    #print(abs(p_t-op_price))
                    
                    reg.append(rev_diff)
                    reg_tt.append(rev_diff)
                    reg_tf.append(rev_diff)
                    reg_bt.append(rev_diff)
                    #print(op_price)
                    #print(abs(p_t-op_price))
                    
                    #reg.append(abs(p_t-op_price)**2)
                    #reg_tt.append(abs(p_t-op_price)**2)
                    #reg_tf.append(abs(p_t-op_price)**2)
                    #reg_bt.append(abs(p_t-op_price)**2)
                    np.savetxt("reg1.csv", reg, delimiter=",")
                    np.savetxt("regtt.csv", reg_tt, delimiter=",")
                    np.savetxt("regtf.csv", reg_tf, delimiter=",")
                    np.savetxt("regbt.csv", reg_bt, delimiter=",")
                    #v_i.append(p_t-2.5-np.dot(theta,x))
                    #X=np.concatenate((X,x.reshape(1,5)))
                    y_t.append(int(p_t<=v))
                    v_t.append(v)
                    if t==l_k1:
                        #v_i=np.array(v_i)
                        v_t=np.array(v_t) #vector of vt
                        y_t=np.array(y_t)#vector of y_t
                        p_t_coll=np.array(p_t_coll)
                        X=X[1:] #matrix of X
                        one=np.ones(l_k1+1,dtype=int)
                        one=one.reshape(l_k1+1,1)
                        X_1=np.concatenate((one,X),axis=1)
                        theta1=np.dot(inv(np.dot(X_1.transpose(),X_1)),np.dot(X_1.transpose(),B*y_t))
                        v_i=p_t_coll-np.dot(X_1,theta1).transpose()
                        v_i_true=np.array(v_i_true)
                        #v_i_true=p_t_coll-np.dot(X_1,bp.array(1,).transpose()
                        ker=Kernel(v_i,y_t,l_k1) 
                        ker_tt=Kernel(v_i_true,y_t,l_k1)
                        print('--explore--')
                    t=t+1
                    #v_i=np.array(v_i)
                    #v_t=np.array(v_t) #vector of vt
                    #y_t=np.array(y_t) #vector
                    #exploration
                else:

                #ker=Kernel(v_i,y_t,l_k1) 
                    x=np.dot(mat1,x_m.T)+np.dot(mat2,x_m1.T)+np.array(AcceptReject_2(4,half))#np.sqrt(2/3)*np.array([AcceptReject_x(1,15/8,3) for _ in range(3)])
                    x_m1=x_m
                    x_m=x
                    theta_x=3+np.dot(theta,x)
                    #print(theta_x)
                    true=solu.phi_root(-0.495,0.495,theta_x)
                    op_price=true+theta_x
                    op_rev=solu.F(op_price,theta_x)
                    theta_est=theta1[0]+np.dot(theta1[1:],x)
                    #print(theta_est)
                    est_price=ker.phi_root(np.log(-(true-0.3)/(true+1.4)),theta_est,0.5)+theta_est #p_t
                    rev_diff=op_rev-solu.F(est_price,theta_x)
                    print(rev_diff)
                    #print(est_price)
                    #print(abs(est_price-op_price))
                    est_price_tt=ker_tt.phi_root(np.log(-(true-0.3)/(true+1.4)),theta_x,0.5)+theta_x
                    rev_diff_tt=op_rev-solu.F(est_price_tt,theta_x)
                    #print(abs(est_price_tt-op_price))
                    est_price_tf=solu.phi_root(-0.495,0.495,theta_est)+theta_est
                    rev_diff_tf=op_rev-solu.F(est_price_tf,theta_x)
                    
                    #print(abs(est_price_tf-op_price))
                    reg.append(rev_diff)#exploitation
                    reg_tt.append(rev_diff_tt)
                    reg_tf.append(rev_diff_tf)
                    reg_bt.append(0)
                    np.savetxt("reg1.csv", reg, delimiter=",")
                    np.savetxt("regtt.csv", reg_tt, delimiter=",")
                    np.savetxt("regtf.csv", reg_tf, delimiter=",")
                    np.savetxt("regbt.csv", reg_bt, delimiter=",")
                    if t==l_k:
                        print('--exploit--')
                    t=t+1
        reg=reg[0:T]
        reg_tt=reg_tt[0:T]
        reg_tf=reg_tf[0:T]
        reg_bt=reg_bt[0:T]
        reg_T.append(np.nansum(reg))#for a fixed T, we need to do this for 30 times
        reg_T_tt.append(np.nansum(reg_tt))
        reg_T_tf.append(np.nansum(reg_tf))
        reg_T_bt.append(np.nansum(reg_bt))
        np.savetxt("reg_t1.csv", np.array(reg_T), delimiter=",")
        np.savetxt("reg_tt.csv", np.array(reg_T_tt), delimiter=",")
        np.savetxt("reg_tf.csv", np.array(reg_T_tf), delimiter=",")
        np.savetxt("reg_bt.csv", np.array(reg_T_bt), delimiter=",")
    reg_T=np.array(reg_T)
    reg_T_tt=np.array(reg_T_tt)
    reg_T_tf=np.array(reg_T_tf)
    reg_T_bt=np.array(reg_T_bt)
    #print(reg_T)
    reg_T=reg_T.astype(int)
    reg_T_tt=reg_T_tt.astype(int)
    ref_T_tf=reg_T_tf.astype(int)
    ref_T_bt=reg_T_bt.astype(int)
    reg_Tcum=np.vstack([reg_Tcum,reg_T.reshape(1,30)])#np.array(reg_T)
    reg_Tcum_tt=np.vstack([reg_Tcum_tt,reg_T_tt.reshape(1,30)])
    reg_Tcum_tf=np.vstack([reg_Tcum_tf,reg_T_tf.reshape(1,30)])
    reg_Tcum_bt=np.vstack([reg_Tcum_bt,reg_T_bt.reshape(1,30)])
    #print(reg_Tcum)
    np.savetxt("reg_tcum1.csv", reg_Tcum, delimiter=",")
    np.savetxt("reg_tcum_tt.csv",reg_Tcum_tt, delimiter=",")
    np.savetxt("reg_tcum_tf.csv",reg_Tcum_tf, delimiter=",")
    np.savetxt("reg_tcum_bt.csv",reg_Tcum_bt, delimiter=",")


# In[ ]:




