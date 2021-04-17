import matplotlib.pyplot as plt
#%matplotlib inline

obj1 = [0.8, 0.92, 0.84, 0.86, 0.88, 0.64]
obj2 = [0.88, 0.75, 0.92, 0.96, 1, 1]
obj3 = [0.36, 0.61, 0.74, 0.74, 0.92, 0.72]
x=['Bare', 'No7_val', 'No1', 'No2', 'No3', 'No5']

plt.plot(x, obj1, 'o-', mfc="none", mec="orange", c='orange', ms=10)
#plt.xlabel()
for a, b in zip(x, obj1):
    plt.text(a, b+0.05, (b), ha='center', va='bottom', fontsize=10, c='orange')
plt.ylabel("Success Rate")
plt.ylim(0,1.1)
#plt.title("Graph of the Root-mean-square Error")
plt.show()


plt.plot(x, obj2, 'o-', mfc="none", mec="purple", c='purple', ms=10)
#plt.xlabel()
for a, b in zip(x, obj2):
    plt.text(a, b+0.05, (b), ha='center', va='bottom', fontsize=10, c='purple')
plt.ylabel("Success Rate")
plt.ylim(0,1.1)
#plt.title("Graph of the Root-mean-square Error")
plt.show()


plt.plot(x, obj3, 'o-', mfc="none", mec="g", c='g', ms=10)
#plt.xlabel()
for a, b in zip(x, obj3):
    plt.text(a, b+0.05, (b), ha='center', va='bottom', fontsize=10, c='g')
plt.ylabel("Success Rate")
plt.ylim(0,1.1)
#plt.title("Graph of the Root-mean-square Error")
plt.show()

'''
plt.legend()
#plt.xlabel()
plt.ylabel("Success Rate")
plt.ylim(0,)
#plt.title("Graph of the Root-mean-square Error")
plt.show()
'''

