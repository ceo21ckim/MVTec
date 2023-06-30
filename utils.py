import torch 
import torchgeometry
import numpy as np 

from sklearn.metrics import roc_curve, auc 
from sklearn.manifold import TSNE
from sklearn.utils import shuffle

import matplotlib.pyplot as plt 
import matplotlib as mpl
import matplotlib.colors as mcl
import matplotlib.cm as cm

def torch2npy(tensor):
    if len(tensor.shape) == 4:
        tensor = tensor.unsqueeze(0)
        
    npy = tensor.detach().cpu().numpy()
    return npy


def set_seed(seed=42):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def roc_measure(target, preds):
    fpr, tpr, _ = roc_curve(target, preds, pos_label=1)
    auroc = metrics.auc(fpr, tpr)
    return auroc


def scaler(x):
    if isinstance(x, torch.Tensor):
        _min = torch.min(x)
        _max = torch.max(x)
        
    elif isinstance(x, np.array):
        _min = np.min(x)
        _max = np.max(x)

    outs = (x - _min) / (_max - _min)
    return outs

    
def loss_ssim(preds, target):
    ssim = torchgeometry.losses.SSIM(11, reduction='mean')
    x_ssim = ssim(preds, target)
    
    return x_ssim



## Associated Figure 

def plot_imshow(img, reshape=(1, 2, 0), savefig=False, fname=None):
    if isinstance(img, torch.Tensor):
        img = torch2npy(img)
    img = np.transpose(img, axes=reshape)
    
    plt.figure(figsize = (6, 6))
    plt.imshow(img)
    
    if savefig:
        plt.savefig(f'{fname}.pdf', dpi=100)
    plt.show()

def plot_segmap(target, preds, norm=True, t=(1, 2, 0), save=None, path=None, alpha=0.5):
    target = torch2npy(target, norm, t)
    preds = torch2npy(preds, norm, t)
    
    cmap = cm.hot
    vmax = preds.max()
    vmin = preds.min()
    norms = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    
    colormapping = cm.ScalarMappable(norm=norms, cmap=cmap)
    
    plt.colorbar(colormapping, ax=plt.gca())
    plt.imshow(target)
    plt.imshow(preds, cmap=cmap, alpha=alpha)
    
    if save:
        plt.savefig(path, dpi=200)
    plt.show()


def plot_roc(labels, scores, filename, modelname="", save_plots=False):

    fpr, tpr, _ = roc_curve(labels, scores)
    roc_auc = auc(fpr, tpr)

    #plot roc
    if save_plots:
        plt.figure()
        lw = 2
        plt.plot(fpr, tpr, color='darkorange',
                lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'Receiver operating characteristic {modelname}')
        plt.legend(loc="lower right")
        # plt.show()
        plt.savefig(filename)
        plt.close()

    return roc_auc

def plot_tsne(labels, embeds, filename):
    tsne = TSNE(n_components=2, verbose=1, perplexity=30, n_iter=500)
    embeds, labels = shuffle(embeds, labels)
    tsne_results = tsne.fit_transform(embeds)
    fig, ax = plt.subplots(1)
    colormap = ["b", "r", "c", "y"]

    ax.scatter(tsne_results[:,0], tsne_results[:,1], color=[colormap[l] for l in labels])
    fig.savefig(filename)
    plt.close()
