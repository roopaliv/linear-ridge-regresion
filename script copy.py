import numpy as np
from scipy.optimize import minimize
from scipy.io import loadmat
from numpy.linalg import det, inv
from math import sqrt, pi
import scipy.io
import matplotlib.pyplot as plt
import pickle
import sys

def ldaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmat - A single d x d learnt covariance matrix 
    
    # IMPLEMENT THIS METHOD 

    k=np.unique(y);
    count=np.zeros((len(k)));
    means=np.zeros((X.shape[1],len(k)));
    for j in range(len(k)):
        for i in range(len(y)):
            if y[i]==k[j]:
                means[:,j]+=X[i,:];
                count[j]+=1;
    means = (means / count [None,:]);
    #print (means);
    covmat=np.cov(X.transpose());
    #print (covmat);
    return means,covmat

def qdaLearn(X,y):
    # Inputs
    # X - a N x d matrix with each row corresponding to a training example
    # y - a N x 1 column vector indicating the labels for each training example
    #
    # Outputs
    # means - A d x k matrix containing learnt means for each of the k classes
    # covmats - A list of k d x d learnt covariance matrices for each of the k classes
    
    # IMPLEMENT THIS METHOD

    covmats=[];
    k=np.unique(y);
    count=np.zeros(len(k));
    means=np.zeros((X.shape[1],len(k)));
    for j in range(len(k)):
        covmat1=[];
        for i in range(len(y)):
            if y[i]==k[j]:
                means[:,j]+=X[i,:];
                count[j]+=1;
                covmat1.append(X[i,:]);
        covmat1 = (np.array(covmat1));
        covmats.append(np.cov(covmat1.transpose()));
    means = (means / count [None,:]);
    #print (means);
    #covmat=np.cov(X);
    #print (covmats);
    return means,covmats

def ldaTest(means,covmat,Xtest,ytest):
    # Inputs
    # means, covmat - parameters of the LDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD
    ypred=np.zeros((Xtest.shape[0],1));
    acc=0;
    for i in range(len(Xtest)):
        predicted=0;
        px=np.zeros(len(means[0]));
        for j in range(len(means[0])):
            transpose1=(np.subtract(Xtest[i],means[:,j])).transpose();
            product1=np.matmul(transpose1,np.linalg.inv(covmat));
            px[j]=np.matmul(product1,np.subtract(Xtest[i],means[:,j]));
            px[j]/=np.linalg.det(covmat);
            if px[j]<px[predicted]:
                predicted=j;
        ypred[i][0]=(predicted+1);
        #print(str(predicted+1)+"----"+str(ytest[i][0]));
        if(ypred[i][0]==ytest[i][0]):
            acc+=1;
    #print(acc);
    return acc,ypred

def qdaTest(means,covmats,Xtest,ytest):
    # Inputs
    # means, covmats - parameters of the QDA model
    # Xtest - a N x d matrix with each row corresponding to a test example
    # ytest - a N x 1 column vector indicating the labels for each test example
    # Outputs
    # acc - A scalar accuracy value
    # ypred - N x 1 column vector indicating the predicted labels

    # IMPLEMENT THIS METHOD

    ypred=np.zeros((Xtest.shape[0],1));
    acc=0;
    for i in range(len(Xtest)):
        predicted=0;
        px=np.zeros(len(means[0]));
        for j in range(len(means[0])):
            transpose1=(np.subtract(Xtest[i],means[:,j])).transpose();
            product1=np.matmul(transpose1,np.linalg.inv(covmats[j]));
            px[j]=np.matmul(product1,np.subtract(Xtest[i],means[:,j]));
            px[j]=np.exp(px[j]*(-0.5));
            px[j]/=sqrt(np.linalg.det(covmats[j]));
            if px[j]>px[predicted]:
                predicted=j;
        ypred[i][0]=(predicted+1);
        #print(str(predicted+1)+"----"+str(ytest[i][0]));
        if(ypred[i][0]==ytest[i][0]):
            acc+=1;
    #print(acc);
    return acc,ypred

def learnOLERegression(X,y):
    # Inputs:                                                         
    # X = N x d 
    # y = N x 1                                                               
    # Output: 
    # w = d x 1 
    
    # IMPLEMENT THIS METHOD
    term1=np.matmul(X.transpose(), X);
    term2=np.matmul(inv(term1), X.transpose());
    w=np.matmul(term2,y);
    return w

