#-*- coding: utf-8 -*-
######################################################################
######################################################################
#  Copyright Tsung-Hsien Wen, Cambridge Dialogue Systems Group, 2016 #
######################################################################
######################################################################
import sys
import os
import numpy as np

from utils.commandparser    import RNNLGOptParser
from generator.net          import Model
from generator.ngram        import Ngram
from generator.knn          import KNN

import warnings
warnings.simplefilter("ignore", DeprecationWarning)

if __name__ == '__main__':
    
    args = RNNLGOptParser()
    config = args.config
    
    if args.mode=='knn':
        # knn
        knn = KNN(config,args)
        knn.testKNN()
    elif args.mode=='ngram':
        # ngram case
        ngram = Ngram(config,args)
        ngram.testNgram()
    else: 
        # NN case        
        model = Model(config,args)
        if args.mode=='train' or args.mode=='adapt':
            model.trainNet()
        elif args.mode=='test':
            model.testNet()
        elif args.mode=='interactive':
            model.loadConverseParams()
            while True:
                da  = raw_input('DAct : ').decode('utf-8')
                print model.generate(da)        
