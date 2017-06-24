#make sure these libraries are installed:
import mdp
import numpy as np
import matplotlib.pyplot as plt

#here is sample data
#concerns are represented on columns, alternatives on lines
var_grid = np.array([[1., 5., 1., 5., 1.],
                     [5., 1., 4., 2., 4.],
                     [1., 5., 1., 4., 2.],
                     [1., 5., 2., 5., 1.],
                     [2., 5., 1., 4., 2.],
                     [1., 4., 2., 5., 1.],
                     [1., 4., 3., 5., 1.],
                     [1., 4., 2., 5., 1.5]])

#improve output readability
np.set_printoptions(precision=2)
np.set_printoptions(suppress=True)

print "var_grid:"
print var_grid

#Create the PCA node and train it
pcan = mdp.nodes.PCANode(output_dim=2, svd=True)
pcar = pcan.execute(var_grid)

print "\npcar"
print pcar

print "\neigenvalues:"
print pcan.d

print "\nexplained variance:"
print pcan.explained_variance

print "\neigenvectors:"
print pcan.v

#Graph results
#pcar[3,0],pcar[3,1] has the projections of alternative3 on the
#first two principal components (0 and 1)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(pcar[:, 0], pcar[:, 1], 'bo')
ax.plot(pcan.v[:, 0], pcan.v[:, 1], 'ro')

#draw axes
ax.axhline(0, color='black')
ax.axvline(0, color='black')

#annotations each concern
id = 0
for xpoint, ypoint in pcan.v:
    ax.annotate('C{:.0f}'.format(id), (xpoint, ypoint), ha='center',
                va='center', bbox=dict(fc='white', ec='none'))
    id += 1


#calculate accounted for variance
var_accounted_PC1 = pcan.d[0] * pcan.explained_variance * 100 / (pcan.d[0] + pcan.d[1])
var_accounted_PC2 = pcan.d[1] * pcan.explained_variance * 100 / (pcan.d[0] + pcan.d[1])

#Show variance accounted for
ax.set_xlabel('Accounted variance on PC1 (%.1f%%)' % (var_accounted_PC1))
ax.set_ylabel('Accounted variance on PC2 (%.1f%%)' % (var_accounted_PC2))

plt.show()