def learnRidgeRegression(X,y,lambd):
    # Inputs:
    # X = N x d                                                               
    # y = N x 1 
    # lambd = ridge parameter (scalar)
    # Output:                                                                  
    # w = d x 1                                                                

    # IMPLEMENT THIS METHOD  
    #w = (X.shape[0] * lambd * np.identity(X.shape[1])) + np.dot(X.T, X)
    #w = np.linalg.inv(w)
    #w = np.dot(w, X.T)
    #w = np.dot(w, y)    
    #xtx = np.dot(X.transpose(),X)
    #no_of_columns = X.shape[1]
    #no_of_rows = X.shape[0]
    #lambda_identity_matrix = lambd*np.eye(no_of_columns)
    #lambda_identity_matrix = no_of_rows*lambda_identity_matrix
    #w = xtx + lambda_identity_matrix
    #w = inv(w)
    #w = np.dot(w,X.transpose())
    #w = np.dot(w,y)  

    cols = X.shape[1]
    rows = X.shape[0]
    identity = rows* lambd * np.identity(cols)
    w = identity + np.dot(X.transpose(),X)
    w = np.linalg.inv(w)
    w = np.dot(w,X.transpose())
    w = np.dot(w,y)  
    return w

def testOLERegression(w,Xtest,ytest):
    # Inputs:
    # w = d x 1
    # Xtest = N x d
    # ytest = X x 1
    # Output:
    # mse
    
    # IMPLEMENT THIS METHOD
    term1=np.matmul(Xtest,w);
    term2=np.subtract(ytest,term1);
    mse=np.matmul(term2.transpose(),term2);
    mse/=Xtest.shape[0];    
    return mse

def regressionObjVal(w, X, y, lambd):

    # compute squared error (scalar) and gradient of squared error with respect
    # to w (vector) for the given data X and y and the regularization parameter
    # lambda                                                                  

    # IMPLEMENT THIS METHOD  
    #sumSquare = np.sum(np.square((y-np.dot(X,w.reshape((w.shape[0],1))))))
    #error = ((1.0/(2.0 * X.shape[0])) * sumSquare) + (.5 * lambd * np.dot(w.T, w))
    #error_grad = ((((-1.0 * np.dot(y.T, X)) + (np.dot(w.T, np.dot(X.T, X)))) / X.shape[0]) + (lambd * w)).flatten()  
    #N_rows_X=X.shape[0]
    #w=w.reshape(X.shape[1],1)  
    #error=(0.5/N_rows_X)*np.dot((y-np.dot(X,w)).transpose(),(y-np.dot(X,w)))+0.5*lambd*np.dot(w.transpose(),w)
    #error_grad=(1.0/N_rows_X)*(np.dot(w.transpose(),np.dot(X.transpose(),X))-np.dot(y.transpose(),X))+lambd*w.transpose() 
    #error_grad=error_grad.transpose()
    #error_grad=error_grad.flatten()    

    rows=X.shape[0]
    sumSquare = np.sum(np.square((y-np.dot(X,w.reshape((w.shape[0],1))))))
    error = (0.5) * sumSquare + (0.5 * lambd * np.dot(w.T, w))
    #error_grad = ((((-1.0 * np.dot(y.T, X)) + (np.dot(w.T, np.dot(X.T, X)))) / X.shape[0]) + (lambd * w)).flatten()  
    error_grad=(1.0/rows)*(np.dot(w.transpose(),np.dot(X.transpose(),X))-np.dot(y.transpose(),X))+lambd*w.transpose() 
    error_grad=error_grad.transpose()
    error_grad=error_grad.flatten()    
   
    return error, error_grad

def mapNonLinear(x,p):
    # Inputs:                                                                  
    # x - a single column vector (N x 1)                                       
    # p - integer (>= 0)                                                       
    # Outputs:                                                                 
    # Xd - (N x (d+1)) 
    
    # IMPLEMENT THIS METHOD
    return Xd

# Main script

# Problem 1
# load the sample data                                                                 
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('sample.pickle','rb'),encoding = 'latin1')

# LDA
means,covmat = ldaLearn(X,y)
ldaacc,ldares = ldaTest(means,covmat,Xtest,ytest)
print('LDA Accuracy = '+str(ldaacc))
# QDA
means,covmats = qdaLearn(X,y)
qdaacc,qdares = qdaTest(means,covmats,Xtest,ytest)
print('QDA Accuracy = '+str(qdaacc))

# plotting boundaries
x1 = np.linspace(-5,20,100)
x2 = np.linspace(-5,20,100)
xx1,xx2 = np.meshgrid(x1,x2)
xx = np.zeros((x1.shape[0]*x2.shape[0],2))
xx[:,0] = xx1.ravel()
xx[:,1] = xx2.ravel()

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)

zacc,zldares = ldaTest(means,covmat,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zldares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest)
plt.title('LDA')

plt.subplot(1, 2, 2)

zacc,zqdares = qdaTest(means,covmats,xx,np.zeros((xx.shape[0],1)))
plt.contourf(x1,x2,zqdares.reshape((x1.shape[0],x2.shape[0])),alpha=0.3)
plt.scatter(Xtest[:,0],Xtest[:,1],c=ytest)
plt.title('QDA')

plt.show()
# Problem 2
if sys.version_info.major == 2:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'))
else:
    X,y,Xtest,ytest = pickle.load(open('diabetes.pickle','rb'),encoding = 'latin1')

# add intercept
X_i = np.concatenate((np.ones((X.shape[0],1)), X), axis=1)
Xtest_i = np.concatenate((np.ones((Xtest.shape[0],1)), Xtest), axis=1)

w = learnOLERegression(X,y)
mle = testOLERegression(w,Xtest,ytest)

w_i = learnOLERegression(X_i,y)
mle_i = testOLERegression(w_i,Xtest_i,ytest)

print('MSE without intercept '+str(mle))
print('MSE with intercept '+str(mle_i))

# Problem 3
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses3_train = np.zeros((k,1))
mses3 = np.zeros((k,1))
for lambd in lambdas:
    w_l = learnRidgeRegression(X_i,y,lambd)
    mses3_train[i] = testOLERegression(w_l,X_i,y)
    mses3[i] = testOLERegression(w_l,Xtest_i,ytest)
    i = i + 1
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.subplot(1, 2, 2)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')

plt.show()
# Problem 4
k = 101
lambdas = np.linspace(0, 1, num=k)
i = 0
mses4_train = np.zeros((k,1))
mses4 = np.zeros((k,1))
opts = {'maxiter' : 20}    # Preferred value.                                                
w_init = np.ones((X_i.shape[1],1))
for lambd in lambdas:
    args = (X_i, y, lambd)
    w_l = minimize(regressionObjVal, w_init, jac=True, args=args,method='CG', options=opts)
    w_l = np.transpose(np.array(w_l.x))
    w_l = np.reshape(w_l,[len(w_l),1])
    mses4_train[i] = testOLERegression(w_l,X_i,y)
    mses4[i] = testOLERegression(w_l,Xtest_i,ytest)
    i = i + 1
fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(lambdas,mses4_train)
plt.plot(lambdas,mses3_train)
plt.title('MSE for Train Data')
plt.legend(['Using scipy.minimize','Direct minimization'])

plt.subplot(1, 2, 2)
plt.plot(lambdas,mses4)
plt.plot(lambdas,mses3)
plt.title('MSE for Test Data')
plt.legend(['Using scipy.minimize','Direct minimization'])
plt.show()


# Problem 5
pmax = 7
lambda_opt = 0 # REPLACE THIS WITH lambda_opt estimated from Problem 3
mses5_train = np.zeros((pmax,2))
mses5 = np.zeros((pmax,2))
for p in range(pmax):
    Xd = mapNonLinear(X[:,2],p)
    Xdtest = mapNonLinear(Xtest[:,2],p)
    w_d1 = learnRidgeRegression(Xd,y,0)
    mses5_train[p,0] = testOLERegression(w_d1,Xd,y)
    mses5[p,0] = testOLERegression(w_d1,Xdtest,ytest)
    w_d2 = learnRidgeRegression(Xd,y,lambda_opt)
    mses5_train[p,1] = testOLERegression(w_d2,Xd,y)
    mses5[p,1] = testOLERegression(w_d2,Xdtest,ytest)

fig = plt.figure(figsize=[12,6])
plt.subplot(1, 2, 1)
plt.plot(range(pmax),mses5_train)
plt.title('MSE for Train Data')
plt.legend(('No Regularization','Regularization'))
plt.subplot(1, 2, 2)
plt.plot(range(pmax),mses5)
plt.title('MSE for Test Data')
plt.legend(('No Regularization','Regularization'))
plt.show()
